#!/usr/bin/env python3
"""
KOReader Deployment Validator
Compare zip contents vs deployed files on Kindle USB.
Detects missing extensions/ and launchpad/ files (known pitfall).

Usage:
    python3 validate-koreader-deploy.py <zip_path> <kindle_mount_path>

Example:
    python3 validate-koreader-deploy.py \
      /Volumes/Kindle/koreader-kindle-legacy-v2026.03.zip \
      /Volumes/Kindle/

Exit code: 0 = all files present, 1 = missing files
"""
import sys
import os
import zipfile
import subprocess


def get_deployed_files(kindle_path: str) -> set:
    """Get all files under koreader/, extensions/, launchpad/ on Kindle."""
    result = subprocess.run(
        ["find", os.path.join(kindle_path, "koreader"),
         os.path.join(kindle_path, "extensions"),
         os.path.join(kindle_path, "launchpad"),
         "-type", "f"],
        capture_output=True, text=True, timeout=30
    )
    files = set()
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line:
            rel = line.replace(kindle_path.rstrip("/") + "/", "")
            files.add(rel)
    return files


def get_deployed_file_count(kindle_path: str) -> int:
    """Count files in a directory by ls-based stat (faster than find for simple count)."""
    for dirname in ["koreader", "extensions", "launchpad"]:
        path = os.path.join(kindle_path, dirname)
        if os.path.isdir(path):
            result = subprocess.run(
                ["find", path, "-type", "f"],
                capture_output=True, text=True, timeout=30
            )
            count = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
            print(f"  {dirname}/: {count} files ({_human_size(path)})")
    return 0


def _human_size(path: str) -> str:
    """Quick du -sh for a path, or fallback."""
    try:
        result = subprocess.run(
            ["du", "-sh", path],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip().split("\t")[0] if result.stdout.strip() else "?"
    except Exception:
        return "?"


def main():
    if len(sys.argv) < 3:
        print("Usage: validate-koreader-deploy.py <zip_path> <kindle_mount_path>")
        sys.exit(1)

    zip_path = sys.argv[1]
    kindle_path = sys.argv[2].rstrip("/") + "/"

    if not os.path.exists(zip_path):
        print(f"❌ ZIP not found: {zip_path}")
        sys.exit(1)
    if not os.path.isdir(kindle_path):
        print(f"❌ Kindle mount not found: {kindle_path}")
        sys.exit(1)

    print("====== KOReader 部署完整性检查 ======")
    print(f"ZIP: {zip_path}")
    print(f"Kindle: {kindle_path}")
    print()

    # Get zip file list
    z = zipfile.ZipFile(zip_path)
    zip_files = set(z.namelist())
    print(f"ZIP 文件数: {len(zip_files)}")

    # Summary counts per directory
    print()
    print("--- 部署路径文件分布 ---")
    get_deployed_file_count(kindle_path)

    # Check known-critical files
    print()
    print("--- 关键文件检查 ---")
    critical_files = [
        "koreader/koreader.sh",
        "koreader/luajit",
        "koreader/fbink",
        "launchpad/koreader.ini",
        "extensions/koreader/menu.json",
        "extensions/koreader/bin/koreader-ext.sh",
    ]
    missing_critical = []
    for f in critical_files:
        full = os.path.join(kindle_path, f)
        if os.path.exists(full):
            size = os.path.getsize(full)
            mode = oct(os.stat(full).st_mode)[-3:]
            print(f"  ✅ {f} ({size}B, {mode})")
        else:
            print(f"  ❌ {f} — 缺失!")
            missing_critical.append(f)

    # Full comparison
    print()
    deployed = get_deployed_files(kindle_path)
    print(f"Kindle 文件数: {len(deployed)}")

    missing = sorted(zip_files - deployed)
    extra = sorted(deployed - zip_files)

    if missing:
        print(f"\n❌ 缺失文件 ({len(missing)}):")
        for f in missing:
            print(f"  - {f}")
    else:
        print("\n✅ 所有 ZIP 文件已部署")

    if extra:
        print(f"\n⚠️ 额外文件（ZIP 中不存在）({len(extra)}):")
        for f in extra:
            print(f"  - {f}")

    print()
    print(f"汇总: zip={len(zip_files)}, deployed={len(deployed)}, "
          f"missing={len(missing)}, extra={len(extra)}")

    if missing_critical:
        print()
        print(f"❌ 存在 {len(missing_critical)} 个关键文件缺失！")
        print("从 ZIP 单独提取 extensions/ + launchpad/:")
        print(f"  python3 -c \"import zipfile; z = zipfile.ZipFile('{zip_path}'); "
              "[z.extract(f, '/tmp/koreader_fix/') for f in z.namelist() if f.startswith('extensions/') or f.startswith('launchpad/')]\"")
        print("  cp -a /tmp/koreader_fix/extensions/koreader /Volumes/Kindle/extensions/")
        print("  cp -a /tmp/koreader_fix/launchpad/koreader.ini /Volumes/Kindle/launchpad/")

    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()