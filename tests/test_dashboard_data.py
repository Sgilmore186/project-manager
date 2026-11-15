"""Tests for scripts/dashboard_data.py (the issue body the dashboard reads)."""
import json, os, shutil, sys, tempfile, unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
import dashboard_data  # noqa: E402


class DashboardData(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def write(self, ideas, projects):
        for name, data in (("ideas.json", ideas), ("projects.json", projects)):
            with open(os.path.join(self.dir, name), "w") as f:
                json.dump(data, f)

    def test_round_trip_keeps_both_files(self):
        ideas = {"ideas": [{"id": "a", "name": "A", "description": "Has } and { and ```"}]}
        projects = {"projects": [{"id": "p", "name": "P"}], "parts": []}
        self.write(ideas, projects)
        body = dashboard_data.build(self.dir, commit="abc123")
        self.assertTrue(body.startswith(dashboard_data.HEADER))
        payload = dashboard_data.parse(body)
        self.assertEqual(payload, {"commit": "abc123", "ideas": ideas, "projects": projects})

    def test_too_big_is_refused(self):
        self.write({"ideas": [{"id": "x", "name": "x" * 70000}]}, {"projects": []})
        with self.assertRaises(ValueError):
            dashboard_data.build(self.dir)

    def test_real_data_fits(self):
        body = dashboard_data.build(REPO)
        self.assertLess(len(body), dashboard_data.MAX_BODY)
        payload = dashboard_data.parse(body)
        self.assertIn("projects", payload["projects"])
        self.assertIn("ideas", payload["ideas"])


if __name__ == "__main__":
    unittest.main()
