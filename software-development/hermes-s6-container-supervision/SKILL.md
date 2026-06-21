---
name: hermes-s6-container-supervision
description: Modify, debug, or extend the s6-overlay supervision tree inside the Hermes Agent Docker image — adding new services, debugging profile gateways, understanding the Architecture B main-program pattern.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [docker, s6, supervision, gateway, profiles]
    related_skills: [hermes-agent, hermes-agent-dev]
---

# Hermes s6-overlay Container Supervision

## When to use this skill

Load this skill when you're working on:
- Adding or removing a static service in the Hermes Docker image (something that should be supervised at every container start, like the dashboard)
- Diagnosing why a per-profile gateway isn't starting, restarting, or surviving `docker restart`
- Understanding why the container's CMD is `/opt/hermes/docker/main-wrapper.sh` and how leading-dash args reach the user's program
- Modifying `cont-init.d` boot scripts (UID remap, volume seeding, profile reconciliation)
- Changing the rendered run-script for per-profile gateways (Phase 4)

If you're just running the Hermes Agent and want to use Docker, see `website/docs/user-guide/docker.md` instead.

## Architecture at a glance

```
/init                                  ← PID 1 (s6-overlay v3.2.3.0)
├── cont-init.d                        ← oneshot setup, runs as root
│   ├── 01-hermes-setup                ← docker/stage2-hook.sh
│   │   ├── UID/GID remap
│   │   ├── chown /opt/data
│   │   ├── chown /opt/data/profiles (every boot)
│   │   ├── seed .env / config.yaml / SOUL.md
│   │   └── skills_sync.py
│   └── 02-reconcile-profiles          ← hermes_cli.container_boot
│       ├── chown /run/service (hermes-writable for runtime register)
│       └── walk $HERMES_HOME/profiles/<name>/gateway_state.json
│           → recreate /run/service/gateway-<name>/
│           → auto-start only those with prior_state == "running"
│
├── s6-rc.d (static services, in /etc/s6-overlay/s6-rc.d/)
│   ├── main-hermes/run                ← exec sleep infinity (no-op slot)
│   └── dashboard/run                  ← if HERMES_DASHBOARD=1, runs `hermes dashboard`
│
├── /run/service (s6-svscan watches; tmpfs)
│   ├── gateway-coder/                 ← runtime-registered per-profile
│   │   ├── type        ("longrun")
│   │   ├── run         ("#!/command/with-contenv sh ... exec s6-setuidgid hermes hermes -p coder gateway run")
│   │   ├── down        (marker — present means "registered but don't auto-start")
│   │   └── log/run     (s6-log → $HERMES_HOME/logs/gateways/coder/current)
│   └── ...
│
└── CMD ("main program")               ← /opt/hermes/docker/main-wrapper.sh
    └── routes user args: bare exec | hermes subcommand | hermes (no args)
        — exec'd by /init with stdin/stdout/stderr inherited (TTY for --tui)
```

## Key files

| Path | Role |
|---|---|
| `Dockerfile` | s6-overlay install + cont-init.d wiring + `ENTRYPOINT ["/init", "/opt/hermes/docker/main-wrapper.sh"]` |
| `docker/stage2-hook.sh` | The "old entrypoint logic" — UID remap, chown, seed, skills sync. Runs as cont-init.d/01-hermes-setup. |
| `docker/cont-init.d/02-reconcile-profiles` | Calls `hermes_cli.container_boot` on every boot to restore profile gateway slots from the persistent volume. |
| `docker/main-wrapper.sh` | The container's CMD. Routes user args, drops to hermes via `s6-setuidgid`, exec's the chosen program. |
| `docker/s6-rc.d/main-hermes/run` | No-op `sleep infinity` — slot exists so the s6-rc user bundle is valid; main hermes runs as the CMD, not as a supervised service. |
| `docker/s6-rc.d/dashboard/run` | Conditional service — `exec sleep infinity` unless `HERMES_DASHBOARD` is truthy. |
| `docker/entrypoint.sh` | Back-compat shim that `exec`s the stage2 hook. External scripts that hard-coded the old entrypoint path still work. |
| `hermes_cli/service_manager.py` | `S6ServiceManager`: `register_profile_gateway`, `unregister_profile_gateway`, `start/stop/restart/is_running`, `list_profile_gateways`. |
| `hermes_cli/container_boot.py` | `reconcile_profile_gateways()` — walks persistent profiles, regenerates s6 slots, emits `container-boot.log`. |
| `hermes_cli/gateway.py::_dispatch_via_service_manager_if_s6` | Intercepts `hermes gateway start/stop/restart` and routes to s6 when running in a container. |

