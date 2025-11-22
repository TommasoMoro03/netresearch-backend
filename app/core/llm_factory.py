"""
LLM Factory for Together AI integration.

This module provides helpers to instantiate OpenAI-compatible clients
for Together AI, as well as pyagentspec configs.

Usage example with OpenAI client:
    from app.core.llm_factory import get_openai_client

    client = get_openai_client()
    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[{"role": "user", "content": "Hello!"}]
    )

Usage example with pyagentspec:
    from app.core.llm_factory import get_llm_config
    from pyagentspec import Agent

    llm_config = get_llm_config()
    agent = Agent(llm_config=llm_config, ...)
"""

from app.core.config import settings
from typing import Any


def get_openai_client():
    """
    Get an OpenAI client configured for Together AI.

    Together AI provides an OpenAI-compatible API, so we use the OpenAI SDK.

    Returns:
        openai.OpenAI: Configured client for Together AI

    Example:
        ```python
        client = get_openai_client()
        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[{"role": "user", "content": "Hello!"}]
        )
        ```
    """
    import openai

    config = settings.get_openai_client_config()
    return openai.OpenAI(**config)


def get_llm_config() -> Any:
    """
    Factory function to get LLM config for pyagentspec.

    Since Together AI uses OpenAI-compatible API, we use OpenAiConfig from pyagentspec.

    Returns:
        LLM config object ready for pyagentspec

    Example usage with pyagentspec:
        ```python
        from pyagentspec import OpenAiConfig

        llm_config = get_llm_config()
        # llm_config is an OpenAiConfig configured for Together AI
        ```
    """
    # Return the config dict for now
    # When pyagentspec is installed, uncomment below:
    # from pyagentspec import OpenAiConfig
    # config_dict = settings.get_agent_spec_llm_config()
    # return OpenAiConfig(**config_dict)

    return settings.get_agent_spec_llm_config()
