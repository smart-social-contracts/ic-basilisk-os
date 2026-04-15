"""
Basilisk Realm CLI — manage realm extensions at runtime.

Commands:
  basilisk install-extension     Install an extension on a deployed realm canister
  basilisk uninstall-extension   Uninstall a runtime extension from a realm canister
  basilisk list-extensions       List runtime-installed extensions on a realm canister
"""

import json
import os
import subprocess
import sys


_HELP_INSTALL_EXTENSION = """\
basilisk install-extension — Install an extension on a deployed realm canister.

Reads the extension's backend files from a local directory and uploads
them to the canister's persistent filesystem via the install_extension endpoint.

Usage: basilisk install-extension [options]

Required:
  --canister <id>      Target realm canister ID
  --source <dir>       Path to extension directory (must contain manifest.json)

Options:
  --network <net>      Network: local, ic     [default: local]
  --identity <name>    dfx identity to use    [default: current]

The extension directory should have:
  manifest.json       Extension metadata
  backend/entry.py    Backend entry point (functions callable via extension_call)
  backend/*.py        Additional backend Python files (optional)

Examples:
  basilisk install-extension --canister lqy7q-... --source ./extensions/voting
  basilisk install-extension --canister lqy7q-... --source ./extensions/voting --network ic
"""

_HELP_UNINSTALL_EXTENSION = """\
basilisk uninstall-extension — Remove a runtime extension from a realm canister.

Usage: basilisk uninstall-extension [options]

Required:
  --canister <id>      Target realm canister ID
  --extension <name>   Extension ID to uninstall

Options:
  --network <net>      Network: local, ic     [default: local]
  --identity <name>    dfx identity to use    [default: current]

Examples:
  basilisk uninstall-extension --canister lqy7q-... --extension voting
"""

_HELP_LIST_EXTENSIONS = """\
basilisk list-extensions — List runtime-installed extensions on a realm canister.

Usage: basilisk list-extensions [options]

Required:
  --canister <id>      Target realm canister ID

Options:
  --network <net>      Network: local, ic     [default: local]
  --identity <name>    dfx identity to use    [default: current]
  --json               Output raw JSON

Examples:
  basilisk list-extensions --canister lqy7q-...
"""


def _parse_candid_string(raw: str) -> str:
    """Parse a Candid text response from dfx canister call."""
    raw = raw.strip()
    if raw.startswith("(") and raw.endswith(")"):
        raw = raw[1:-1].strip()
    if raw.endswith(","):
        raw = raw[:-1].strip()
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    raw = raw.replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")
    return raw


