from typing import final

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from typing_extensions import Callable

from app.config import llm_config

_BuilderFn = Callable[[str, str], BaseChatModel]

_PROVIDERS: dict[str, _BuilderFn] = {
    "openai": lambda api_key, model: ChatOpenAI(api_key=SecretStr(api_key), model=model)
}


@final
class LLMFactory:
    def __init__(self):
        self.llm_config = llm_config.get_llm_config()

    def get_llm(self):
        provider = self.llm_config["provider"]
        builder = _PROVIDERS.get(provider)

        if not builder:
            raise ValueError(f"Unsopported LLM provider: {provider}")

        return builder(self.llm_config["api_key"], self.llm_config["model"])


llm_factory = LLMFactory()
