# ic-basilisk-os

**Basilisk OS** — Operating system services, interactive shell, and SFTP for [Basilisk](https://github.com/smart-social-contracts/basilisk) IC Python canisters.

## Overview

`ic-basilisk-os` provides POSIX-like abstractions on top of the Basilisk CDK:

- **Task/Process Management** — `Task`, `TaskStep`, `TaskSchedule`, `TaskManager`
- **Wallet** — ICRC-1 token registry, transfers, balance tracking, transaction sync
- **Encryption** — vetKeys + per-principal envelopes + groups (`CryptoService`)
- **FX** — Exchange rate queries via the IC XRC canister (`FXService`)
- **Entities** — Persistent ORM entities via [ic-python-db](https://github.com/smart-social-contracts/ic-python-db)
- **Logging** — Structured logging via [ic-python-logging](https://github.com/smart-social-contracts/ic-python-logging)
- **Interactive Shell** — REPL for live canister interaction (`basilisk-os shell`)
- **SFTP** — Browse and edit canister filesystem over SSH (`basilisk-os sshd`)

## Installation

```bash
pip install ic-basilisk-os
```

For shell/SFTP support (requires `asyncssh`):
```bash
pip install ic-basilisk-os[shell]
```

## CLI Usage

```
basilisk-os exec 'print("hello")'                    # Execute code on canister
basilisk-os shell --canister my_app --network ic      # Interactive shell
basilisk-os sshd --canister my_app --network ic       # SSH/SFTP server
```

## Canister-Side Usage

Inside your canister code:

```python
from ic_basilisk_os import Task, TaskStep, Wallet, CryptoService

# Create and schedule a task
task = Task(name="sync_balances")
TaskStep(task=task, name="fetch", code="wallet.refresh_all()")
```

## Dependencies

- [ic-basilisk](https://github.com/smart-social-contracts/basilisk) — CDK (types, decorators, `ic.*` API)
- [ic-python-db](https://github.com/smart-social-contracts/ic-python-db) — Persistent entity ORM
- [ic-python-logging](https://github.com/smart-social-contracts/ic-python-logging) — Structured logging

## Development

```bash
git clone https://github.com/smart-social-contracts/ic-basilisk-os.git
cd ic-basilisk-os
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
pytest tests/ -v
```

## License

MIT — see [LICENSE](LICENSE).
