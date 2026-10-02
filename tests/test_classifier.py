from app.classifier import classify_lead

def test_sales_lead():
    category, confidence = classify_lead("Can I get pricing and a product demo?")
    assert category == "sales"
    assert 0 <= confidence <= 1

def test_support_lead():
    category, _ = classify_lead("The integration is broken and I need help")
    assert category in {"support", "partnership"}

def test_general_lead():
    category, confidence = classify_lead("Hello, I have a question")
    assert category == "general"
    assert confidence == 0.45
