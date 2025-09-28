from case_generator.core import compose_case

def test_compose_case():
    c = compose_case("ECG")
    assert c.topic == "ECG"
    assert isinstance(c.plan, list)