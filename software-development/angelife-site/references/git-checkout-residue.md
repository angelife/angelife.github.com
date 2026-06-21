# git checkout 残留文件检测与清理（v0.7.22）

## 症状

- `git status --short` 显示 clean，但 Hugo build 结果与 live site 不符
- 本地 build 显示 44 篇，live site 只有 7 篇
- `git log -n 3 --oneline` 显示 HEAD 已是最新 commit，但 build 用的是旧文件

## 根因

在 detached HEAD 状态执行 `git checkout {旧commit}` 时：
- **若磁盘文件与目标 commit 内容不同，`git checkout` 不会覆写磁盘**
- git 切换到新 commit，但磁盘保留旧文件
- `git status` 仍显示 clean（因为 git 认为工作树与 HEAD 一致）

## 正确诊断（Python）

```python
import subprocess, glob, os

def check_disk_vs_head(base_path, subdir):
    os.chdir(base_path)
    
    # 获取 HEAD 中的 .md 文件列表（权威数据）
    r = subprocess.run(["git", "ls-tree", "-r", "HEAD", "--", subdir],
                      capture_output=True, text=True)
    head_files = set()
    for line in r.stdout.strip().split('\n'):
        if line and '.md' in line:
            parts = line.split('\t', 1)
            if len(parts) == 2:
                head_files.add(parts[1])  # 路径不含引号
    
    # 获取磁盘实际 .md 文件
    disk_files = set(glob.glob(f"{subdir}/**/*.md", recursive=True))
    
    extra = disk_files - head_files
    missing = head_files - disk_files
    
    return {
        'head_count': len(head_files),
        'disk_count': len(disk_files),
        'extra_files': sorted(extra),   # 残留：磁盘有 HEAD 无
        'missing_files': sorted(missing) # 缺失：HEAD 有磁盘无
    }

result = check_disk_vs_head("/opt/data/angelife-clone/hugo-site", "content/posts")
print(f"HEAD: {result['head_count']}, 磁盘: {result['disk_count']}")
if result['extra_files']:
    print(f"残留文件: {len(result['extra_files'])}")
    for f in result['extra_files'][:5]:
        print(f"  DELETE: {f}")
```

## 清理步骤

1. 用上方脚本找出残留文件
2. 删除：`os.remove(f) for f in extra_files`
3. 验证删除后磁盘 vs HEAD 对齐
4. `git add -A`（含删除操作）
5. `git commit -m "fix: remove git checkout residue, restore disk=HEAD sync"`
6. `git push origin master`

## 预防

`git checkout` 后立即执行：
```bash
git status --short
```
若有 "D ..."（deleted in work tree）变更，说明磁盘与 HEAD 已脱节，立即清理。

## 本次记录（v0.7.22）

| 目录 | 残留文件数 | HEAD 文件数 | 清理操作 |
|------|-----------|------------|---------|
| content/posts/ | 70 个残留 | 17 个 | 已删除 + commit `1dcf332` |
| content/series/ | 31 个残留 | 72 个 | 已删除 + commit `1dcf332` |

commit: `1dcf332` (master)