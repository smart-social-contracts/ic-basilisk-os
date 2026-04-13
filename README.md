# ic-basilisk-toolkit

**Basilisk Toolkit** — A set of ready-made tools on top of the[Basilisk](https://github.com/smart-social-contracts/basilisk) CDK for IC Python canisters.

**Live demo:** [https://ic-basilisk.tech/](https://ic-basilisk.tech/).

## Overview

| Service | Description | Examples |
|---|---|---|
| **Task Management** | Create, schedule, and run background tasks | `%task create heartbeat every 60s --code "print('alive')"` / `Task(name="sync")` |
| **Wallet** | ICRC-1 token registry, transfers, balance tracking | `%wallet balance` / `Wallet.transfer(token, to, amount)` |
| **Encryption** | vetKeys + per-principal envelopes + groups | `%crypto encrypt "secret"` / `CryptoService.encrypt(data, recipients)` |
| **FX** | Exchange rate queries via the IC XRC canister | `%fx ICP/USD` / `FXService.get_rate("ICP", "USD")` |
| **Entities** | Persistent ORM via [ic-python-db](https://github.com/smart-social-contracts/ic-python-db) | `%db list User` / `User(name="alice").save()` |
| **Logging** | Structured logging via [ic-python-logging](https://github.com/smart-social-contracts/ic-python-logging) | `logger.info("msg")` |
| **HTTP Fetch** | Download a URL into the canister filesystem | `%wget https://example.com /data.txt` / `yield from wget(url, dest)` |
| **File Transfer** | Move files between local machine and canister | `%get /app.py` / `%put script.py` |
| **Interactive Shell** | REPL for live canister interaction | `basilisk-toolkit shell --canister my_app` |
| **SFTP** | Browse and edit canister filesystem over SSH | `basilisk-toolkit sshd --canister my_app` |

Type `:help` inside the shell for full command reference, or see the [tip_jar template](templates/tip_jar) for a working example project.

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


## Dependencies

- [ic-basilisk](https://github.com/smart-social-contracts/basilisk) — CDK (types, decorators, `ic.*` API)
- [ic-python-db](https://github.com/smart-social-contracts/ic-python-db) — Persistent entity ORM
- [ic-python-logging](https://github.com/smart-social-contracts/ic-python-logging) — Structured logging


## License

MIT — see [LICENSE](LICENSE).
