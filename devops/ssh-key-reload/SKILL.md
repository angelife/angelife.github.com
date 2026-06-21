---
name: ssh-key-reload
category: devops
description: Docker 新 session 后 GitHub push 失败，快速恢复 SSH key 加载
---

# SSH Key 加载（Docker 新 Session 恢复）

## 触发条件
GitHub push 报 `Permission denied (publickey)` 但 `~/.ssh/id_ed25519` 文件存在。

## 根因
Docker 新 session 后 ssh-agent 进程是新的，已加载的 key 丢失。

## 解决方案
```bash
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com  # 验证
```

## 验证
看到 `Hi angelife! You've successfully authenticated` 即成功。

## 状态
- Key 文件：`~/.ssh/id_ed25519`
- GitHub 已配置：`hermes-docker-nvidia`
- 指纹：`SHA256:OwABsi6upN34A5hoi2542vCrYmy4BwxNUgxBIesr01Y`

## Related

For general Docker environment troubleshooting (date verification, process management), see `references/docker-container-faq.md`.