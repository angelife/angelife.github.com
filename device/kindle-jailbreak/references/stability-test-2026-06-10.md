# Bridge Stability Test Results — 2026-06-10

## Root Cause Analysis: bridge_check timeout

### What happened
Every `process(wait, session_id=cmd_xxx)` returned `status: "not_found"` after `bridge_send.py` printed a cmd_id.

### Investigation trace
1. `bridge_check.py` — pure file ops, no subprocess. `check()` looks for `{cmd_id}_response.json` in outbox/.
2. `bridge_client.py` — 2s poll loop via `glob.glob(os.path.join(INBOX, "cmd_*.json"))`. After execution, writes `{cmd_id}_response.json` to OUTBOX, then deletes inbox file.
3. `bridge_send.py` — writes JSON to inbox/, prints cmd_id to stdout.
4. `process()` Hermes tool — **only** tracks processes started with `terminal(background=True)`. Bridge cmd_id is not a Hermes process.

### Timeline per task
```
t=0s    bridge_send.py → prints cmd_id
t=0.01  Hermes calls process(wait, cmd_id) → NOT_FOUND ❌
t=0-2s  bridge_client.py polling (may be sleeping)
t=2-4s  SSH execution (echo ~2.6s, hugo ~5.4s)
t=4-6s  bridge_client.py writes outbox
t=6s    bridge_check.py --all → SUCCESS ✅
```

### Correct pattern (verified)
```python
# Send
r = terminal("python3 bridge_send.py shell '...'")
cmd_id = r["output"].strip()

# Wait — bridge has 2s poll + SSH ~2-4s
time.sleep(6)

# Query
r = terminal("python3 bridge_check.py --all")
# Parse JSON from output
```

## Pressure Test Raw Data

```json
{
  "total_elapsed": 66.27,
  "tasks": 10,
  "avg_response": 6.42,
  "max_response": 6.52,
  "min_response": 6.35,
  "all_exit_zero": true,
  "duplicates": []
}
```

Per-task breakdown:
```
Task 0: t=6.42s result=YES
Task 1: t=6.35s result=YES
Task 2: t=6.52s result=YES
Task 3: t=6.36s result=YES
Task 4: t=6.39s result=YES
Task 5: t=6.44s result=YES
Task 6: t=6.41s result=YES
Task 7: t=6.45s result=YES
Task 8: t=6.51s result=YES
Task 9: t=6.35s result=YES
```

All 10 tasks returned `exit_code: 0` with valid stdout. No duplicates, no lost tasks.

## SSH PATH Investigation

```bash
# What SSH sees (non-login shell):
$ echo $PATH
/usr/bin:/bin:/usr/sbin:/sbin

# What login shell sees:
$ echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin
```

Mac's SSH non-login shell (`ssh user@host cmd`) doesn't source `.zshrc`/`.bashrc`.
`/usr/local/bin` is missing → `hugo`, `brew`, `go`, `npm` all fail with "command not found".

### Fix: export PATH in executor
In `bridge_client.py`, the `ssh_run()` function should prepend PATH:
```python
cmd_str = f"export PATH=$PATH:/usr/local/bin && {' && '.join(commands)}"
```

## Hugo Build Verification

```bash
$ export PATH=$PATH:/usr/local/bin && hugo version
hugo v0.147.4+extended+withdeploy darwin/amd64 BuildDate=2025-05-20T10:41:19Z VendorInfo=brew

$ cd ~/angelife.github.com/hugo-site && hugo --minify
Pages            | 402
Paginator pages  | 38
Non-page files   | 7
Static files     | 462
Processed images | 14
Aliases          | 18
Cleaned          | 0
Total in 5405 ms
```

Site path: `/Users/macos/angelife.github.com/hugo-site/hugo.toml`
Public output: `/Users/macos/angelife.github.com/hugo-site/public/`

## Mac Environment Details

- OS: Darwin 24.6.0 (x86_64)
- Shell: /bin/zsh
- SSH key: /opt/data/home/.ssh/id_ed25519 (comment: hermes-docker-nvidia)
- Bridge daemon: PID 5276, started 13:51
- Homebrew at: /usr/local (Intel Mac, not Apple Silicon)
- Hugo: installed via brew at /usr/local/Cellar/hugo/0.147.4