"""Behavior tests for scripts/control.py (STOP, claims, dispatch readiness, overlap).

Run from the repo root:  python3 -m unittest discover -s tests -v
Each test builds a scratch repo layout, so the real boards are never read.
"""
import os, shutil, subprocess, sys, tempfile, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "scripts", "control.py")

BOARD = """# Development Board: Demo

## Project routing

- Project ID: {pid}
- Target repository: Sgilmore186/demo
- Target branch: main
- Activation: {activation}

## Run claim

- Owner: {owner}
- Run ID: {run}
- Claimed/renewed UTC: {renewed}
- Starting target commit: none

## Ordered phases

### P1 - Phase one

- Objective: test

#### P1/1 - First task

- **Assignee:** claude-code
- **Status:** {s1}
- **Touches:** src/game/, docs/notes.md
- **Claim:** none

#### P1/2 - Second task

- **Assignee:** codex
- **Status:** pending
- **Touches:** src/game/rules.js
- **Claim:** none

#### P1/3 - Third task

- **Assignee:** any
- **Status:** pending
- **Touches:** tests/*.mjs
- **Claim:** none
"""


class ControlTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir)

    def board(self, pid="demo", activation="active", owner="none", run="none", renewed="none", s1="pending"):
        path = os.path.join(self.dir, "development", pid)
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "BOARD.md"), "w", encoding="utf-8") as f:
            f.write(BOARD.format(pid=pid, activation=activation, owner=owner, run=run, renewed=renewed, s1=s1))

    def run_cli(self, *args):
        env = dict(os.environ, PM_ROOT=self.dir)
        p = subprocess.run([sys.executable, SCRIPT] + list(args), env=env, capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr

    def stop(self, text="Seph paused all agents"):
        with open(os.path.join(self.dir, "STOP"), "w", encoding="utf-8") as f:
            f.write(text + "\n")

    # status
    def test_status_runs_without_stop_file(self):
        self.assertEqual(self.run_cli("status"), (0, "RUN\n"))

    def test_status_reports_stop_and_reason(self):
        self.stop()
        code, out = self.run_cli("status")
        self.assertEqual(code, 3)
        self.assertIn("STOPPED: Seph paused all agents", out)

    def test_empty_stop_file_still_stops(self):
        self.stop("")
        code, out = self.run_cli("status")
        self.assertEqual(code, 3)
        self.assertIn("no reason given", out)

    # ready
    def test_ready_when_active_and_unclaimed(self):
        self.board()
        self.assertEqual(self.run_cli("ready", "demo")[0], 0)

    def test_stop_blocks_ready_even_when_free(self):
        self.board(); self.stop()
        code, out = self.run_cli("ready", "demo")
        self.assertEqual(code, 3)
        self.assertIn("STOP is set", out)

    def test_held_claim_blocks_ready(self):
        self.board(owner="Codex", run="codex-1", renewed="2026-11-28T16:49:40Z")
        code, out = self.run_cli("ready", "demo")
        self.assertEqual(code, 3)
        self.assertIn("held by Codex", out)

    def test_pending_board_is_not_ready(self):
        self.board(activation="pending")
        self.assertEqual(self.run_cli("ready", "demo")[0], 3)

    def test_test_board_needs_allow_test(self):
        self.board(activation="test")
        self.assertEqual(self.run_cli("ready", "demo")[0], 3)
        self.assertEqual(self.run_cli("ready", "demo", "--allow-test")[0], 0)

    def test_missing_board(self):
        self.assertEqual(self.run_cli("ready", "nope")[0], 2)

    # claims
    def test_claims_flags_stale(self):
        self.board(owner="Claude Code", run="cc-1", renewed="2020-01-01T00:00:00Z")
        code, out = self.run_cli("claims")
        self.assertEqual(code, 0)
        self.assertIn("owner=Claude Code", out)
        self.assertIn("STALE", out)

    def test_claims_free_board(self):
        self.board()
        self.assertIn("demo [active] owner=none", self.run_cli("claims")[1])

    # overlap
    def test_overlap_with_in_progress_directory(self):
        self.board(s1="in-progress")
        code, out = self.run_cli("overlap", "demo", "P1/2")
        self.assertEqual(code, 4)
        self.assertIn("demo/P1/1 (in-progress): src/game/rules.js", out)

    def test_dispatched_counts_as_active(self):
        self.board(s1="dispatched")
        self.assertEqual(self.run_cli("overlap", "demo", "P1/2")[0], 4)

    def test_no_overlap_when_other_task_pending(self):
        self.board()
        self.assertEqual(self.run_cli("overlap", "demo", "P1/2")[0], 0)

    def test_glob_and_disjoint_paths(self):
        self.board(s1="in-progress")
        self.assertEqual(self.run_cli("overlap", "demo", "P1/3")[0], 0)

    def test_other_repo_never_overlaps(self):
        self.board(s1="in-progress")
        self.board(pid="other", s1="in-progress")
        path = os.path.join(self.dir, "development", "other", "BOARD.md")
        with open(path, encoding="utf-8") as f:
            text = f.read().replace("Sgilmore186/demo", "Sgilmore186/other")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        code, out = self.run_cli("overlap", "demo", "P1/2")
        self.assertEqual(code, 4)
        self.assertNotIn("other/", out)

    def test_unknown_task(self):
        self.board()
        self.assertEqual(self.run_cli("overlap", "demo", "P9/9")[0], 2)

    def test_parses_real_board_shape(self):
        # The live Gridline board must stay readable by the checker.
        sys.path.insert(0, os.path.join(REPO, "scripts"))
        import control
        real = os.path.join(REPO, "development", "football-game", "BOARD.md")
        if not os.path.exists(real):
            self.skipTest("no football-game board")
        old = os.environ.get("PM_ROOT")
        os.environ["PM_ROOT"] = REPO
        try:
            b = control.read_board("football-game")
        finally:
            if old is None:
                os.environ.pop("PM_ROOT", None)
            else:
                os.environ["PM_ROOT"] = old
        self.assertEqual(b["repo"], "Sgilmore186/gridline")
        self.assertTrue(b["tasks"])


if __name__ == "__main__":
    unittest.main()
