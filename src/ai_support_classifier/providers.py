from __future__ import annotations

import time
from typing import Protocol

from .config import Settings, get_settings
from .json_utils import extract_json_object
from .prompts import SUPPORT_TICKET_RESPONSE_PROMPT, JSON_CLASSIFICATION_PROMPT, SYSTEM_PROMPT
from .schemas import CustomerIntent, ProviderResult


class Provider(Protocol):
    name: str
    model: str

    def classify(self, message: str) -> ProviderResult: ...
    def generate_text(self, message: str) -> ProviderResult: ...


class OpenAIProvider:
    name = "OpenAI"

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.model = self.settings.openai_chat_model
        self.reasoning_model = self.settings.openai_reasoning_model
        from openai import OpenAI
        self.client = OpenAI(api_key=self.settings.openai_api_key)

    def generate_text(self, message: str) -> ProviderResult:
        start = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=self.settings.default_temperature,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": SUPPORT_TICKET_RESPONSE_PROMPT.format(message=message)},
                ],
            )
            text = response.choices[0].message.content or ""
            tokens = response.usage.total_tokens if response.usage else None
            return ProviderResult(
                provider=self.name,
                model=self.model,
                text=text,
                latency_seconds=round(time.time() - start, 2),
                tokens=tokens,
                status="success",
            )
        except Exception as exc:
            return self._failed(start, exc, self.model)

    def classify(self, message: str) -> ProviderResult:
        start = time.time()
        try:
            response = self.client.responses.parse(
                model=self.reasoning_model,
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
                text_format=CustomerIntent,
            )
            intent = response.output_parsed
            return ProviderResult(
                provider=self.name,
                model=self.reasoning_model,
                intent=intent,
                latency_seconds=round(time.time() - start, 2),
                tokens="See provider dashboard / API response usage",
                status="success",
            )
        except Exception as exc:
            return self._failed(start, exc, self.reasoning_model)

    def _failed(self, start: float, exc: Exception, model: str) -> ProviderResult:
        return ProviderResult(
            provider=self.name,
            model=model,
            latency_seconds=round(time.time() - start, 2),
            status="failed",
            error=str(exc),
        )


class AnthropicProvider:
    name = "Anthropic Claude"

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.model = self.settings.anthropic_model
        from anthropic import Anthropic
        self.client = Anthropic(api_key=self.settings.anthropic_api_key)

    def generate_text(self, message: str) -> ProviderResult:
        start = time.time()
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.settings.default_max_tokens,
                temperature=self.settings.default_temperature,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": SUPPORT_TICKET_RESPONSE_PROMPT.format(message=message)}],
            )
            text = response.content[0].text
            tokens = response.usage.input_tokens + response.usage.output_tokens
            return ProviderResult(
                provider=self.name,
                model=self.model,
                text=text,
                latency_seconds=round(time.time() - start, 2),
                tokens=tokens,
                status="success",
            )
        except Exception as exc:
            return self._failed(start, exc)

    def classify(self, message: str) -> ProviderResult:
        start = time.time()
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.settings.default_max_tokens,
                temperature=0.1,
                system="You are a JSON classifier. Return only valid JSON. Do not wrap in Markdown.",
                messages=[{"role": "user", "content": JSON_CLASSIFICATION_PROMPT.format(message=message)}],
            )
            text = response.content[0].text
            parsed = extract_json_object(text)
            intent = CustomerIntent(**parsed)
            tokens = response.usage.input_tokens + response.usage.output_tokens
            return ProviderResult(
                provider=self.name,
                model=self.model,
                text=text,
                intent=intent,
                latency_seconds=round(time.time() - start, 2),
                tokens=tokens,
                status="success",
            )
        except Exception as exc:
            return self._failed(start, exc)

    def _failed(self, start: float, exc: Exception) -> ProviderResult:
        return ProviderResult(
            provider=self.name,
            model=self.model,
            latency_seconds=round(time.time() - start, 2),
            status="failed",
            error=str(exc),
        )


