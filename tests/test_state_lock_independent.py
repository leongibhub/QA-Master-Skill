"""Independent concurrency checks for the local revisioned state lock."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest

from qa_master.state_store import StateConflictError, load_document, save_document


_CHILD = r'''
import json
from pathlib import Path
import sys
import time
from qa_master.state_store import StateConflictError, save_document

state, ready, gate, value = map(Path, sys.argv[1:5])
ready.write_text("ready", encoding="ascii")
deadline = time.monotonic() + 15
while not gate.exists():
    if time.monotonic() >= deadline:
        raise SystemExit("start gate timeout")
    time.sleep(0.005)
try:
    result = save_document(state, {"winner": value.name}, expected_revision=0,
                           create_if_absent=True)
    print(json.dumps({"outcome": "saved", "revision": result["revision"]}))
except StateConflictError:
    print(json.dumps({"outcome": "conflict"}))
'''


class IndependentStateLockTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="qa-master-state-lock-independent-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def _assert_complete_winner(self, path: Path):
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
        self.assertEqual(value["revision"], 1)
        self.assertIn(value["winner"], {"left", "right"})
        self.assertEqual(load_document(path), value)
        self.assertFalse(list(path.parent.glob(".qa-master-state-*.json")))
        self.assertEqual(path.with_name(path.name + ".lock").read_bytes(), b"0")

    def test_zero_byte_lock_concurrent_threads_yield_one_winner_and_conflict(self):
        for number in range(3):
            with self.subTest(round=number):
                path = self.root / f"threads-{number}.json"
                lock = path.with_name(path.name + ".lock")
                lock.write_bytes(b"")
                gate = threading.Barrier(2)
                outcomes = []

                def writer(value):
                    gate.wait(timeout=10)
                    try:
                        save_document(path, {"winner": value}, expected_revision=0,
                                      create_if_absent=True)
                        outcomes.append(("saved", value))
                    except StateConflictError:
                        outcomes.append(("conflict", value))
                    except BaseException as error:  # capture infrastructure failures as a test failure
                        outcomes.append((type(error).__name__, value))

                threads = [threading.Thread(target=writer, args=(value,)) for value in ("left", "right")]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join(timeout=15)
                self.assertFalse(any(thread.is_alive() for thread in threads))
                self.assertCountEqual([kind for kind, _ in outcomes], ["saved", "conflict"])
                self._assert_complete_winner(path)

    def test_zero_byte_lock_concurrent_processes_and_settled_reuse(self):
        for number in range(3):
            with self.subTest(round=number):
                path = self.root / f"processes-{number}.json"
                path.with_name(path.name + ".lock").write_bytes(b"")
                gate = self.root / f"go-{number}"
                processes = []
                for value in ("left", "right"):
                    ready = self.root / f"ready-{number}-{value}"
                    process = subprocess.Popen(
                        [sys.executable, "-X", "utf8", "-c", _CHILD, str(path), str(ready), str(gate), value],
                        cwd=Path(__file__).resolve().parents[1],
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    processes.append((process, ready))
                deadline = time.monotonic() + 15
                while not all(ready.exists() for _, ready in processes):
                    if time.monotonic() >= deadline:
                        self.fail("child processes did not reach the shared start gate")
                    time.sleep(0.01)
                gate.write_text("go", encoding="ascii")
                outcomes = []
                for process, _ in processes:
                    stdout, stderr = process.communicate(timeout=20)
                    self.assertEqual(process.returncode, 0, stderr)
                    outcomes.append(json.loads(stdout)["outcome"])
                self.assertCountEqual(outcomes, ["saved", "conflict"])
                self._assert_complete_winner(path)
                settled = save_document(path, {"winner": "settled"}, expected_revision=1)
                self.assertEqual(settled["revision"], 2)
                self.assertEqual(load_document(path)["winner"], "settled")


if __name__ == "__main__":
    unittest.main()
