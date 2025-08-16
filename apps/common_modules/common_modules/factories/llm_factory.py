from typing import TypedDict, Required, NotRequired
from enum import Enum
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.rate_limiters import InMemoryRateLimiter


class LLMFactory:
    class Config(TypedDict):
        model_name: Required[str]
        api_key: Required[str]
        model_region: NotRequired[str]
        api_endpoint: NotRequired[str]
        provider_key: NotRequired[str]
        max_completion_tokens: NotRequired[int]
        temperature: NotRequired[float]
        max_retries: NotRequired[int]
        timeout: NotRequired[float]
        rate_limiter: NotRequired[InMemoryRateLimiter]
        top_p: NotRequired[float]

    class Provider(Enum):
        OPENAI = "openai"
        GEMINI = "gemini"
        BEDROCK = "bedrock"
        DEEPSEEK = "deepseek"
        BEDROCK_EMBEDDINGS = "bedrock_embeddings"

    @staticmethod
    def create_llm(llm_provider: Provider, config: Config) -> BaseChatModel:
        if llm_provider == LLMFactory.Provider.OPENAI:
            from langchain_openai import ChatOpenAI

            kwargs = {
                "model": config["model_name"],
                "api_key": config["api_key"],
            }

            if "api_endpoint" in config:
                kwargs["base_url"] = config["api_endpoint"]
            if "max_completion_tokens" in config:
                kwargs["max_tokens"] = config["max_completion_tokens"]
            if "temperature" in config:
                kwargs["temperature"] = config["temperature"]
            if "max_retries" in config:
                kwargs["max_retries"] = config["max_retries"]
            if "timeout" in config:
                kwargs["timeout"] = config["timeout"]

            return ChatOpenAI(**kwargs)

        if llm_provider == LLMFactory.Provider.GEMINI:
            from langchain_google_genai import ChatGoogleGenerativeAI

            kwargs = {
                "model": config["model_name"],
                "google_api_key": config["api_key"],
            }

            if "max_completion_tokens" in config:
                kwargs["max_output_tokens"] = config["max_completion_tokens"]
            if "temperature" in config:
                kwargs["temperature"] = config["temperature"]
            if "max_retries" in config:
                kwargs["max_retries"] = config["max_retries"]
            if "timeout" in config:
                kwargs["timeout"] = config["timeout"]
            if "rate_limiter" in config:
                kwargs["rate_limiter"] = config["rate_limiter"]
            if "top_p" in config:
                kwargs["top_p"] = config["top_p"]

            return ChatGoogleGenerativeAI(**kwargs)

        if llm_provider == LLMFactory.Provider.BEDROCK:
            from langchain_aws import ChatBedrockConverse

            kwargs = {
                "model_id": config["model_name"],
                "aws_access_key_id": config["provider_key"],
                "aws_secret_access_key": config["api_key"],
                "region_name": config["model_region"],
            }

            if "max_completion_tokens" in config:
                kwargs["max_tokens"] = config["max_completion_tokens"]
            if "temperature" in config:
                kwargs["temperature"] = config["temperature"]

            return ChatBedrockConverse(**kwargs)

        if llm_provider == LLMFactory.Provider.DEEPSEEK:
            from langchain_deepseek import ChatDeepSeek

            kwargs = {
                "model": config["model_name"],
                "api_key": config["api_key"],
            }

            if "max_completion_tokens" in config:
                kwargs["max_tokens"] = config["max_completion_tokens"]
            if "temperature" in config:
                kwargs["temperature"] = config["temperature"]

            return ChatDeepSeek(**kwargs)

        if llm_provider == LLMFactory.Provider.BEDROCK_EMBEDDINGS:
            from langchain_aws.embeddings import BedrockEmbeddings

            kwargs = {
                "model_id": config["model_name"],
                "aws_access_key_id": config["provider_key"],
                "aws_secret_access_key": config["api_key"],
                "region_name": config["model_region"],
            }

            return BedrockEmbeddings(**kwargs)

        if llm_provider not in LLMFactory.Provider:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}. Supported providers are: {list(LLMFactory.Provider)}")
