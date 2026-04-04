"""
agent/llm_client.py — Thin abstraction over Anthropic and OpenAI chat APIs.

Returns plain strings so the rest of the agent is provider-agnostic.
"""

from __future__ import annotations
from typing import Protocol
from utils.config import Config

class LLMClient(Protocol):
    def complete(self, system: str, messages: list[dict]) -> str: ...

# -- Anthropic --
class AnthropicClient:
    def __init__(self, config: Config) -> None:
        import anthropic
        self._client = anthropic.Anthropic(api_key=config.anthropic_api_key)
        self._model = config.model

    def complete(self, system: str, messages: list[dict]) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=system,
            messages=messages
        )
        return response.content[0].text
    
# -- OpenAI --
class OpenAIClient:
    def __init__(self, config: Config) -> None:
        import openai
        self._client = openai.OpenAI(api_key=config.openai_api_key)
        self._model = config.model

    def complete(self, system: str, messages: list[dict]) -> str:
        all_messages = [{"role": "system", "content": system}] + messages
        response = self._client.chat.completions.create(
            model=self._model,
            max_tokens=4096,
            messages=all_messages
        )
        return response.choices[0].message.content or ""

# -- Factory --
def build_client(config: Config) -> LLMClient:
    match config.provider:
        case "anthropic":
            return AnthropicClient(config)
        case "open":
            return OpenAIClient(config)
        case _:
            raise ValueError(f"Unknown provider: {config.provider!r}")