import os
import subprocess
import signal
import sys
from pathlib import Path

from django.conf import settings


def _get_preferred_tts_python() -> str:
    configured = os.getenv('QWEN_TTS_PYTHON', '').strip()
    if configured:
        return configured
    current_python = sys.executable
    if current_python:
        return current_python
    candidate = Path('/home/user/anaconda3/envs/qwen3-tts/bin/python')
    if candidate.exists():
        return str(candidate)
    return sys.executable


def _get_tts_worker_lines(base_dir: Path) -> list[str]:
    result = subprocess.run(
        ['pgrep', '-af', 'manage.py process_tts_orders --watch'],
        cwd=base_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _worker_uses_python(line: str, expected_python: str) -> bool:
    return expected_python in line.split()


def _is_tts_worker_running(base_dir: Path, expected_python: str | None = None) -> bool:
    lines = _get_tts_worker_lines(base_dir)
    if expected_python is None:
        return bool(lines)
    return any(_worker_uses_python(line, expected_python) for line in lines)


def _get_tts_worker_pids(base_dir: Path) -> list[int]:
    pids = []
    for line in _get_tts_worker_lines(base_dir):
        try:
            pids.append(int(line.split()[0]))
        except (ValueError, IndexError):
            continue
    return pids


def stop_tts_worker() -> bool:
    base_dir = Path(settings.BASE_DIR)
    stopped = False
    for pid in _get_tts_worker_pids(base_dir):
        try:
            os.kill(pid, signal.SIGKILL)
            stopped = True
        except ProcessLookupError:
            continue
    return stopped


def trigger_tts_generation(order_no: str = '') -> None:
    if order_no is None:
        order_no = ''

    base_dir = Path(settings.BASE_DIR)
    stdout_path = base_dir / 'tts_worker.log'
    stderr_path = base_dir / 'tts_worker_error.log'

    qwen_python = _get_preferred_tts_python()

    if _is_tts_worker_running(base_dir, expected_python=qwen_python):
        return

    if _is_tts_worker_running(base_dir):
        stop_tts_worker()

    cmd = [qwen_python, '-u', 'manage.py', 'process_tts_orders', '--watch']

    with open(stdout_path, 'ab') as stdout_handle, open(stderr_path, 'ab') as stderr_handle:
        subprocess.Popen(
            cmd,
            cwd=base_dir,
            stdout=stdout_handle,
            stderr=stderr_handle,
            start_new_session=True,
            env=os.environ.copy(),
        )
