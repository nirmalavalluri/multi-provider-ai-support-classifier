from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    groq_api_key: str | None = os.getenv("GROQ_API_KEY")

    openai_chat_model: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
    openai_reasoning_model: str = os.getenv("OPENAI_REASONING_MODEL", "gpt-5-mini")
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    default_temperature: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.2"))
    default_max_tokens: int = int(os.getenv("DEFAULT_MAX_TOKENS", "800"))


def get_settings() -> Settings:
    return Settings()
