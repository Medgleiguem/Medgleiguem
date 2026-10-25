"""Behavior tests for the offline activity-generation boundary (no network)."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil
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
        for name in ["workbench.svg", "workbench-mobile.svg", "workbench-static.svg", "workbench-mobile-static.svg", "workbench-compact.svg", "workbench-compact-static.svg"]:
            self.assertTrue((root / 'assets' / name).exists(), 'Collector must publish the new workbench chart')
            text = (root / "assets" / name).read_text()
            svg = ET.fromstring(text)
            self.assertIsNotNone(svg.find("{http://www.w3.org/2000/svg}title"))
            self.assertIsNotNone(svg.find("{http://www.w3.org/2000/svg}desc"))
            self.assertNotIn("<script", text)
            self.assertNotIn("https://", text)
            self.assertIn("GitHub-visible contributions", text)
            if "static" in name:
                self.assertNotIn("@keyframes", text)
            else:
                self.assertIn("prefers-reduced-motion", text)

    def test_calendar_preserves_actual_dates_and_fills_gaps_with_zero(self):
        _, root = self.snapshot(payload([
            ('2026-10-11', 2), ('2026-10-18', 2),
            ('2026-10-19', 3), ('2026-10-24', 5)]))
        expected = {f'2026-10-{day:02d}': 0 for day in range(11, 25)}
        expected.update({'2026-10-11': 2, '2026-10-18': 2,
                         '2026-10-19': 3, '2026-10-24': 5})
        variants = []
        for path in sorted((root/'assets').glob('workbench*.svg')):
            svg = ET.parse(path).getroot()
            cells = [node for node in svg.iter() if 'data-date' in node.attrib]
            self.assertEqual({c.get('data-date'): int(c.get('data-count')) for c in cells}, expected)
            variants.append([(c.get('data-date'), c.get('data-count'), c.get('fill')) for c in cells])
            self.assertTrue(all(c.find('{http://www.w3.org/2000/svg}title') is not None for c in cells))
        self.assertTrue(all(value == variants[0] for value in variants))

    def test_calendar_keeps_full_available_year_without_inventing_counts(self):
        _, root = self.snapshot(payload([
            ('2026-01-04', 7), ('2026-10-18', 3), ('2026-10-24', 2)]))
        for path in (root/'assets').glob('workbench*.svg'):
            cells = [node for node in ET.parse(path).getroot().iter() if 'data-date' in node.attrib]
            self.assertEqual(len(cells), 294)
            self.assertEqual(cells[0].get('data-date'), '2026-01-04')
            self.assertEqual(cells[-1].get('data-date'), '2026-10-24')
            self.assertEqual(sum(int(c.get('data-count')) for c in cells), 12)

    def test_type_counters_are_allowlisted_separately_from_calendar_total(self):
        data, _ = self.snapshot(payload([('2026-10-24', 3)]))
        self.assertEqual(data.get('contribution_types'), {'commits': 7, 'pull_requests': 2, 'issues': 1, 'reviews': 3})
        self.assertEqual(data['stats']['total_contributions'], 999)

    def test_missing_type_is_unavailable_and_real_zero_stays_zero(self):
        source = payload([('2026-10-24', 3)])
        collection = source['data']['user']['contributionsCollection']
        del collection['totalPullRequestReviewContributions']
        collection['totalIssueContributions'] = 0
        data, _ = self.snapshot(source)
        self.assertIsNone(data.get('contribution_types', {}).get('reviews'))
        self.assertEqual(data.get('contribution_types', {}).get('issues'), 0)

    def test_invalid_type_count_retains_previous_outputs_without_echoing_payload(self):
        source = payload([('2026-10-24', 3)])
        source['data']['user']['contributionsCollection']['totalCommitContributions'] = -1
        process, root = self.run_generator(source, existing={'data/activity.json':'good','assets/workbench.svg':'good chart'})
        self.assertEqual(process.returncode, 1)
        self.assertEqual((root/'data/activity.json').read_text(), 'good')
        self.assertEqual((root/'assets/workbench.svg').read_text(), 'good chart')

    def test_collection_window_is_retained_and_invalid_timestamp_is_rejected(self):
        source = payload([('2026-10-24', 3)])
        collection = source['data']['user']['contributionsCollection']
        collection.update(startedAt='2025-10-25T12:00:00Z', endedAt='2026-10-24T12:00:00Z')
        data, _ = self.snapshot(source)
        self.assertEqual(data.get('collection_window'), {'start':'2025-10-25T12:00:00Z','end':'2026-10-24T12:00:00Z'})
        for bad in ('DO-NOT-LOG-TIMESTAMP',None,False,17):
            collection['startedAt']=bad
            process, _ = self.run_generator(source)
            self.assertEqual(process.returncode, 1)
            self.assertNotIn('DO-NOT-LOG-TIMESTAMP', process.stderr)
            self.assertNotIn('Traceback',process.stderr)

    def test_short_zero_calendar_keeps_its_bounds_and_has_an_empty_state(self):
        _, root = self.snapshot(payload([('2026-10-24', 0)]))
        for path in (root/'assets').glob('workbench*.svg'):
            svg = ET.parse(path).getroot()
            cells = [node for node in svg.iter() if 'data-date' in node.attrib]
            self.assertEqual([(c.get('data-date'), c.get('data-count')) for c in cells], [('2026-10-24', '0')])
            self.assertIn('No contributions in this window', ''.join(svg.itertext()))

    def test_activity_values_do_not_animate_or_change_color_over_time(self):
        _, root = self.snapshot(payload([('2026-10-23', 4), ('2026-10-24', 50)]))
        svg = ET.parse(root/'assets/workbench.svg').getroot()
        cells = [node for node in svg.iter() if 'data-date' in node.attrib]
        self.assertEqual(len(cells), 2)
        for cell in cells:
            self.assertNotIn('class', cell.attrib)
            self.assertFalse(any(node.tag.rsplit('}', 1)[-1].startswith('animate') for node in cell.iter()))
        self.assertNotEqual(cells[0].get('fill'), cells[1].get('fill'))

    def test_failed_refresh_preserves_the_previous_workbench(self):
        process, root = self.run_generator({'errors': [{'message': 'bad response'}]},
            existing={'assets/workbench.svg': 'previous chart', 'data/activity.json': 'previous snapshot'})
        self.assertEqual(process.returncode, 1)
        self.assertEqual((root/'assets/workbench.svg').read_text(), 'previous chart')

    def test_refresh_and_full_generation_produce_identical_workbench_files(self):
        _, root = self.snapshot(payload([('2026-10-18', 2), ('2026-10-24', 3)]))
        before = {p.name: p.read_bytes() for p in (root/'assets').glob('workbench*.svg')}
        summary_before = (root/'work/activity.md').read_bytes()
        (root/'tools').mkdir()
        shutil.copy2(SCRIPT.with_name('generate_assets.py'), root/'tools/generate_assets.py')
        shutil.copy2(SCRIPT.with_name('desert_console.py'), root/'tools/desert_console.py')
        shutil.copy2(SCRIPT.with_name('expertise.py'), root/'tools/expertise.py')
        for name in ('activity_data.py','activity_dashboard.py'):
            shutil.copy2(SCRIPT.with_name(name), root/'tools'/name)
        shutil.copytree(SCRIPT.parent.parent/'assets/artwork/desert', root/'assets/artwork/desert')
        result = subprocess.run([sys.executable, str(root/'tools/generate_assets.py')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((root/'work/activity.md').read_bytes(),summary_before)
        for name, content in before.items():
            self.assertEqual((root/'assets'/name).read_bytes(), content, name+' changed after full generation')

    def test_calendar_metrics_describe_the_displayed_window_in_visible_text(self):
        _, root = self.snapshot(payload([('2026-10-11', 2), ('2026-10-18', 2), ('2026-10-24', 8)]))
        for path in (root/'assets').glob('workbench*.svg'):
            svg = ET.parse(path).getroot()
            metrics = {n.get('data-metric'): ''.join(n.itertext()) for n in svg.iter() if n.get('data-metric')}
            self.assertEqual(metrics.get('contributions'), '12')
            self.assertEqual(metrics.get('active-days'), '3')
            labels = ' '.join(n.text or '' for n in svg.iter() if n.tag.endswith('}text'))
            self.assertIn('2026-10-11', labels)
            self.assertIn('2026-10-24', labels)
            self.assertIn('UTC', labels)
            self.assertNotIn('999', metrics.values())


if __name__ == "__main__":
    unittest.main()