def _dfx_call(canister, method, arg, network, identity, is_query=False, timeout=120):
    """Run a dfx canister call and return parsed output."""
    cmd = ["dfx", "canister", "call"]
    if identity:
        cmd.extend(["--identity", identity])
    if network:
        cmd.extend(["--network", network])
    if is_query:
        cmd.append("--query")
    cmd.extend([canister, method, arg])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            print(f"Error: {result.stderr.strip()}", file=sys.stderr)
            sys.exit(1)
        return _parse_candid_string(result.stdout)
    except subprocess.TimeoutExpired:
        print(f"Error: canister call timed out ({timeout}s)", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: dfx not found. Install the DFINITY SDK.", file=sys.stderr)
        sys.exit(1)


def _parse_common_args(args):
    """Parse common flags: --canister, --network, --identity, --json."""
    canister = None
    network = "local"
    identity = None
    raw_json = False
    remaining = []

    i = 0
    while i < len(args):
        if args[i] == "--canister" and i + 1 < len(args):
            canister = args[i + 1]
            i += 2
        elif args[i] == "--network" and i + 1 < len(args):
            network = args[i + 1]
            i += 2
        elif args[i] == "--identity" and i + 1 < len(args):
            identity = args[i + 1]
            i += 2
        elif args[i] == "--json":
            raw_json = True
            i += 1
        else:
            remaining.append(args[i])
            i += 1

    return canister, network, identity, raw_json, remaining


def _collect_extension_files(source_dir: str) -> dict:
    """Collect extension files from a source directory into a {filename: content} dict.

    Reads manifest.json from the root, and all .py files from backend/.
    Backend files are flattened: backend/entry.py -> entry.py, backend/utils.py -> utils.py
    """
    files = {}

    # manifest.json (required)
    manifest_path = os.path.join(source_dir, "manifest.json")
    if not os.path.exists(manifest_path):
        print(f"Error: manifest.json not found in {source_dir}", file=sys.stderr)
        sys.exit(1)
    with open(manifest_path, "r") as f:
        files["manifest.json"] = f.read()

    # Backend .py files
    backend_dir = os.path.join(source_dir, "backend")
    if os.path.isdir(backend_dir):
        for root, _dirs, filenames in os.walk(backend_dir):
            for fname in filenames:
                if fname.endswith(".py"):
                    full_path = os.path.join(root, fname)
                    # Flatten: backend/entry.py -> entry.py
                    rel = os.path.relpath(full_path, backend_dir)
                    with open(full_path, "r") as f:
                        files[rel] = f.read()
    else:
        # Check for entry.py at root level
        entry_path = os.path.join(source_dir, "entry.py")
        if os.path.exists(entry_path):
            with open(entry_path, "r") as f:
                files["entry.py"] = f.read()

    if "entry.py" not in files:
        print(f"Error: entry.py not found in {source_dir}/backend/ or {source_dir}/", file=sys.stderr)
        sys.exit(1)

    return files


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_install_extension(args):
    """Install a runtime extension on a realm canister."""
    if "--help" in args or "-h" in args:
        print(_HELP_INSTALL_EXTENSION, end="")
        return

    canister, network, identity, _, remaining = _parse_common_args(args)

    source_dir = None
    i = 0
    while i < len(remaining):
        if remaining[i] == "--source" and i + 1 < len(remaining):
            source_dir = remaining[i + 1]
            i += 2
        else:
            i += 1

    if not canister:
        print("Error: --canister is required", file=sys.stderr)
        sys.exit(1)
    if not source_dir:
        print("Error: --source is required", file=sys.stderr)
        sys.exit(1)

    source_dir = os.path.abspath(source_dir)
    if not os.path.isdir(source_dir):
        print(f"Error: {source_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Read manifest to get extension ID
    manifest_path = os.path.join(source_dir, "manifest.json")
    with open(manifest_path, "r") as f:
        manifest = json.loads(f.read())
    ext_id = manifest.get("name") or os.path.basename(source_dir)

    print(f"Installing extension '{ext_id}' on {canister} ({network})...")

    # Collect files
    files = _collect_extension_files(source_dir)
    total_bytes = sum(len(v) for v in files.values())
    print(f"  Files: {len(files)} ({total_bytes:,} bytes)")
    for fname, content in sorted(files.items()):
        print(f"    {fname} ({len(content):,} bytes)")

    # Build the JSON payload
    payload = json.dumps({"extension_id": ext_id, "files": files})

    # Escape for Candid text format
    candid_arg = '("' + payload.replace("\\", "\\\\").replace('"', '\\"') + '")'

    print(f"  Uploading to canister...")
    raw = _dfx_call(canister, "install_extension", candid_arg, network, identity, timeout=300)

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        print(f"  Response: {raw}")
        return

    if result.get("success"):
        print(f"  ✓ Extension '{ext_id}' installed successfully")
    else:
        print(f"  ✗ Installation failed: {result.get('error', 'unknown error')}", file=sys.stderr)
        sys.exit(1)


def cmd_uninstall_extension(args):
    """Uninstall a runtime extension from a realm canister."""
    if "--help" in args or "-h" in args:
        print(_HELP_UNINSTALL_EXTENSION, end="")
        return

    canister, network, identity, _, remaining = _parse_common_args(args)

    ext_id = None
    i = 0
    while i < len(remaining):
        if remaining[i] == "--extension" and i + 1 < len(remaining):
            ext_id = remaining[i + 1]
            i += 2
        else:
            i += 1

    if not canister:
        print("Error: --canister is required", file=sys.stderr)
        sys.exit(1)
    if not ext_id:
        print("Error: --extension is required", file=sys.stderr)
        sys.exit(1)

    print(f"Uninstalling extension '{ext_id}' from {canister} ({network})...")

    payload = json.dumps({"extension_id": ext_id})
    candid_arg = '("' + payload.replace("\\", "\\\\").replace('"', '\\"') + '")'

    raw = _dfx_call(canister, "uninstall_extension", candid_arg, network, identity)

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        print(f"  Response: {raw}")
        return

    if result.get("success"):
        print(f"  ✓ Extension '{ext_id}' uninstalled")
    else:
        print(f"  ✗ Uninstall failed: {result.get('error', 'unknown error')}", file=sys.stderr)
        sys.exit(1)


def cmd_list_extensions(args):
    """List runtime-installed extensions on a realm canister."""
    if "--help" in args or "-h" in args:
        print(_HELP_LIST_EXTENSIONS, end="")
        return

    canister, network, identity, raw_json, _ = _parse_common_args(args)

    if not canister:
        print("Error: --canister is required", file=sys.stderr)
        sys.exit(1)

    raw = _dfx_call(canister, "list_runtime_extensions", "()", network, identity, is_query=True)

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        print(raw)
        return

    if raw_json:
        print(json.dumps(result, indent=2))
        return

    if not result.get("success"):
        print(f"Error: {result.get('error', 'unknown')}", file=sys.stderr)
        sys.exit(1)

    extensions = result.get("runtime_extensions", [])
    manifests = result.get("all_manifests", {})

    if not extensions and not manifests:
        print("No extensions installed.")
        return

    # Show runtime extensions
    if extensions:
        print(f"Runtime extensions ({len(extensions)}):")
        for ext_id in extensions:
            m = manifests.get(ext_id, {})
            name = m.get("name", ext_id)
            version = m.get("version", "?")
            desc = m.get("description", "")
            print(f"  {ext_id} v{version} — {desc}" if desc else f"  {ext_id} v{version}")

    # Show baked-in extensions (in manifests but not in runtime)
    baked = [k for k in manifests if k not in extensions]
    if baked:
        print(f"\nBaked-in extensions ({len(baked)}):")
        for ext_id in baked:
            m = manifests[ext_id]
            version = m.get("version", "?")
            desc = m.get("description", "")
            print(f"  {ext_id} v{version} — {desc}" if desc else f"  {ext_id} v{version}")