class GeminiProvider:
    name = "Google Gemini"

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.model = self.settings.gemini_model
        from google import genai
        self.genai = genai
        self.client = genai.Client(api_key=self.settings.gemini_api_key)

    def generate_text(self, message: str) -> ProviderResult:
        start = time.time()
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=SUPPORT_TICKET_RESPONSE_PROMPT.format(message=message),
                config=self.genai.types.GenerateContentConfig(
                    temperature=self.settings.default_temperature,
                    max_output_tokens=self.settings.default_max_tokens,
                    system_instruction=SYSTEM_PROMPT,
                ),
            )
            tokens = response.usage_metadata.total_token_count if response.usage_metadata else None
            return ProviderResult(
                provider=self.name,
                model=self.model,
                text=response.text,
                latency_seconds=round(time.time() - start, 2),
                tokens=tokens,
                status="success",
            )
        except Exception as exc:
            return self._failed(start, exc)

    def classify(self, message: str) -> ProviderResult:
        start = time.time()
        try:
            # Prompt-based JSON keeps this compatible across SDK versions.
            prompt = JSON_CLASSIFICATION_PROMPT.format(message=message)
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=self.genai.types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=self.settings.default_max_tokens,
                    system_instruction="Return only valid JSON. Do not wrap in Markdown.",
                ),
            )
            parsed = extract_json_object(response.text or "")
            intent = CustomerIntent(**parsed)
            tokens = response.usage_metadata.total_token_count if response.usage_metadata else None
            return ProviderResult(
                provider=self.name,
                model=self.model,
                text=response.text,
                intent=intent,
                latency_seconds=round(time.time() - start, 2),
                tokens=tokens,
                status="success",
            )
        except Exception as exc:
            return self._failed(start, exc)

    def _failed(self, start: float, exc: Exception) -> ProviderResult:
        return ProviderResult(
            provider=self.name,
            model=self.model,
            latency_seconds=round(time.time() - start, 2),
            status="failed",
            error=str(exc),
        )


class GroqProvider:
    name = "Groq / Llama"

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.model = self.settings.groq_model
        from groq import Groq
        self.client = Groq(api_key=self.settings.groq_api_key)

    def generate_text(self, message: str) -> ProviderResult:
        start = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=self.settings.default_temperature,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": SUPPORT_TICKET_RESPONSE_PROMPT.format(message=message)},
                ],
            )
            text = response.choices[0].message.content or ""
            tokens = response.usage.total_tokens if response.usage else None
            return ProviderResult(
                provider=self.name,
                model=self.model,
                text=text,
                latency_seconds=round(time.time() - start, 2),
                tokens=tokens,
                status="success",
            )
        except Exception as exc:
            return self._failed(start, exc)

    def classify(self, message: str) -> ProviderResult:
        start = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0.1,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You are a JSON classifier. Return only valid JSON."},
                    {"role": "user", "content": JSON_CLASSIFICATION_PROMPT.format(message=message)},
                ],
            )
            text = response.choices[0].message.content or "{}"
            parsed = extract_json_object(text)
            intent = CustomerIntent(**parsed)
            tokens = response.usage.total_tokens if response.usage else None
            return ProviderResult(
                provider=self.name,
                model=self.model,
                text=text,
                intent=intent,
                latency_seconds=round(time.time() - start, 2),
                tokens=tokens,
                status="success",
            )
        except Exception as exc:
            return self._failed(start, exc)

    def _failed(self, start: float, exc: Exception) -> ProviderResult:
        return ProviderResult(
            provider=self.name,
            model=self.model,
            latency_seconds=round(time.time() - start, 2),
            status="failed",
            error=str(exc),
        )


def build_provider(provider_name: str, settings: Settings | None = None):
    from .mock_provider import MockProvider

    provider_name = provider_name.lower().strip()
    settings = settings or get_settings()

    if provider_name == "mock":
        return MockProvider()
    if provider_name == "openai":
        return OpenAIProvider(settings)
    if provider_name in {"anthropic", "claude"}:
        return AnthropicProvider(settings)
    if provider_name == "gemini":
        return GeminiProvider(settings)
    if provider_name in {"groq", "llama"}:
        return GroqProvider(settings)

    raise ValueError(f"Unknown provider: {provider_name}")


def build_configured_providers(settings: Settings | None = None):
    settings = settings or get_settings()
    providers = []

    if settings.openai_api_key:
        providers.append(OpenAIProvider(settings))
    if settings.groq_api_key:
        providers.append(GroqProvider(settings))
    if settings.gemini_api_key:
        providers.append(GeminiProvider(settings))
    if settings.anthropic_api_key:
        providers.append(AnthropicProvider(settings))

    if not providers:
        from .mock_provider import MockProvider
        providers.append(MockProvider())

    return providers
