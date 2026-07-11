"""Hugo development server management."""

import subprocess
import time
import os
import signal
import socket
import re
from pathlib import Path


def find_free_port(start: int = 1313) -> int:
    """Find an available port starting from `start`."""
    port = start
    while port < start + 100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
            port += 1
    raise RuntimeError("No free port found")


def check_hugo() -> str:
    """Verify Hugo is installed and return its version string."""
    try:
        result = subprocess.run(["hugo", "version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        raise RuntimeError("Hugo not found. Install with: brew install hugo")
    except Exception as e:
        raise RuntimeError(f"Hugo check failed: {e}")


def start_hugo_server(
    project_path: str,
    port: int = 0,
    base_url: str = None
) -> tuple[subprocess.Popen, int]:
    """Start `hugo server` on a (possibly random) port.

    Returns (process, actual_port).
    """
    hugo_dir = _find_hugo_dir(project_path)
    if not hugo_dir:
        raise FileNotFoundError(f"No Hugo project found in {project_path}")

    # Check hugo first
    version = check_hugo()
    print(f"   Hugo: {version.split('v')[1] if 'v' in version else version}")

    # Auto-select port if 0 or occupied
    if port == 0:
        port = find_free_port()
    else:
        # Verify the specified port is free
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()
        if result == 0:
            port = find_free_port(port + 1)

    cmd = [
        "hugo", "server",
        "--bind", "127.0.0.1",
        "--port", str(port),
        "--disableFastRender",
    ]
    if base_url:
        cmd.extend(["--baseURL", base_url])
    else:
        cmd.extend(["--baseURL", f"http://127.0.0.1:{port}"])

    print(f"   Starting Hugo server on 127.0.0.1:{port}...")

    proc = subprocess.Popen(
        cmd,
        cwd=str(hugo_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid,
    )

    # Wait for server to be ready by scanning stdout for "Web Server is available"
    start_time = time.time()
    timeout = 30
    while time.time() - start_time < timeout:
        if proc.poll() is not None:
            raise RuntimeError(f"Hugo server exited prematurely (code {proc.returncode})")

        # Check port is listening
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()
        if result == 0:
            print(f"   Hugo server ready at http://127.0.0.1:{port}")
            return proc, port

        time.sleep(0.5)

    # Timeout
    stop_hugo_server(proc)
    raise RuntimeError(f"Hugo server didn't start on port {port} within {timeout}s")


def stop_hugo_server(proc: subprocess.Popen) -> None:
    """Stop the Hugo server process."""
    if proc and proc.poll() is None:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            proc.wait(timeout=5)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except ProcessLookupError:
                pass


def build_hugo(project_path: str, output_dir: str = None) -> Path:
    """Build the Hugo site and return the public/ directory path."""
    hugo_dir = _find_hugo_dir(project_path)
    if not hugo_dir:
        raise FileNotFoundError(f"No Hugo project found in {project_path}")

    cmd = ["hugo"]
    if output_dir:
        cmd.extend(["--destination", output_dir])

    result = subprocess.run(cmd, cwd=str(hugo_dir), capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"Hugo build failed:\n{result.stderr}")

    # Find public dir
    public_dir = hugo_dir / "public"
    if output_dir:
        public_dir = Path(output_dir)

    if not public_dir.exists():
        # Try parent
        public_dir = hugo_dir.parent / "hugo-site" / "public"

    return public_dir.resolve()


def _find_hugo_dir(project_path: str) -> Path | None:
    """Find the hugo-site/ directory under project_path."""
    base = Path(project_path).resolve()
    candidates = [
        base / "hugo-site",
        base,
    ]
    for c in candidates:
        if (c / "config.toml").exists() or (c / "config.yaml").exists() or (c / "hugo.toml").exists():
            return c
    return None
