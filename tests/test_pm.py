"""Behavior tests for scripts/pm.py.

Run from the repo root:  python3 -m unittest discover -s tests -v
Standard library only. Each test runs pm.py against a scratch copy of the data,
so the real ideas.json, projects.json and log.md are never touched.
"""
import json, os, shutil, subprocess, sys, tempfile, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IDEAS = {"updated": "2026-01-01", "ideas": [
    {"id": "idea-a", "name": "Idea A", "description": "An idea", "goal": "A done", "added": "2026-01-01",
     "notes": "Has a prototype", "aliases": ["alpha"]},
]}
PROJECTS = {"updated": "2026-01-01", "rules": {"max_primary": 1, "max_secondary": 2}, "projects": [
    {"id": "proj", "name": "Proj", "description": "", "goal": "Proj done", "status": "active", "focus": "primary",
     "stage": "Started", "next_step": "Build the thing", "open_items": ["Build the thing", "Mac encryption"],
     "progress": [], "started": "2026-01-01", "updated": "2026-01-01"},
    {"id": "other", "name": "Other", "description": "", "goal": "Other done", "status": "paused", "focus": "none",
     "stage": "", "next_step": "", "open_items": [], "progress": [], "started": "2026-01-01", "updated": "2026-01-01"},
], "parts": [
    {"id": "piece", "name": "Piece", "part_of": ["proj"], "stage": "", "updated": "2026-01-01"},
]}


class PMTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.dir, "scripts"))
        shutil.copy(os.path.join(REPO, "scripts", "pm.py"), os.path.join(self.dir, "scripts", "pm.py"))
        self.write("ideas.json", IDEAS)
        self.write("projects.json", PROJECTS)
        with open(os.path.join(self.dir, "log.md"), "w") as f:
            f.write("# Log\n\n")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    # --- helpers ---
    def write(self, name, data):
        with open(os.path.join(self.dir, name), "w") as f:
            json.dump(data, f, indent=2)

    def run_pm(self, *args):
        return subprocess.run([sys.executable, os.path.join(self.dir, "scripts", "pm.py"), *args],
                              capture_output=True, text=True, cwd=self.dir)

    def ok(self, *args):
        r = self.run_pm(*args)
        self.assertEqual(r.returncode, 0, f"expected success for {args}:\n{r.stdout}{r.stderr}")
        return r

    def fails(self, *args, says=None):
        r = self.run_pm(*args)
        self.assertNotEqual(r.returncode, 0, f"expected failure for {args}:\n{r.stdout}")
        if says:
            self.assertIn(says, r.stdout + r.stderr)
        return r

    def data(self):
        out = {}
        for name in ("ideas.json", "projects.json"):
            with open(os.path.join(self.dir, name)) as f:
                out[name] = json.load(f)
        return out

    def item(self, id_):
        return json.loads(self.ok("get", id_).stdout)

    def log_lines(self):
        with open(os.path.join(self.dir, "log.md")) as f:
            return [l for l in f.read().splitlines() if l.startswith("- ")]

    def assertUnchanged(self, before):
        self.assertEqual(self.data(), before)


class Basics(PMTest):
    def test_check_and_list(self):
        self.ok("check")
        out = self.ok("list").stdout
        self.assertIn("proj: Proj [active, primary]", out)

    def test_dates_are_validated(self):
        self.fails("update", "proj", "--set", "stage=x", "--date", "banana", says="YYYY-MM-DD")
        self.fails("update", "proj", "--set", "stage=x", "--date", "2026-02-30", says="not a real date")
        self.ok("update", "proj", "--set", "stage=x", "--date", "2026-02-28")
        self.assertEqual(self.item("proj")["updated"], "2026-02-28")

    def test_line_breaks_rejected(self):
        before = self.data()
        self.fails("update", "proj", "--set", "stage=one\n- 2099-01-01: fake", says="line breaks")
        self.assertUnchanged(before)

    def test_unknown_fields_rejected(self):
        self.fails("update", "proj", "--set", "statu=done", says="not a project field")
        self.fails("update", "idea-a", "--set", "focus=primary", says="not a idea field")

    def test_no_double_periods_in_log(self):
        self.ok("update", "proj", "--set", "stage=Done.", "--reason", "Because.")
        self.assertNotIn("..", self.log_lines()[-1])

    def test_dry_run_changes_nothing(self):
        before = self.data()
        self.ok("done", "proj", "--dry-run")
        self.assertUnchanged(before)
        self.assertEqual(self.log_lines(), [])


class Ideas(PMTest):
    def test_idea_needs_description(self):
        self.fails("add", "idea", "--id", "b", "--name", "B", says="--description")
        self.ok("add", "idea", "--id", "b", "--name", "B", "--description", "Thing B")
        self.assertEqual(self.item("b")["description"], "Thing B")

    def test_projects_go_through_ideas_first(self):
        self.fails("add", "project", "--id", "p2", "--name", "P2", "--goal", "g", says="ideas first")
        self.fails("add", "project", "--id", "p2", "--name", "P2", "--goal", "g", "--skip-idea", says="--reason")
        self.ok("add", "project", "--id", "p2", "--name", "P2", "--goal", "g", "--skip-idea",
                "--reason", "imported", "--description", "Project two")
        self.assertEqual(self.item("p2")["description"], "Project two")

    def test_move_idea_to_project_keeps_description(self):
        self.ok("move", "idea-a", "--to", "project")
        p = self.item("idea-a")
        self.assertEqual(p["kind"], "project")
        self.assertEqual(p["description"], "An idea")
        self.assertEqual(p["goal"], "A done")


