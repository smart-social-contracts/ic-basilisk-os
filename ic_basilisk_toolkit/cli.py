"""
Basilisk Toolkit — CLI for canister interaction.

Usage: basilisk-toolkit <command> [options]

Commands:
  exec <code>      Execute Python code on a deployed canister
  shell            Interactive Python shell on a deployed canister
  sshd             Start an SSH/SFTP server proxy to a canister
  deploy           Deploy a new basilisk canister from the on-chain deployer
  upgrade          Upgrade an existing canister to a new WASM version
  versions         List available WASM versions on the deployer
  deployments      List deployment history

  install-extension    Install a runtime extension on a realm canister
  uninstall-extension  Uninstall a runtime extension from a realm canister
  list-extensions      List runtime-installed extensions on a realm canister

Options (exec, shell, sshd):
  --canister <id>   Canister name or principal ID  [auto-detect from dfx.json]
  --network <net>   Network: local, ic, or URL     [default: local]
  --identity <name> dfx identity to use            [default: current identity]

Other:
  --version        Print version info
  help, -h         Show this help

Run basilisk-toolkit <command> --help for command-specific options and examples.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

_HELP_EXEC = """\
basilisk-toolkit exec — Execute Python code on a deployed canister.

Usage: basilisk-toolkit exec [options] <code>
       basilisk-toolkit exec [options] -f <file>
       echo "code" | basilisk-toolkit exec [options]

Options:
  --canister <id>  Canister name or principal ID  [auto-detect from dfx.json]
  --network <net>  Network: local, ic, or URL     [default: local]
  -f <file>        Execute a local Python file instead of inline code

Examples:
  basilisk-toolkit exec 'print("hello")'                         Inline code
  basilisk-toolkit exec --canister my_app 'print(1+1)'           Explicit canister
  basilisk-toolkit exec --network ic 'print(ic.time())'          On mainnet
  basilisk-toolkit exec -f script.py                             Run a local file
  echo "import sys; print(sys.version)" | basilisk-toolkit exec  Pipe from stdin
