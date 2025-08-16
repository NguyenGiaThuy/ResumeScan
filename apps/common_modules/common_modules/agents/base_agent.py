from abc import ABC
from logging import Logger
from typing import Callable
from langchain_core.language_models.chat_models import BaseChatModel


class BaseAgent(ABC):
    def __init__(self, name: str, llm: BaseChatModel, tools: list[Callable]):
        super().__init__()
        self.name = name
        self.llm = llm
        self.tools = tools
        self.logger = Logger(self.name)