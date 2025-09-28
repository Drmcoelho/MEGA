from adaptive.mastery import MasteryTracker

def test_mastery_updates():
    m = MasteryTracker()
    m.update("skillA", 2)
    assert m.mastery("skillA") > 0