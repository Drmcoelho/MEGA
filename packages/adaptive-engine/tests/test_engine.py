from adaptive.engine import AdaptiveEngine
import pytest
from adaptive.exceptions import InvalidRatingError

def test_rate_and_mastery_cycle():
    eng = AdaptiveEngine(backend="json", path=".adaptive/test_data.json")
    r = eng.rate_item("itemX", 2)
    assert r.next_interval >= 60
    m = eng.update_mastery("skillX", 2)
    assert m["mastery"] > 0

def test_update_mastery_logic():
    eng = AdaptiveEngine(backend="json", path=".adaptive/test_data_mastery.json")
    
    # Initial update
    m1 = eng.update_mastery("skillY", 1)
    assert m1["mastery"] > 0
    
    # Second update should increase mastery
    m2 = eng.update_mastery("skillY", 2)
    assert m2["mastery"] > m1["mastery"]

    # Test another skill
    m3 = eng.update_mastery("skillZ", 0)
    assert m3["mastery"] < m2["mastery"] # Assuming rating 0 decreases or keeps it low

def test_invalid_rating_error():
    eng = AdaptiveEngine(backend="json", path=".adaptive/test_data_errors.json")
    with pytest.raises(InvalidRatingError):
        eng.rate_item("some_item", 3)
        
    with pytest.raises(InvalidRatingError):
        eng.update_mastery("some_skill", -1)