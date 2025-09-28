from adaptive.engine import AdaptiveEngine

def test_rate_and_mastery_cycle():
    eng = AdaptiveEngine(backend="json", path=".adaptive/test_data.json")
    r = eng.rate_item("itemX", 2)
    assert r.next_interval >= 60
    m = eng.update_mastery("skillX", 2)
    assert m["mastery"] > 0