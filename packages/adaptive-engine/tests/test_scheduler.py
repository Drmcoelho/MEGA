from adaptive.scheduler import IntervalScheduler

def test_interval_progression():
    s = IntervalScheduler()
    first = s.next_interval("item1", 2)
    second = s.next_interval("item1", 2)
    assert second >= first