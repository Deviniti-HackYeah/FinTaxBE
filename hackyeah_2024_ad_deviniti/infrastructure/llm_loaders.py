from langchain_core.language_models import BaseChatModel
from langchain_openai import AzureChatOpenAI
from langchain_openai.chat_models.base import BaseChatOpenAI
from pydantic import SecretStr

from hackyeah_2024_ad_deviniti.config.config_models import get_bielik_config, get_azure_config


def get_bielik_2_2(temperature: float = 0.1, max_tokens: int = 200) -> BaseChatModel:
    config = get_bielik_config()
    return BaseChatOpenAI(
        model=config.bielik_model_name,
        base_url=config.bielik_api_url,
        api_key=SecretStr(config.bielik_secret_key),
        temperature=temperature,
        max_tokens=max_tokens
    )


def get_azure_gpt_4o(temperature: float = 0.1, max_tokens: int = 200) -> BaseChatModel:
    config = get_azure_config()
    return AzureChatOpenAI(
        azure_deployment=config.azure_gpt_4o_deployment,
        temperature=temperature,
        max_tokens=max_tokens,
        streaming=False,
    )


def get_azure_gpt_4o_mini(temperature: float = 0.1, max_tokens: int = 200) -> BaseChatModel:
    config = get_azure_config()
    return AzureChatOpenAI(
        azure_deployment=config.azure_gpt_4o_mini_deployment,
        temperature=temperature,
        max_tokens=max_tokens,
        streaming=False,
    )
