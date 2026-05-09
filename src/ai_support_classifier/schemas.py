from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


IntentCategory = Literal[
    "billing_dispute",
    "account_access",
    "technical_issue",
    "cancellation_request",
    "security_alert",
    "general_inquiry",
]
Urgency = Literal["low", "medium", "high", "critical"]
Sentiment = Literal["positive", "neutral", "negative", "angry"]


class CustomerIntent(BaseModel):
    """Schema for classifying customer support tickets."""

    category: IntentCategory = Field(
        description="Primary intent category of the customer message."
    )
    urgency: Urgency = Field(
        description="How urgently this issue needs attention."
    )
    sentiment: Sentiment = Field(
        description="Customer's emotional tone."
    )
    entities: list[str] = Field(
        default_factory=list,
        description="Important extracted entities such as amounts, dates, merchants, accounts, cards, or products."
    )
    summary: str = Field(
        description="One-sentence summary of the customer's issue."
    )
    recommended_action: str = Field(
        description="Suggested next step for the support agent or workflow."
    )


class ProviderResult(BaseModel):
    """Standard result returned by each provider."""

    provider: str
    model: str
    text: str | None = None
    intent: CustomerIntent | None = None
    latency_seconds: float
    tokens: int | str | None = None
    status: Literal["success", "failed"]
    error: str | None = None
