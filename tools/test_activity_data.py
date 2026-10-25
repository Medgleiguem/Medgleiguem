"""Behavior contracts for calendar-derived metrics and public language proportions."""
from datetime import date, timedelta
import unittest
from activity_data import calendar_days, calendar_stats, weekly_totals, language_shares, activity_summary


def snapshot(start='2026-10-11', end='2026-10-25', counts=None, as_of='2026-10-25'):
    return {'window':{'start':start,'end':end}, 'as_of':as_of,
            'updated_at':'2026-10-25T03:00:00Z',
            'stats':{'total_contributions':99999,'current_streak':999},
            'calendar':[{'date':day,'count':count} for day,count in (counts or {}).items()],
            'public_languages':[]}


class ActivityDataTests(unittest.TestCase):
    def test_calendar_caps_at_366_real_dates_and_fills_only_inside_window(self):
        data=snapshot('2024-01-01','2026-10-25',{'2026-10-25':4})
        days=calendar_days(data)
        self.assertEqual(len(days),366)
        self.assertEqual(days[0][0],date(2026,10,25)-timedelta(days=365))
        self.assertEqual(sum(v for _,v in days),4)

    def test_metrics_use_calendar_dates_instead_of_reported_api_totals(self):
        data=snapshot(counts={'2026-10-22':4,'2026-10-23':2,'2026-10-24':1})
        metrics=calendar_stats(data)
        self.assertEqual(metrics,{'contributions':7,'active_days':3,'current_streak':3,'longest_streak':3,'last_30_days':7})

    def test_stale_window_has_no_current_streak_and_last30_has_exact_bounds(self):
        data=snapshot('2026-09-25','2026-10-20',{'2026-09-25':100,'2026-09-26':2,'2026-10-20':4})
        metrics=calendar_stats(data)
        self.assertEqual(metrics['current_streak'],0)
        self.assertEqual(metrics['last_30_days'],6)
        self.assertEqual(metrics['longest_streak'],2)

    def test_weeks_are_sunday_aligned_with_partial_last_week(self):
        days=calendar_days(snapshot(counts={'2026-10-11':2,'2026-10-24':3,'2026-10-25':4}))
        self.assertEqual(weekly_totals(days),[(date(2026,10,11),2),(date(2026,10,18),3),(date(2026,10,25),4)])

    def test_recent_weeks_never_include_earlier_contributions(self):
        days=calendar_days(snapshot('2026-01-01',counts={'2026-01-01':100,'2026-10-25':2}))
        weeks=weekly_totals(days)
        self.assertEqual(len(weeks),13)
        self.assertEqual(sum(count for _,count in weeks),2)

    def test_language_shares_use_bytes_and_group_the_tail(self):
        data=snapshot()
        data['public_languages']=[{'name':chr(65+i),'bytes':7-i,'percent':999} for i in range(7)]
        shares=language_shares(data)
        self.assertEqual([x['name'] for x in shares],['A','B','C','D','Other'])
        self.assertEqual(shares[-1]['bytes'],6)
        self.assertAlmostEqual(sum(x['percent'] for x in shares),100)

    def test_no_public_bytes_has_no_invented_language_share(self):
        data=snapshot()
        data['public_languages']=[{'name':'Python','bytes':0,'percent':100}]
        self.assertEqual(language_shares(data),[])

    def test_native_summary_keeps_zero_and_missing_types_distinct(self):
        data=snapshot(counts={'2026-10-25':4})
        data['contribution_types']={'commits':0,'pull_requests':None,'issues':1,'reviews':0}
        source=activity_summary(data)
        self.assertIn('| Commits | 0 |',source)
        self.assertIn('| Pull requests opened | Unavailable |',source)
        self.assertIn('2026-10-11',source)
        self.assertIn('2026-10-25',source)
        self.assertIn('Public repositories',source)


if __name__=='__main__':unittest.main()