class FinishRule(PMTest):
    def test_stepping_away_needs_reason_and_names_whats_left(self):
        before = self.data()
        for status in ("paused", "archived", "dropped"):
            r = self.fails("update", "proj", "--set", f"status={status}", "--set", "focus=none", says="--reason")
            self.assertIn("Mac encryption", r.stderr)
        self.assertUnchanged(before)
        self.ok("update", "proj", "--set", "status=paused", "--set", "focus=none", "--reason", "Busy")
        self.assertIn("Reason: Busy.", self.log_lines()[-1])

    def test_dropping_focus_needs_reason(self):
        self.fails("update", "proj", "--set", "focus=none", says="--reason")

    def test_goal_reached_needs_no_reason(self):
        self.ok("update", "proj", "--set", "status=done", "--set", "focus=none")

    def test_moving_project_back_to_ideas_needs_reason(self):
        self.fails("move", "proj", "--to", "idea", says="--reason")

    def test_delete_needs_reason(self):
        self.fails("delete", "idea-a")

    def test_focus_limits(self):
        self.ok("add", "project", "--id", "p2", "--name", "P2", "--goal", "g", "--skip-idea", "--reason", "t")
        self.fails("update", "p2", "--set", "focus=primary", says="too many primary")

    def test_active_without_focus_is_flagged(self):
        self.ok("add", "project", "--id", "p2", "--name", "P2", "--goal", "g", "--skip-idea", "--reason", "t")
        self.assertIn("p2' is active but has no focus", self.ok("check").stdout)
        self.assertIn("NO FOCUS", self.ok("list", "projects").stdout)


class Done(PMTest):
    def test_done_moves_next_step_to_progress_and_closes_item(self):
        self.ok("done", "proj", "--next", "Ship it", "--date", "2026-03-01")
        p = self.item("proj")
        self.assertEqual(p["progress"], [{"date": "2026-03-01", "step": "Build the thing"}])
        self.assertEqual(p["next_step"], "Ship it")
        self.assertEqual(p["open_items"], ["Mac encryption"])
        self.assertIn("Closed open item: Build the thing.", self.log_lines()[-1])

    def test_match_ignores_case_spacing_and_punctuation(self):
        self.ok("done", "proj", "--step", "  mac   ENCRYPTION. ")
        self.assertEqual(self.item("proj")["open_items"], ["Build the thing"])

    def test_item_flag_and_bad_item(self):
        before = self.data()
        self.fails("done", "proj", "--step", "x", "--item", "nope", says="not an open item")
        self.assertUnchanged(before)
        self.ok("done", "proj", "--step", "Wrote the crypto", "--item", "Mac encryption")
        p = self.item("proj")
        self.assertEqual(p["open_items"], ["Build the thing"])
        self.assertEqual(p["next_step"], "Build the thing")  # --step leaves next_step alone

    def test_last_open_item_asks_about_goal(self):
        self.ok("done", "proj", "--item", "Mac encryption", "--step", "a")
        r = self.ok("done", "proj")
        self.assertIn("is the goal reached", r.stdout)

    def test_done_blocked_on_inactive_project(self):
        self.fails("done", "other", "--step", "x", says="not active")

    def test_done_only_on_projects(self):
        self.fails("done", "piece", "--step", "x", says="projects only")

    def test_progress_cannot_be_set(self):
        self.fails("update", "proj", "--set", "progress=x", says="can't be set directly")

    def test_needs_a_step(self):
        self.ok("done", "proj")
        self.fails("done", "proj", says="no next_step")


class Parts(PMTest):
    def test_deleting_parent_removes_orphaned_part(self):
        self.ok("delete", "proj", "--reason", "test")
        self.fails("get", "piece")

    def test_part_needs_existing_parent(self):
        self.fails("add", "part", "--id", "x", "--name", "X", "--part-of", "ghost", says="unknown parent")


class Commit(PMTest):
    def git(self, *args):
        return subprocess.run(["git", "-C", self.dir, *args], capture_output=True, text=True)

    def setUp(self):
        super().setUp()
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "t")
        self.git("add", "-A")
        self.git("commit", "-qm", "init")

    def last_message(self):
        return self.git("log", "-1", "--format=%B").stdout.strip()

    def test_commit_uses_log_lines(self):
        self.ok("update", "proj", "--set", "stage=a")
        self.ok("update", "proj", "--set", "stage=b")
        self.ok("commit")
        msg = self.last_message()
        self.assertIn("2 changes", msg.splitlines()[0])
        self.assertIn("stage=a", msg)
        self.assertIn("stage=b", msg)

    def test_hand_edit_is_refused(self):
        path = os.path.join(self.dir, "projects.json")
        with open(path) as f: text = f.read()
        with open(path, "w") as f: f.write(text.replace("Started", "Hand edited"))
        self.fails("commit", says="hand-edited")

    def test_failed_git_commit_is_reported(self):
        hook = os.path.join(self.dir, ".git", "hooks", "pre-commit")
        with open(hook, "w") as f: f.write("#!/bin/sh\nexit 1\n")
        os.chmod(hook, 0o755)
        self.ok("update", "proj", "--set", "stage=a")
        self.fails("commit", says="git commit failed")


class RealData(unittest.TestCase):
    def test_repo_data_passes_check(self):
        r = subprocess.run([sys.executable, os.path.join(REPO, "scripts", "pm.py"), "check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
