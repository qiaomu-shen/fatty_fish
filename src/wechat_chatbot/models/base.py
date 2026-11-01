from typing import Protocol

from wechat_chatbot.domain import ChatMessage


class ModelClient(Protocol):
    def reply(self, messages: list[ChatMessage]) -> str:
        """根据完整上下文生成一条回复。"""
        ...
