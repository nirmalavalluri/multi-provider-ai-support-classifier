from ai_support_classifier.json_utils import extract_json_object, strip_json_fences


def test_strip_json_fences():
    text = "```json\n{\"category\": \"billing_dispute\"}\n```"
    assert strip_json_fences(text) == '{"category": "billing_dispute"}'


def test_extract_json_object_with_extra_text():
    text = "Here is JSON: {\"category\": \"billing_dispute\"} thanks"
    assert extract_json_object(text) == {"category": "billing_dispute"}