## Why Architecture B (CMD as main program, not s6-supervised)

The original plan (v1–v3) called for main hermes to run as a supervised s6-rc service. Two real s6-overlay v3 mechanics blocked that:

1. **cont-init.d scripts receive no CMD args** — so the stage2 hook can't parse `docker run <image> chat -q "hi"` to set `HERMES_ARGS` for a service `run` script to consume.
2. **`/run/s6/basedir/bin/halt` does NOT propagate the exit code** written to `/run/s6-linux-init-container-results/exitcode`. Containers always exit 143 (SIGTERM) regardless. Confirmed by skarnet (s6 author) in [issue #477](https://github.com/just-containers/s6-overlay/issues/477): _"if you want a container shutdown, you need to either have your CMD exit, or, if you have no CMD, write the container exit code you want then call halt"_.

So we use the s6-overlay-native CMD pattern: `ENTRYPOINT ["/init", "/opt/hermes/docker/main-wrapper.sh"]`. /init prepends the wrapper to user args automatically — so `docker run <image> --version` becomes `/init main-wrapper.sh --version`, and `--version` doesn't get intercepted by /init's POSIX shell. The wrapper drops to hermes via `s6-setuidgid`, then exec's the chosen program. The program's exit code becomes the container exit code, exactly matching the pre-s6 tini contract.

Trade-off: main hermes is unsupervised under s6. That exactly matches its behavior under tini (the pre-s6 image). Dashboard supervision is the only **new** guarantee — and per-profile gateways under `/run/service/` get full supervision.

## Quick recipes

### Verify s6 is PID 1 in a running container

```sh
docker exec <c> sh -c 'cat /proc/1/comm; readlink /proc/1/exe'
# Expect: s6-svscan or init / /package/admin/s6/.../s6-svscan
```

### Inspect a profile gateway service

```sh
# /command/ isn't on docker-exec PATH — use absolute path
docker exec <c> /command/s6-svstat /run/service/gateway-<name>
# "up (pid …) … seconds"            → running
# "down (exitcode N) … seconds, normally up, want up, …" → s6 wants it up but the process keeps exiting (crash loop)
# "down … normally up, ready …"     → user stopped it
```

### Bring a service up/down manually

```sh
docker exec <c> /command/s6-svc -u /run/service/gateway-<name>   # up
docker exec <c> /command/s6-svc -d /run/service/gateway-<name>   # down
docker exec <c> /command/s6-svc -t /run/service/gateway-<name>   # SIGTERM (restart)
```

### Watch the cont-init reconciler log

```sh
docker exec <c> tail -n 50 /opt/data/logs/container-boot.log
# 2026-05-21T06:18:05+0000 profile=coder prior_state=running action=started
# 2026-05-21T06:18:05+0000 profile=writer prior_state=stopped action=registered
```

### Add a new static service

1. Create `docker/s6-rc.d/<name>/type` with `longrun\n` and `docker/s6-rc.d/<name>/run` (use `#!/command/with-contenv sh` + `# shellcheck shell=sh`).
2. Drop to hermes via `s6-setuidgid hermes` at the top of run (unless you specifically need root).
3. Create empty `docker/s6-rc.d/<name>/dependencies.d/base` so it waits for the base bundle.
4. Create empty `docker/s6-rc.d/user/contents.d/<name>` so it joins the user bundle.
5. The `COPY docker/s6-rc.d/` in the Dockerfile picks it up automatically — no other changes.

### Change the per-profile gateway run command

Edit `S6ServiceManager._render_run_script` in `hermes_cli/service_manager.py`. The function is also called by `hermes_cli/container_boot.py::_register_service` during boot reconciliation, so it's the single source of truth. Update the corresponding assertion in `tests/hermes_cli/test_service_manager.py::test_s6_register_creates_service_dir_and_triggers_scan`.

### Run the docker test harness

```sh
docker build -t hermes-agent-harness:latest .
HERMES_TEST_IMAGE=hermes-agent-harness:latest scripts/run_tests.sh tests/docker/ -v
# Expect 19 passed, 0 xfailed against the s6 image
```

The harness lives in `tests/docker/` and skips when Docker isn't available. The per-test timeout is bumped to 180s (see `tests/docker/conftest.py`).

## Common pitfalls

### "command not found" via `docker exec`

`/command/` (where s6-overlay puts its binaries) is on PATH only for processes spawned by the supervision tree — services, cont-init.d, main-wrapper.sh. `docker exec <c> s6-svstat …` will fail with "command not found"; always use the absolute path `/command/s6-svstat`. The `hermes` binary works because the Dockerfile adds `/opt/hermes/.venv/bin` to the runtime `ENV PATH`.

### Legacy s6 (not s6-overlay v3) — `s6-svc` not on PATH

Some Hermes containers run a **legacy s6 layout** (not the v3 overlay): `/init` is `/package/admin/s6/command/s6-svscan`, supervise dirs are at `/run/service/<name>/supervise`, and the binary `s6-svc` is **NOT on PATH** (no `/command/s6-svc`). Detection:

```sh
ls /package/admin/s6/command/         # legacy layout
ls /command/                            # overlay v3 layout (would have s6-svc here)
which s6-svc                            # empty => legacy
```

When `s6-svc` is missing, you can still trigger a supervised restart by killing the gateway's child PID with `SIGTERM`. The `s6-supervise` process under `/run/service/<name>/supervise` notices the death and re-execs `run` within ~3-5 s; a new PID appears under `ps aux | grep "hermes gateway run"`. From `execute_code` (no `s6-svc`):

```python
import os, signal, time, subprocess
target = None
for ln in subprocess.run(['ps','aux'], capture_output=True, text=True).stdout.splitlines():
    if 'hermes gateway run' in ln:
        target = int(ln.split()[1]); break
os.kill(target, signal.SIGTERM)
time.sleep(8)  # s6 relaunch
```

Confirm with `/proc/net/tcp` for ESTABLISHED outbound to the platform IP range — Telegram long polling: typical egress `146.119.3.17:443` (or FB-Meta 31.13.95.0/24 like `31.13.95.33:443`). Outbound HTTPS connection from the new PID is the cheapest "polling is actually live" signal — faster and cheaper than exercising the full LLM round-trip.

### Profile directory ownership

The cont-init reconciler runs as hermes (`s6-setuidgid hermes` in `02-reconcile-profiles`). If a profile dir ends up root-owned (e.g. because `docker exec <c> hermes profile create …` ran as root by default), the reconciler can't read SOUL.md and fails with `PermissionError`. Mitigation: `stage2-hook.sh` chowns `$HERMES_HOME/profiles` to hermes on **every** boot, idempotently. Don't remove that block.

### Files written by `docker exec` are root-owned

`docker exec` defaults to root. Either pass `--user hermes` or rely on the stage2 chown sweep next reboot. Don't write files under `$HERMES_HOME/profiles/<name>/` as root manually — the next reconcile pass will sweep them but in-flight operations may hit perm errors.

### Service slot exists but s6-svstat says "s6-supervise not running"

The service directory is on tmpfs and was wiped on container restart. Either the cont-init reconciler hasn't run yet (give it a moment after `docker restart`) or it failed. Check `docker logs <c> | grep '02-reconcile'`.

### Gateway starts then immediately exits (`down (exitcode 1)` in svstat)

Most likely the profile has no model or auth configured. The service slot is correct — the gateway itself is unconfigured. Run `hermes -p <profile> setup` first. The s6 supervisor will restart it a few times, but **s6 has a built-in crash-loop throttle**: after N rapid crashes (default ~5 restarts within ~30 seconds), s6-supervise writes a `down` file and stops trying, leaving the service in "down" state. Once you fix the config, remove the `down` file and restart the service.

### Down file reappears after removal (s6 crash-loop throttle)

**Symptom:** You remove `/run/service/gateway-<name>/down`, start the service with `s6-svc -u`, and it appears to work — until later you find the `down` file is back and the gateway is stopped again. No error is logged in `gateway.log` (the process didn't crash — s6 simply gave up on it after the throttle).

**Root cause:** s6-supervise has a restart backoff mechanism. When a service exits with a non-zero code N times within a short window, s6-supervise assumes the service is in a crash loop and **automatically creates a `down` file** to stop attempting restarts. This is intentional — it prevents CPU spin on a service that keeps dying.

The container-boot reconciler at `/opt/data/logs/container-boot.log` shows which profiles were booted with which prior state. If a profile had `prior_state=running` but kept crashing, after the throttle triggers, the next boot's reconciler will find the `down` file and keep the service registered but stopped.

**Diagnosis:**

```sh
# Check s6-svstat status
/command/s6-svstat /run/service/gateway-default/
# Can show various states:
#   "up (pid 50676) 43 seconds"              → running normally
#   "down (exitcode 1) 16 seconds, want up"  → process exited, s6 will retry
#   "down (signal SIGTERM) 300 seconds"       → s6 gave up after throttle

# Check the cont-init reconciler history
cat /opt/data/logs/container-boot.log

# Check gateway.log for rapid crash pattern
grep -E "gateway run|SIGTERM|SIGKILL" /opt/data/logs/gateway.log | tail -20

# Check process history
ps aux | grep "hermes gateway" | grep -v grep
```

**Typical trigger sequence (observed):**
1. Gateway starts but has missing API key → 401 errors on every response → crashes
2. s6-supervise restarts it (3-5 times in quick succession)
3. All restarts fail within seconds → s6-supervise gives up → writes `down` file
4. The `down` file persists across container restarts (reconciler preserves it)
5. User removes `down` file and restarts → but if the root cause (missing API key) is still present → cycle repeats

**Fix:**
1. Identify **why** the gateway keeps crashing (missing API key, bad config, network issue)
2. Fix the root cause
3. Remove the `down` file and restart: `rm /run/service/gateway-<name>/down && /command/s6-svc -u /run/service/gateway-<name>/`
4. Verify with `s6-svstat` — should show "up" and survive longer than the throttle window

**Prevention:** The `down` file mechanism is working as designed — don't disable it. Instead, instrument the gateway to exit with code 0 when the error is transient vs. permanent, or add the missing `.env` variables to the run script (see "Gateway missing API keys" pitfall for the canonical fix).

### Gateway missing API keys / 401 errors (`with-contenv` strips `.env`)

**Symptom:** Gateway starts, connects to Telegram, receives messages, but every response attempt fails with `HTTP 401: Invalid API key`. The gateway log (`gateway.log`) shows `Provider: custom` and `AuthError` — but the same API key works when tested directly via `curl` from the CLI.

**Root cause:** The s6 `run` script uses `#!/command/with-contenv sh` as its shebang. `with-contenv` imports the container's *base* environment but **does not source** the Hermes `.env` file (`/opt/data/.env`). Even adding `. /opt/data/.env` in the script body doesn't reliably pass variables to the exec'd process — `with-contenv`'s environment isolation prevents the shell's sourced variables from reaching the child.

The config.yaml has `api_key: ''` (empty) for most providers because API keys are stored in `.env`. The gateway process therefore has no credential.

**Detection:**
```sh
# Check if the env var made it to the gateway process
cat /proc/<PID>/environ | tr '\0' '\n' | grep -i OPENCODE_ZEN
# Empty = the .env wasn't loaded
```

**Fix:** Extract the specific env var from `.env` inline in the run script, rather than sourcing the whole file:

```sh
#!/command/with-contenv sh
set -e
export HOME=/opt/data
cd /opt/data
. /opt/hermes/.venv/bin/activate
# Load API keys from .env — with-contenv doesn't inherit sourced env
export OPENCODE_ZEN_API_KEY=*** '^OPENCODE_ZEN_API_KEY=' /opt/data/.env | head -1 | cut -d= -f2- | sed "s/^['\"]//;s/['\"]$//")"
export HERMES_S6_SUPERVISED_CHILD=1
exec s6-setuidgid hermes hermes gateway run
```

For other providers, add similar export lines for their env vars (e.g. `NVIDIA_API_KEY`, `DEEPSEEK_API_KEY`, `XUNFEI_API_KEY`). The `grep | head | cut | sed` pipeline:
- Extracts the value after `=`
- Strips surrounding single or double quotes (`.env` files often quote values)

**Verification:**
```sh
/command/s6-svc -t /run/service/gateway-<name>/    # restart
sleep 3
ps aux | grep "hermes gateway"                      # get new PID
cat /proc/<PID>/environ | tr '\0' '\n' | grep OPENCODE_ZEN  # should show the key
# Then check gateway.log for 200 responses instead of 401
tail -f /opt/data/logs/gateway.log | grep "response ready"
```

**Note:** This is a one-time fix per service directory. After a container restart, the reconciler recreates the run script from the template, so the fix is durable only if applied to the template source (`hermes_cli/service_manager.py::_render_run_script`). For manual fixes on running containers, edit `/run/service/gateway-<name>/run` directly — it will persist until the next container restart.

### Gateway silently "running" but nothing works (run script replaced with `sleep infinity`)

Diagnostic: `ps aux | grep "hermes gateway"` shows NO process, but `s6-svstat` reports "up".

Root cause: The `run` script in the service directory was replaced with:
```sh
#!/bin/sh
exec sleep infinity
```

This can happen if `s6-setuidgid` was invoked incorrectly, or if a previous manual intervention (e.g., writing a down file then restarting) triggered a corruption of the run script. When the script is `sleep infinity`, s6-supervise considers the service "up and running" but no actual gateway process exists.

**Fix:**
1. Verify: `cat /run/service/gateway-<name>/run` — if you see `exec sleep infinity`, the run script is broken
2. **Rewrite the run script** with the correct content:
   ```sh
   #!/command/with-contenv sh
   set -e
   export HOME=/opt/data
   cd /opt/data
   . /opt/hermes/.venv/bin/activate
   export HERMES_S6_SUPERVISED_CHILD=1
   exec s6-setuidgid hermes hermes gateway run
   ```
3. **Restart the service**: `/command/s6-svc -t /run/service/gateway-<name>/`
4. Verify: `ps aux | grep "hermes gateway"` should show the process again

This is distinct from the "exits immediately" case because the service reports "up" not "down" — making it harder to spot.

### Reconciler skipped a profile

The reconciler keys on the **presence of `SOUL.md`** as the "real profile" marker. `hermes profile create` always seeds it. If a profile dir is missing SOUL.md (stray directory, partial restore, backup-in-progress), the reconciler skips it intentionally. Add a `SOUL.md` (even empty) to opt back in.

### "Help, the container exits 143!"

Check whether something is invoking `s6-svscanctl -t` or `/run/s6/basedir/bin/halt` — both cause /init to begin stage 3 shutdown but return 143 (SIGTERM) rather than the desired exit code. This was the Phase 2 architecture pivot from A to B. For container shutdown with a real exit code, you must let the CMD (main-wrapper.sh) exit normally; do **not** try to control exit from a finish script.

## Related skills

- `hermes-agent-dev`: General hermes-agent codebase navigation
- `hermes-tool-quirks`: Specific Hermes-tool workarounds (sed/grep/etc.) — load when debugging the s6 stack's interaction with hermes built-in tools.

## Reference files

- `references/process-memory-footprint.md` — Hermes Docker 容器进程布局与内存诊断：典型进程树、各实例（CMD CLI / gateway / 二次 CLI）的 RSS 范围、瘦身方案（仅 gateway / 仅 CLI / 冗余进程清理）、Hugo server 处理。
- `references/gateway-missing-dotenv-api-keys.md` — Configuring API keys in gateway run scripts.
- `references/docker-vision-capability.md` — Adding vision/inference capability to Docker.
