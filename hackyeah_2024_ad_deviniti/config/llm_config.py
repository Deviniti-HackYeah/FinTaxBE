import os

from openai import BaseModel


class BielikConfig(BaseModel):
    bielik_api_url: str
    bielik_model_name: str
    bielik_secret_key: str


class AzureConfig(BaseModel):
    azure_openai_url: str
    azure_openai_secret_key: str
    azure_model_api_version: str
    azure_gpt_4o_deployment: str
    azure_gpt_4o_mini_deployment: str


def get_bielik_config() -> BielikConfig:
    return BielikConfig(
        bielik_api_url=os.environ['BIELIK_BASE_URL_2_2'],
        bielik_model_name=os.environ['BIELIK_MODEL_2_2'],
        bielik_secret_key=os.environ['BIELIK_API_KEY_2_2']
    )


def get_azure_config() -> AzureConfig:
    return AzureConfig(
        azure_openai_url=os.environ['AZURE_OPENAI_API_KEY'],
        azure_openai_secret_key=os.environ['AZURE_OPENAI_ENDPOINT'],
        azure_model_api_version=os.environ['OPENAI_API_VERSION'],
        azure_gpt_4o_deployment=os.environ['AZURE_GPT_4O_DEPLOYMENT'],
        azure_gpt_4o_mini_deployment=os.environ['AZURE_GPT_4O_MINI_DEPLOYMENT']
    )
