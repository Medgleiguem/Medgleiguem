"""Behavior tests for the offline activity-generation boundary (no network)."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


SCRIPT = Path(__file__).with_name("update_activity.py")


def payload(days):
    return {"data": {"user": {
        "login": "Medgleiguem", "followers": {"totalCount": 9},
        "repositories": {"nodes": [
            {"name": "DO-NOT-PUBLISH-REPO", "stargazerCount": 2,
             "languages": {"edges": [
                 {"size": 75, "node": {"name": "Python", "color": "#3572A5"}},
                 {"size": 25, "node": {"name": "Shell", "color": "#89e051"}}]}},
            {"stargazerCount": 3, "languages": {"edges": [
                {"size": 25, "node": {"name": "Python", "color": "#3572A5"}}]}}
        ]},
        "contributionsCollection": {
            "totalCommitContributions": 7, "totalPullRequestContributions": 2,
            "totalIssueContributions": 1, "totalPullRequestReviewContributions": 3,
            "restrictedContributionsCount": 12,
            "privateSecret": "DO-NOT-PUBLISH-PRIVATE",
            "contributionCalendar": {"totalContributions": 999,
                "weeks": [{"contributionDays": [
                    {"date": day, "contributionCount": count} for day, count in days
                ]}]}
        }
    }}}


class ActivityTests(unittest.TestCase):
    def run_generator(self, source, today="2026-10-24", existing=None):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        input_path = root / "input.json"
        input_path.write_text(json.dumps(source))
        if existing:
            for name, text in existing.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
        process = subprocess.run(
            [sys.executable, str(SCRIPT), "--input", str(input_path),
             "--output-dir", str(root), "--today", today],
            capture_output=True, text=True,
        )
        return process, root

    def snapshot(self, source, today="2026-10-24"):
        process, root = self.run_generator(source, today)
        self.assertEqual(process.returncode, 0, process.stderr)
        return json.loads((root / "data/activity.json").read_text()), root

    def test_empty_today_keeps_yesterdays_current_streak(self):
        data, _ = self.snapshot(payload([
            ("2026-10-20", 0), ("2026-10-21", 5), ("2026-10-22", 1),
            ("2026-10-23", 2), ("2026-10-24", 0)]))
        self.assertEqual(data["stats"]["current_streak"], 3)
        self.assertEqual(data["stats"]["longest_streak"], 3)
        self.assertEqual(data["stats"]["active_days"], 3)

    def test_calendar_gaps_break_both_streaks(self):
        data, _ = self.snapshot(payload([
            ("2026-10-19", 1), ("2026-10-20", 1),
            ("2026-10-22", 1), ("2026-10-24", 1)]))
        self.assertEqual(data["stats"]["current_streak"], 1)
        self.assertEqual(data["stats"]["longest_streak"], 2)

    def test_no_recent_activity_means_zero_current_streak(self):
        data, _ = self.snapshot(payload([("2026-10-20", 5), ("2026-10-24", 0)]))
        self.assertEqual(data["stats"]["current_streak"], 0)

    def test_last_30_days_are_inclusive_and_total_uses_github_calendar(self):
        data, _ = self.snapshot(payload([
            ("2026-09-24", 100), ("2026-09-25", 2),
            ("2026-10-23", 3), ("2026-10-24", 4)]))
        self.assertEqual(data["stats"]["last_30_days"], 9)
        self.assertEqual(data["stats"]["total_contributions"], 999)
        self.assertEqual(data["window"], {"start": "2026-09-24", "end": "2026-10-24"})

    def test_snapshot_contains_only_allowlisted_counts_dates_and_public_languages(self):
        data, root = self.snapshot(payload([("2026-10-24", 1)]))
        self.assertEqual(data["public_languages"][0]["name"], "Python")
        self.assertEqual(data["public_languages"][0]["bytes"], 100)
        self.assertEqual(data["public_languages"][0]["percent"], 80.0)
        self.assertEqual(data["stats"]["public_stars"], 5)
        for path in list((root / "assets").glob("*.svg")) + [root / "data/activity.json"]:
            text = path.read_text()
            self.assertNotIn("DO-NOT-PUBLISH", text)
            self.assertNotIn("privateSecret", text)

    def test_graphql_error_preserves_previous_snapshot(self):
        process, root = self.run_generator(
            {"errors": [{"message": "DO-NOT-LOG-SECRETS"}]},
            existing={"data/activity.json": "previous good snapshot"})
        self.assertNotEqual(process.returncode, 0)
        self.assertEqual((root / "data/activity.json").read_text(), "previous good snapshot")
        self.assertNotIn("DO-NOT-LOG-SECRETS", process.stderr)

    def test_negative_counts_and_duplicate_dates_are_rejected(self):
        for days in [[("2026-10-24", -1)], [("2026-10-24", 1), ("2026-10-24", 2)]]:
            with self.subTest(days=days):
                process, _ = self.run_generator(payload(days))
                self.assertEqual(process.returncode, 1)

    def test_invalid_calendar_does_not_echo_untrusted_payload(self):
        source = payload([("DO-NOT-LOG-PRIVATE-DATA", 1)])
        process, _ = self.run_generator(source)
        self.assertEqual(process.returncode, 1)
        self.assertNotIn("DO-NOT-LOG-PRIVATE-DATA", process.stderr)

    def test_missing_profile_and_login_mismatch_preserve_good_data(self):
        wrong_user = payload([("2026-10-24", 1)])
        wrong_user["data"]["user"]["login"] = "another-account"
        for source in [{"data": {"user": None}}, wrong_user]:
            with self.subTest(source=source):
                process, root = self.run_generator(source, existing={"data/activity.json": "good"})
                self.assertEqual(process.returncode, 1)
                self.assertEqual((root / "data/activity.json").read_text(), "good")

    def test_rendered_variants_are_accessible_self_contained_svg(self):
        _, root = self.snapshot(payload([("2026-10-24", 3)]))
        for name in ["activity.svg", "activity-mobile.svg", "activity-static.svg", "activity-mobile-static.svg"]:
            text = (root / "assets" / name).read_text()
            svg = ET.fromstring(text)
            self.assertIsNotNone(svg.find("{http://www.w3.org/2000/svg}title"))
            self.assertIsNotNone(svg.find("{http://www.w3.org/2000/svg}desc"))
            self.assertNotIn("<script", text)
            self.assertNotIn("https://", text)
            self.assertIn("GitHub-visible contributions", text)
            self.assertIn("Public-repository languages", text)
            if "static" in name:
                self.assertNotIn("@keyframes", text)
            else:
                self.assertIn("prefers-reduced-motion", text)

    def test_skyline_bars_use_real_weekly_totals_and_proportional_heights(self):
        _, root = self.snapshot(payload([
            ("2026-10-11", 2), ("2026-10-18", 2),
            ("2026-10-19", 3), ("2026-10-24", 5)]))
        ns = {"svg": "http://www.w3.org/2000/svg"}
        for name in ["skyline.svg", "skyline-mobile.svg", "skyline-static.svg", "skyline-mobile-static.svg"]:
            self.assertTrue((root / "assets" / name).exists(), "Generator must emit the skyline variant")
            svg = ET.parse(root / "assets" / name).getroot()
            bars = [element for element in svg.iter() if "data-week" in element.attrib]
            self.assertEqual([(bar.attrib["data-week"], bar.attrib["data-count"]) for bar in bars],
                             [("2026-10-11", "2"), ("2026-10-18", "10")])
            heights = [float(bar.find('svg:rect[@data-face="front"]', ns).attrib["height"]) for bar in bars]
            self.assertAlmostEqual(heights[1] / heights[0], 5, places=2)
            content = (root / "assets" / name).read_text()
            self.assertIn("GitHub-visible contributions", content)
            self.assertIn("2026-10-11", content)
            self.assertIn("2026-10-24", content)
            if "static" in name:
                self.assertNotIn("@keyframes", content)
            else:
                self.assertIn("prefers-reduced-motion", content)

    def test_mobile_skyline_limits_to_latest_27_weeks_and_labels_scope(self):
        _, root = self.snapshot(payload([
            ("2026-01-04", 7), ("2026-10-18", 3), ("2026-10-24", 2)]))
        self.assertTrue((root / "assets/skyline.svg").exists(), "Generator must emit the full skyline")
        desktop = ET.parse(root / "assets/skyline.svg").getroot()
        mobile = ET.parse(root / "assets/skyline-mobile.svg").getroot()
        desktop_bars = [e for e in desktop.iter() if "data-week" in e.attrib]
        mobile_bars = [e for e in mobile.iter() if "data-week" in e.attrib]
        self.assertEqual(len(mobile_bars), 27)
        self.assertGreater(len(desktop_bars), 27)
        self.assertEqual(sum(int(e.attrib["data-count"]) for e in mobile_bars), 5)
        self.assertEqual(sum(int(e.attrib["data-count"]) for e in desktop_bars), 12)
        self.assertIn("Last 27 weeks", (root / "assets/skyline-mobile.svg").read_text())


if __name__ == "__main__":
    unittest.main()
