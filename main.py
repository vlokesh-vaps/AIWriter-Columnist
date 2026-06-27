"""
AI Newsroom Platform — Local Development Entry Point.

Starts all three microservices in parallel subprocesses for local testing.
Each service runs its own uvicorn server on its designated port:

  • Research Service      → http://localhost:8001
  • AI Writer Service     → http://localhost:8002
  • Fact-Check Service    → http://localhost:8003
  • AI Columnist Service  → http://localhost:8005

Usage:
    python main.py

NOTE: This is for LOCAL DEVELOPMENT / TESTING ONLY.
      Production deployment uses Docker (docker-compose up --build).
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Dict, List

# ── Configuration ─────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent

SERVICES = [
    {
        "name": "Research Service",
        "module": "app.main:app",
        "port": 8004,
        "cwd": str(PROJECT_ROOT / "research_service"),
        # Both the service dir (for bare `from app.`) and project root
        # (for `from shared.` and `from research_service.app.`) imports.
        "pythonpath": os.pathsep.join([
            str(PROJECT_ROOT / "research_service"),
            str(PROJECT_ROOT),
        ]),
    },
    {
        "name": "AI Writer Service",
        "module": "app.main:app",
        "port": 8002,
        "cwd": str(PROJECT_ROOT / "ai_writer_service"),
        "pythonpath": os.pathsep.join([
            str(PROJECT_ROOT / "ai_writer_service"),
            str(PROJECT_ROOT),
        ]),
    },
    {
        "name": "Fact-Check Service",
        "module": "app.main:app",
        "port": 8003,
        "cwd": str(PROJECT_ROOT / "fact_check_service"),
        "pythonpath": os.pathsep.join([
            str(PROJECT_ROOT / "fact_check_service"),
            str(PROJECT_ROOT),
        ]),
    },
    {
        "name": "AI Columnist Service",
        "module": "app.main:app",
        "port": 8005,
        "cwd": str(PROJECT_ROOT / "ai_columnist_service"),
        "pythonpath": os.pathsep.join([
            str(PROJECT_ROOT / "ai_columnist_service"),
            str(PROJECT_ROOT),
        ]),
    },
]

# ── Colour helpers (ANSI — works in modern terminals / Windows 10+) ──────

COLORS = {
    "Research Service":      "\033[96m",   # Cyan
    "AI Writer Service":     "\033[93m",   # Yellow
    "Fact-Check Service":    "\033[95m",   # Magenta
    "AI Columnist Service":  "\033[94m",   # Blue
}
RESET = "\033[0m"
BOLD  = "\033[1m"
GREEN = "\033[92m"
RED   = "\033[91m"


def _banner() -> None:
    """Print startup banner with service URLs."""
    print(f"""
{BOLD}{'=' * 62}
   AI Newsroom Platform -- Local Development Server
{'=' * 62}{RESET}
""")
    for svc in SERVICES:
        color = COLORS.get(svc["name"], "")
        print(f"  {color}> {svc['name']:.<30s} http://localhost:{svc['port']}{RESET}")
    print(f"""
  {GREEN}[docs]   Swagger docs at /docs on each port{RESET}
  {GREEN}[health] Health checks at /health on each port{RESET}

  {BOLD}Press Ctrl+C to stop all services{RESET}
{'-' * 62}
""")


# ── Subprocess management ────────────────────────────────────────────────

def _build_env(pythonpath: str) -> Dict[str, str]:
    """Build environment dict with PYTHONPATH injected."""
    env = os.environ.copy()
    env["PYTHONPATH"] = pythonpath
    return env


def _start_services() -> List[subprocess.Popen]:
    """Start each service as a uvicorn subprocess."""
    python = sys.executable
    processes: List[subprocess.Popen] = []

    for svc in SERVICES:
        cmd = [
            python, "-m", "uvicorn",
            svc["module"],
            "--host", "0.0.0.0",
            "--port", str(svc["port"]),
            "--reload",
            "--log-level", "info",
        ]

        color = COLORS.get(svc["name"], "")
        print(f"  {color}>> Starting {svc['name']} on port {svc['port']}...{RESET}")

        proc = subprocess.Popen(
            cmd,
            cwd=svc["cwd"],
            env=_build_env(svc["pythonpath"]),
        )
        processes.append(proc)

    return processes


def _stop_services(processes: List[subprocess.Popen]) -> None:
    """Gracefully terminate all service processes."""
    print(f"\n{BOLD}{RED}[STOP] Shutting down all services...{RESET}")
    for proc in processes:
        if proc.poll() is None:  # Still running
            proc.terminate()

    # Wait up to 5 seconds for graceful shutdown
    deadline = time.time() + 5
    for proc in processes:
        remaining = max(0, deadline - time.time())
        try:
            proc.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            proc.kill()

    print(f"{GREEN}[OK] All services stopped.{RESET}\n")


# ── Main ─────────────────────────────────────────────────────────────────

def main() -> None:
    """Entry point: start all services and wait for Ctrl+C."""

    # Pre-flight check: ensure .env exists
    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        env_example = PROJECT_ROOT / ".env.example"
        if env_example.exists():
            print(
                f"{RED}[WARNING] No .env file found!{RESET}\n"
                f"   Copy the example and configure it:\n\n"
                f"     copy .env.example .env\n"
            )
        else:
            print(f"{RED}[WARNING] No .env file found! Create one with your settings.{RESET}")
        sys.exit(1)

    _banner()

    processes = _start_services()

    # Handle Ctrl+C gracefully
    try:
        # Wait for any process to exit (or Ctrl+C)
        while True:
            for i, proc in enumerate(processes):
                retcode = proc.poll()
                if retcode is not None:
                    svc_name = SERVICES[i]["name"]
                    color = COLORS.get(svc_name, "")
                    print(
                        f"\n{color}{RED}[CRASH] {svc_name} exited with code {retcode}{RESET}"
                    )
                    # Stop all if one crashes
                    _stop_services(processes)
                    sys.exit(retcode or 1)
            time.sleep(1)
    except KeyboardInterrupt:
        _stop_services(processes)


if __name__ == "__main__":
    main()
