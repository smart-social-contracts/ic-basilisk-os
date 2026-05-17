# ic-basilisk-toolkit

**Basilisk Toolkit** — A set of ready-made tools on top of [Basilisk](https://github.com/smart-social-contracts/basilisk) CDK for IC Python canisters.

**Live demo:** [https://ic-basilisk.tech/](https://ic-basilisk.tech/).

## Overview

<table>
<tr>
  <td><strong>Task Management</strong></td>
  <td>Create, schedule, and run background tasks</td>
</tr>
<tr><td colspan="2">

```shell
%task create heartbeat every 60s --code "print('alive')"
%task start 1
%task info 1
%task list
```
```python
t = Task(name="sync")
TaskStep(task=t, code="print('syncing...')")
TaskSchedule(task=t, interval=60)
TaskManager().run()
```
</td></tr>
<tr>
  <td><strong>Wallet</strong></td>
  <td>ICRC-1 token registry, transfers, balance tracking</td>
</tr>
<tr><td colspan="2">

```shell
%wallet balance
%wallet transfer ckBTC <principal> 1000
```
```python
w = Wallet()
w.register_token("ckBTC", ledger="mxzaz-...", indexer="n5wcd-...")
yield from w.balance_of("ckBTC")
yield from w.transfer("ckBTC", to_principal, amount=1000)
yield from w.refresh("ckBTC", max_results=50)
w.list_transfers("ckBTC", limit=20)
```
</td></tr>
<tr>
  <td><strong>Encryption</strong></td>
  <td>vetKeys + per-principal envelopes + groups</td>
</tr>
<tr><td colspan="2">

```shell
%crypto encrypt "secret"
%group create team1
%group add team1 <principal>
```
```python
cs = CryptoService(vetkey_service)
yield from cs.init_scope("my-scope")
cs.grant_access("my-scope", target_principal)
cs.create_group("team")
cs.add_member("team", principal)
cs.grant_group_access("my-scope", "team")
cs.revoke_access("my-scope", principal)
```
</td></tr>
<tr>
  <td><strong>FX</strong></td>
  <td>Exchange rate queries via the IC XRC canister</td>
</tr>
<tr><td colspan="2">

```shell
%fx ICP/USD
```
```python
fx = FXService()
fx.register_pair("ICP", "USD")
yield from fx.refresh()         # fetch latest rates from XRC canister
fx.get_rate("ICP", "USD")       # cached float
fx.get_rate_info("ICP", "USD")  # full info with staleness metadata
```
</td></tr>
<tr>
  <td><strong>Entities</strong></td>
  <td>Persistent ORM via <a href="https://github.com/smart-social-contracts/ic-python-db">ic-python-db</a></td>
</tr>
<tr><td colspan="2">

```shell
%db types
%db list User 10
%db show User 1
%db search User name=alice
%db export User backup.json
%db import backup.json
```
```python
u = User(name="alice")
u.save()
User.load(1)
User.instances()
User.count()
```
</td></tr>
<tr>
  <td><strong>Logging</strong></td>
  <td>Structured logging via <a href="https://github.com/smart-social-contracts/ic-python-logging">ic-python-logging</a></td>
</tr>
<tr><td colspan="2">

```python
from ic_python_logging import get_logger
logger = get_logger("my_module")
logger.info("processing")
logger.error("failed", exc_info=True)
```
</td></tr>
<tr>
  <td><strong>HTTP Fetch</strong></td>
  <td>Download a URL into the canister filesystem</td>
</tr>
<tr><td colspan="2">

```shell
%wget https://example.com/data.json /data.json
```
```python
yield from wget("https://example.com/data.json", "/data.json")
run("/data.json")  # execute a downloaded Python script
```
</td></tr>
<tr>
  <td><strong>File Transfer</strong></td>
  <td>Move files between local machine and canister</td>
</tr>
<tr><td colspan="2">

```shell
%put local_script.py /app/script.py
%get /app/output.json result.json
```
</td></tr>
<tr>
  <td><strong>Interactive Shell</strong></td>
  <td>REPL for live canister interaction</td>
</tr>
<tr><td colspan="2">

```shell
basilisk-toolkit shell --canister my_app --network ic
basilisk-toolkit exec --canister my_app 'print(ic.time())'
```
</td></tr>
<tr>
  <td><strong>SFTP</strong></td>
  <td>Browse and edit canister filesystem over SSH</td>
</tr>
<tr><td colspan="2">

```shell
basilisk-toolkit sshd --canister my_app --network ic
sftp -P 2222 localhost
ssh -p 2222 localhost
```
</td></tr>
</table>

Type `:help` inside the shell for full command reference, or see the [tip_jar template](templates/tip_jar) for a working example project.

## Templates

Full-stack example canisters, each deployable as-is:

- [**Tip Jar**](templates/tip_jar) — crypto donations in ckBTC / ckETH / ckUSDC / ICP with live exchange rates, encrypted messages, donor leaderboard. [Live](https://ox2q2-saaaa-aaaau-agj7a-cai.icp0.io/).
- [**File Registry**](templates/file_registry) — general-purpose on-chain file storage with HTTP serving, CORS, chunked upload for large WASMs, and per-namespace ACLs. [Live](https://oe3kv-3aaaa-aaaac-qgmzq-cai.icp0.io/).

## Website

[`website/`](website/) is the static landing page at [ic-basilisk.tech](https://ic-basilisk.tech/) — it introduces basilisk and this toolkit and links out to the live template demos. Pure assets canister, no backend.

## Installation

```bash
pip install ic-basilisk-toolkit
```

For shell/SFTP support (requires `asyncssh`):
```bash
pip install ic-basilisk-toolkit[shell]
```

## CLI Usage

```
basilisk-toolkit exec 'print("hello")'                    # Execute code on canister
basilisk-toolkit shell --canister my_app --network ic      # Interactive shell
basilisk-toolkit sshd --canister my_app --network ic       # SSH/SFTP server
```

## Schema Upgrade Checking

The `check-upgrade` command compares the on-chain schema with your local Entity definitions before you deploy, catching breaking changes early:

```bash
basilisk check-upgrade --canister my_app --network local
```

### Example: Full Test Workflow

```python
# src/main.py
from basilisk import query, update, text, nat64, void, init, ic, StableBTreeMap
from ic_python_db import Database, Entity
from ic_python_db.properties import String, Integer

__basilisk_features__ = ["browse"]

storage = StableBTreeMap[str, str](memory_id=1, max_key_size=100, max_value_size=10000)
db = Database.init(db_storage=storage)


class User(Entity):
    __db__ = db
    name = String(default="")
    age = Integer(default=0)


@init
def init_() -> void:
    db.save_schema()
    User(name="alice", age=30)
```

**Step 1 — No changes (clean):**

```
$ basilisk check-upgrade --canister my_app --network local
No schema changes detected. Safe to upgrade.
```

**Step 2 — Add a field with a default (safe):**

```python
class User(Entity):
    __db__ = db
    name = String(default="")
    age = Integer(default=0)
    email = String(default="unknown@example.com")  # new field
```

```
$ basilisk check-upgrade --canister my_app --network local
Schema changes (1 total):
  ✅  User.email: New field with default='unknown@example.com' — auto-migratable
All 1 change(s) are safe. No migration needed.
```

**Step 3 — Change a field type (breaking):**

```python
from ic_python_db.properties import String, Float

class User(Entity):
    __db__ = db
    name = String(default="")
    age = Float(default=0.0)   # was Integer
    email = String(default="unknown@example.com")
```

```
$ basilisk check-upgrade --canister my_app --network local
Schema changes (2 total):
  ✅  User.email: New field with default='unknown@example.com' — auto-migratable
  ⚠️   User.age: Type changed Integer → Float — requires migrate()
Upgrade will be REJECTED: 1 breaking change(s) without migrate().
```

**Step 4 — Add a `migrate()` method (fix the breaking change):**

```python
class User(Entity):
    __db__ = db
    __version__ = 2
    name = String(default="")
    age = Float(default=0.0)
    email = String(default="unknown@example.com")

    @classmethod
    def migrate(cls, data: dict, old_version: int, new_version: int) -> dict:
        if old_version < 2:
            data["age"] = float(data.get("age", 0))
        return data
```

```
$ basilisk check-upgrade --canister my_app --network local
Schema changes (3 total):
  ✅  User: Version 1 → 2
  ✅  User.email: New field with default='unknown@example.com' — auto-migratable
  ⚠️   User.age: Type changed Integer → Float — requires migrate()
All breaking changes have migrate(). Safe to upgrade.
```

### Verbose Mode

Use `--verbose` (or `-v`) to print the full schemas and save them to files for manual comparison:

```
$ basilisk check-upgrade --canister my_app --network local -v
--- On-chain schema (.basilisk/schemas/on_chain_schema.json) ---
{ ... }

--- Local schema (.basilisk/schemas/local_schema.json) ---
{ ... }

Schemas written to .basilisk/schemas/ for manual comparison.
  diff .basilisk/schemas/on_chain_schema.json .basilisk/schemas/local_schema.json
```

Use `--output-dir <dir>` to write schema files to a custom location.

### On-chain Enforcement

Even if you skip `check-upgrade`, Basilisk auto-injects a safety net into `post_upgrade`: if a breaking change is deployed without `migrate()`, the IC traps and atomically rolls back — your canister stays on the old code with all data intact.

```
$ dfx deploy
...
🎉 Built canister my_app
...
Error: Failed to install wasm module to canister 'my_app'.
Caused by: Canister called `ic0.trap` with message:
  'Upgrade rejected: 1 breaking change(s) without migrate() method:
    - User.age: Type changed Integer → Float — requires migrate()'
```

The upgrade is rejected, the canister remains on the previous version, and no data is lost.

## Data Browsing (read-only)

Canisters with `__basilisk_features__ = ["browse"]` expose a `__browse__` query endpoint for instant, free, read-only data access:

```python
from ic_basilisk_toolkit.shell import canister_browse, canister_schema, canister_keys, canister_get

# Get the canister's data schema
schema = canister_schema("my_canister", network="ic")

# List keys in a stable map (paginated)
keys = canister_keys("my_canister", "users", network="ic")

# Read a single value
value = canister_get("my_canister", "users", "alice", network="ic")

# Generic browse with any action
result = canister_browse("items", "my_canister", network="ic", map="users", limit=50)
```

Unlike `__shell__` (which is an `@update` call requiring consensus and controller access), `__browse__` is a `@query` — instant response, no cycles cost, and public by default.

> **Security note:** The `sshd` command starts a local development proxy that accepts any password. It is intended for local use only — do not expose it on a public network without adding proper authentication.

## Dependencies

- [ic-basilisk](https://github.com/smart-social-contracts/basilisk) — CDK (types, decorators, `ic.*` API)
- [ic-python-db](https://github.com/smart-social-contracts/ic-python-db) — Persistent entity ORM
- [ic-python-logging](https://github.com/smart-social-contracts/ic-python-logging) — Structured logging


## Disclaimer

This software is in alpha and may have unknown security vulnerabilities. It has not undergone an independent security audit. Use at your own risk — see the Basilisk [disclaimer](https://github.com/smart-social-contracts/basilisk#disclaimer) for details.

## License

MIT — see [LICENSE](LICENSE).
