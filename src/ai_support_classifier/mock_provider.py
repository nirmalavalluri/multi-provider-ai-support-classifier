from __future__ import annotations

import time
from .schemas import CustomerIntent, ProviderResult


class MockProvider:
    """Deterministic provider for demos, tests, screenshots, and GitHub portfolio usage."""

    name = "Mock"
    model = "mock-ai-support-classifier-v1"

    def classify(self, message: str) -> ProviderResult:
        start = time.time()
        lower = message.lower()

        if any(word in lower for word in ["verification code", "unauthorized", "suspicious", "access my account", "account takeover"]):
            category = "security_alert"
            urgency = "critical"
            sentiment = "negative"
            action = "Escalate to the security support workflow, verify the customer securely, and advise them not to share verification codes."
        elif any(word in lower for word in ["charged", "charge", "refund", "invoice", "billing", "renewal", "$"]):
            category = "billing_dispute"
            urgency = "high"
            sentiment = "angry" if any(word in lower for word in ["immediately", "unacceptable", "angry", "reverse"]) else "negative"
            action = "Open a billing review, verify subscription and invoice details, and route the ticket to the billing support team."
        elif any(word in lower for word in ["cancel", "canceled", "cancelled", "subscription"]):
            category = "cancellation_request"
            urgency = "medium"
            sentiment = "negative"
            action = "Verify the subscription status, confirm cancellation details, and provide the customer with next steps."
        elif any(word in lower for word in ["error", "bug", "failed", "failing", "500", "not working", "dashboard", "export"]):
            category = "technical_issue"
            urgency = "high"
            sentiment = "negative"
            action = "Collect reproduction details, check logs, and route the ticket to the technical support team."
        elif any(word in lower for word in ["login", "password", "session", "locked out"]):
            category = "account_access"
            urgency = "high"
            sentiment = "negative"
            action = "Verify the customer securely and guide them through account recovery or session troubleshooting."
        else:
            category = "general_inquiry"
            urgency = "low"
            sentiment = "neutral"
            action = "Answer the customer's question or route the ticket to the correct support queue."

        intent = CustomerIntent(
            category=category,  # type: ignore[arg-type]
            urgency=urgency,  # type: ignore[arg-type]
            sentiment=sentiment,  # type: ignore[arg-type]
            entities=self._extract_simple_entities(message),
            summary=f"Customer support ticket classified as {category} with {urgency} urgency.",
            recommended_action=action,
        )

        return ProviderResult(
            provider=self.name,
            model=self.model,
            intent=intent,
            latency_seconds=round(time.time() - start, 4),
            tokens="N/A",
            status="success",
        )

    def generate_text(self, message: str) -> ProviderResult:
        start = time.time()
        text = (
            "Thank you for contacting support. I understand your concern. "
            "We will review the details securely and route your ticket to the appropriate support team."
        )
        return ProviderResult(
            provider=self.name,
            model=self.model,
            text=text,
            latency_seconds=round(time.time() - start, 4),
            tokens="N/A",
            status="success",
        )

    @staticmethod
    def _extract_simple_entities(message: str) -> list[str]:
        entities: list[str] = []
        for token in message.replace(".", " ").replace(",", " ").split():
            cleaned = token.strip()
            if (
                cleaned.startswith("$")
                or cleaned.lower() in {"pro", "starter", "team", "subscription", "renewal", "invoice"}
                or cleaned in {"500"}
            ):
                entities.append(cleaned)
        return entities