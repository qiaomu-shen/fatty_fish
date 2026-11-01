"""可重复的离线演示，不联网、不消耗 API 额度。"""

from wechat_chatbot.domain import ChatMessage


class DemoClient:
    def reply(self, messages: list[ChatMessage]) -> str:
        user_messages = [message for message in messages if message.role == "user"]
        return (
            f"[离线演示] 收到：{user_messages[-1].content}（上下文含 {len(user_messages)} 轮输入）"
        )
