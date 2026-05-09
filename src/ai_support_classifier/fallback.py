from __future__ import annotations

from collections.abc import Iterable

from .providers import build_configured_providers
from .schemas import ProviderResult


def classify_with_fallback(message: str, providers: Iterable | None = None) -> ProviderResult:
    """Try providers in order and return the first successful structured classification."""
    providers = list(providers or build_configured_providers())
    failures: list[str] = []

    for provider in providers:
        result = provider.classify(message)
        if result.status == "success" and result.intent is not None:
            return result
        failures.append(f"{result.provider}: {result.error or 'No structured intent returned'}")

    return ProviderResult(
        provider="none",
        model="none",
        latency_seconds=0,
        status="failed",
        error="All providers failed. " + " | ".join(failures),
    )


def compare_providers(message: str, providers: Iterable | None = None) -> list[ProviderResult]:
    """Classify a message with all providers and return all results."""
    providers = list(providers or build_configured_providers())
    return [provider.classify(message) for provider in providers]