"""


def _detect_canister_from_dfx() -> str | None:
    """Try to find the first basilisk canister name from dfx.json."""
    if not Path("dfx.json").exists():
        return None
    try:
        with open("dfx.json") as f:
            dfx = json.load(f)
        for name, config in dfx.get("canisters", {}).items():
            if "basilisk" in config.get("build", ""):
                return name
    except Exception:
        pass
    return None


def _parse_candid_string(raw: str) -> str:
    """Parse a Candid text response from dfx canister call."""
    raw = raw.strip()
    # Remove outer parens: (text "...")
    if raw.startswith("(") and raw.endswith(")"):
        raw = raw[1:-1].strip()
    # Remove 'text' prefix if present
    if raw.startswith("text "):
        raw = raw[5:].strip()
    # Remove surrounding quotes
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    # Unescape
    raw = raw.replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")
    return raw


def cmd_exec(args: list[str]):
    """Execute Python code on a deployed basilisk canister."""
    canister = None
    network = None
    identity = None
    file_path = None
    code_parts = []

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
        elif args[i] == "-f" and i + 1 < len(args):
            file_path = args[i + 1]
            i += 2
        else:
            code_parts.append(args[i])
            i += 1

    # Get code from file or args
    if file_path:
        try:
            code = Path(file_path).read_text()
        except FileNotFoundError:
            print(f"Error: file not found: {file_path}", file=sys.stderr)
            sys.exit(1)
    elif code_parts:
        code = " ".join(code_parts)
    else:
        # Read from stdin
        code = sys.stdin.read()

    if not code.strip():
        print(
            "Error: no code provided. Usage: basilisk-toolkit exec [--canister <c>] [--network <n>] [-f <file>] <code>",
            file=sys.stderr,
        )
        sys.exit(1)

    # Auto-detect canister if not specified
    if not canister:
        canister = _detect_canister_from_dfx()
        if not canister:
            print(
                "Error: --canister required (could not auto-detect from dfx.json)",
                file=sys.stderr,
            )
            sys.exit(1)

    # Build dfx command
    escaped_code = code.replace('"', '\\"').replace("\n", "\\n")
    cmd = ["dfx", "canister", "call"]
    if identity:
        cmd.extend(["--identity", identity])
    if network:
        cmd.extend(["--network", network])
    cmd.extend([canister, "execute_code_shell", f'("{escaped_code}")'])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(result.stderr.strip(), file=sys.stderr)
            sys.exit(1)
        output = _parse_candid_string(result.stdout)
        if output:
            print(output, end="" if output.endswith("\n") else "\n")
    except subprocess.TimeoutExpired:
        print("Error: canister call timed out (120s)", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: dfx not found. Install the DFINITY SDK.", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    command = sys.argv[1]

    if command == "exec":
        if "--help" in sys.argv[2:] or "-h" in sys.argv[2:]:
            print(_HELP_EXEC, end="")
            return
        cmd_exec(sys.argv[2:])

    elif command == "shell":
        from ic_basilisk_toolkit.shell import main as shell_main

        sys.argv = ["basilisk-toolkit-shell"] + sys.argv[2:]
        shell_main()

    elif command == "sshd":
        from ic_basilisk_toolkit.sshd import main as sshd_main

        sys.argv = ["basilisk-toolkit-sshd"] + sys.argv[2:]
        sshd_main()

    elif command == "deploy":
        from ic_basilisk_toolkit.deployer import cmd_deploy

        cmd_deploy(sys.argv[2:])

    elif command == "upgrade":
        from ic_basilisk_toolkit.deployer import cmd_upgrade

        cmd_upgrade(sys.argv[2:])

    elif command == "versions":
        from ic_basilisk_toolkit.deployer import cmd_versions

        cmd_versions(sys.argv[2:])

    elif command == "deployments":
        from ic_basilisk_toolkit.deployer import cmd_deployments

        cmd_deployments(sys.argv[2:])

    elif command == "install-extension":
        from ic_basilisk_toolkit.realm import cmd_install_extension

        cmd_install_extension(sys.argv[2:])

    elif command == "uninstall-extension":
        from ic_basilisk_toolkit.realm import cmd_uninstall_extension

        cmd_uninstall_extension(sys.argv[2:])

    elif command == "list-extensions":
        from ic_basilisk_toolkit.realm import cmd_list_extensions

        cmd_list_extensions(sys.argv[2:])

    elif command in ("-h", "--help", "help"):
        print(__doc__.strip())

    elif command == "--version":
        from ic_basilisk_toolkit import __version__

        print(__version__)

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print(__doc__.strip())
        sys.exit(1)


# ---------------------------------------------------------------------------
# Entry-point handlers for basilisk CLI plugin discovery
# (registered via pyproject.toml [project.entry-points."basilisk.commands"])
# ---------------------------------------------------------------------------


def plugin_shell():
    """basilisk shell — Interactive Python shell on a deployed canister."""
    from ic_basilisk_toolkit.shell import main as shell_main

    sys.argv = ["basilisk shell"] + sys.argv[2:]
    shell_main()


def plugin_exec():
    """basilisk exec — Execute Python code on a deployed canister."""
    if "--help" in sys.argv[2:] or "-h" in sys.argv[2:]:
        print(_HELP_EXEC, end="")
        return
    cmd_exec(sys.argv[2:])


def plugin_sshd():
    """basilisk sshd — Start an SSH/SFTP server proxy to a canister."""
    from ic_basilisk_toolkit.sshd import main as sshd_main

    sys.argv = ["basilisk sshd"] + sys.argv[2:]
    sshd_main()


def plugin_deploy():
    """basilisk deploy — Deploy a new basilisk canister."""
    from ic_basilisk_toolkit.deployer import cmd_deploy

    cmd_deploy(sys.argv[2:])


def plugin_upgrade():
    """basilisk upgrade — Upgrade an existing canister."""
    from ic_basilisk_toolkit.deployer import cmd_upgrade

    cmd_upgrade(sys.argv[2:])


def plugin_versions():
    """basilisk versions — List available WASM versions."""
    from ic_basilisk_toolkit.deployer import cmd_versions

    cmd_versions(sys.argv[2:])


def plugin_deployments():
    """basilisk deployments — List deployment history."""
    from ic_basilisk_toolkit.deployer import cmd_deployments

    cmd_deployments(sys.argv[2:])


def plugin_install_extension():
    """basilisk install-extension — Install a runtime extension on a realm canister."""
    from ic_basilisk_toolkit.realm import cmd_install_extension

    cmd_install_extension(sys.argv[2:])


def plugin_uninstall_extension():
    """basilisk uninstall-extension — Uninstall a runtime extension."""
    from ic_basilisk_toolkit.realm import cmd_uninstall_extension

    cmd_uninstall_extension(sys.argv[2:])


def plugin_list_extensions():
    """basilisk list-extensions — List runtime-installed extensions."""
    from ic_basilisk_toolkit.realm import cmd_list_extensions

    cmd_list_extensions(sys.argv[2:])


if __name__ == "__main__":
    main()
