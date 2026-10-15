"""Regression coverage for BUG-013: lock-sentinel initialization races."""
from __future__ import annotations

import tempfile
import threading
import unittest
from pathlib import Path

from qa_master.application import CampaignApplicationService
from qa_master.state_store import StateConflictError


class StateLockInitializationRaceTests(unittest.TestCase):
    def test_empty_lock_file_parallel_initialization_has_one_winner(self):
        """An existing empty lock file must not make a losing initializer fail I/O."""
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "campaign.json"
            lock_path = state_path.with_name(state_path.name + ".lock")
            lock_path.touch()
            barrier = threading.Barrier(2)
            outcomes: list[str] = []
            unexpected: list[BaseException] = []

            def initialize(project: str) -> None:
                barrier.wait()
                try:
                    CampaignApplicationService.initialize(state_path, project)
                except StateConflictError:
                    outcomes.append("conflict")
                except Exception as error:  # Preserve unexpected lock failures for the assertion.
                    unexpected.append(error)
                else:
                    outcomes.append("created")

            workers = [threading.Thread(target=initialize, args=(project,))
                       for project in ("left", "right")]
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join()

            self.assertEqual(unexpected, [])
            self.assertEqual(sorted(outcomes), ["conflict", "created"])
            self.assertEqual(lock_path.read_bytes(), b"0")
            self.assertFalse(list(state_path.parent.glob(".qa-master-state-*.json")))


if __name__ == "__main__":
    unittest.main()
