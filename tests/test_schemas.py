from ai_support_classifier.schemas import CustomerIntent


def test_customer_intent_schema_valid():
    intent = CustomerIntent(
        category="security_alert",
        urgency="critical",
        sentiment="negative",
        entities=["verification code"],
        summary="Customer received a verification code they did not request.",
        recommended_action="Escalate to security support workflow."
    )

    assert intent.category == "security_alert"
    assert intent.urgency == "critical"