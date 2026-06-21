# SSH Key Setup in NVIDIA Container

## Quick Start

```bash
# 1. Generate key (one-time)
mkdir -p ~/.ssh
ssh-keygen -t ed25519 -C "hermes-docker-nvidia" -f ~/.ssh/id_ed25519 -N ""

# 2. Add public key to GitHub: github.com/settings/keys
# Key fingerprint: SHA256:OwABsi6upN34A5hoi2542vCrYmy4BwxNUgxBIesr01Y

# 3. Each container session, load key before git push:
eval $(ssh-agent) && ssh-add ~/.ssh/id_ed25519

# 4. Test:
ssh -T git@github.com
# Expected: "Hi angelife! You've successfully authenticated..."
```

## Why ssh-agent Is Required

The SSH key exists but SSH won't use it without an agent. Without `ssh-agent`, you get:

```
git@github.com: Permission denied (publickey).
```

Even though the key is correct.

## Key Properties

- Type: ED25519
- Location: `~/.ssh/id_ed25519` (private), `~/.ssh/id_ed25519.pub` (public)
- Fingerprint: `SHA256:OwABsi6upN34A5hoi2542vCrYmy4BwxNUgxBIesr01Y`
- Comment: `hermes-docker-nvidia`
- No passphrase (empty `-N ""`)

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Permission denied (publickey)` | Key not loaded | `eval $(ssh-agent) && ssh-add` |
| `Could not open a connection to your authentication agent` | ssh-agent not running | `eval $(ssh-agent)` first |
| Key works but git push still fails | Wrong key offered | Check `ssh -vT git@github.com` |

## Security Note

- Private key has no passphrase — protect it accordingly
- Do NOT log the private key content
- Public key is safe to share (it's meant for GitHub)

## Container Restart

The key persists in `~/.ssh/` but `ssh-agent` is not running by default. Must reload each session:

```bash
eval $(ssh-agent) && ssh-add ~/.ssh/id_ed25519
```

## Git Push After Key Loaded

```bash
cd /repo
git add <files> && git commit -m "..." && git tag v0.X.Y
git push origin master && git push origin v0.X.Y
```

Both master branch and tag push require the key loaded.