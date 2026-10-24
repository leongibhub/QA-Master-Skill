"""Launch the bounded delivery proof outside the caller's short command window."""
from __future__ import annotations

from pathlib import Path
import os
import subprocess
import sys


EVIDENCE = Path(__file__).resolve().parent
partial = EVIDENCE / "delivery-commands.json"
if partial.exists():
    partial.replace(EVIDENCE / "delivery-commands-interrupted-foreground.json")
stdout = (EVIDENCE / "delivery-driver-stdout.bin").open("wb")
stderr = (EVIDENCE / "delivery-driver-stderr.bin").open("wb")
flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
child = subprocess.Popen([sys.executable, str(EVIDENCE / "run_final_delivery.py")], cwd=EVIDENCE.parents[4],
                         stdout=stdout, stderr=stderr, creationflags=flags)
(EVIDENCE / "delivery-driver-pid.txt").write_text(f"{child.pid}\n", encoding="ascii")
print(child.pid)
