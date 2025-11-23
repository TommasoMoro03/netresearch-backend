from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Dict, Any, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Automatically loads from .env file if present.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "NetResearch"
    
    # OpenAI Configuration (for Whisper)
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API Key")

    # Together AI Configuration
    TOGETHER_API_KEY: Optional[str] = Field(
        default=None,
        description="Together AI API key (provided by hackathon organizers)"
    )
    TOGETHER_BASE_URL: str = Field(
        default="https://api.together.xyz/v1",
        description="Together AI API base URL"
    )
    MODEL_NAME: str = Field(
        default="moonshotai/Kimi-K2-Instruct-0905",
        description="Model name from Together AI catalog"
    )

    # Agent Configuration
    AGENT_MAX_ITERATIONS: int = Field(default=10, description="Max iterations for agent reasoning")
    AGENT_TIMEOUT: int = Field(default=300, description="Agent timeout in seconds")

    # CORS Configuration
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000"],
        description="Allowed CORS origins"
    )

    def get_openai_client_config(self) -> Dict[str, Any]:
        """
        Returns configuration for OpenAI-compatible client (Together AI).

        Together AI provides an OpenAI-compatible API, so we can use the OpenAI client.

        Returns:
            Dict with api_key and base_url for openai.OpenAI() initialization

        Example usage:
            ```python
            import openai
            from app.core.config import settings

            config = settings.get_openai_client_config()
            client = openai.OpenAI(**config)
            ```
        """
        return {
            "api_key": self.TOGETHER_API_KEY,
            "base_url": self.TOGETHER_BASE_URL,
        }

    def get_agent_spec_llm_config(self) -> Dict[str, Any]:
        """
        Returns a configuration dictionary ready for pyagentspec LLM initialization.

        Since Together AI uses OpenAI-compatible API, use OpenAiConfig from pyagentspec.

        Returns:
            Dict with provider-specific configuration

        Example usage with pyagentspec:
            ```python
            from pyagentspec import OpenAiConfig

            config_dict = settings.get_agent_spec_llm_config()
            llm_config = OpenAiConfig(**config_dict)
            ```
        """
        return {
            "name": "TogetherAI_Agent",
            "model_id": self.MODEL_NAME,
            "url": self.TOGETHER_BASE_URL,
        }


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to ensure settings are loaded only once.
    """
    return Settings()


# Global settings instance for easy import
settings = get_settings()
