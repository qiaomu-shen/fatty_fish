from wechat_chatbot.domain import ChatMessage
from wechat_chatbot.memory.sqlite_store import HistoryStore
from wechat_chatbot.models.base import ModelClient


class ChatService:
    def __init__(self, model: ModelClient, history: HistoryStore, persona: str) -> None:
        self.model = model
        self.history = history
        self.persona = persona

    def reply(self, user_id: str, text: str) -> str:
        text = text.strip()
        if not text:
            raise ValueError("消息不能为空。")

        # 第一个建议的断点：检查当前用户和数据库中取出的上下文。
        recent_history = self.history.recent(user_id, limit=20)
        messages = [
            ChatMessage(role="system", content=self.persona),
            *recent_history,
            ChatMessage(role="user", content=text),
        ]
        answer = self.model.reply(messages)
        # 生成成功后，将这一轮的问答放在同一个事务中保存。
        self.history.save_exchange(user_id, text, answer)
        return answer
