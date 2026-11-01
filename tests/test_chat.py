from pathlib import Path

import pytest

from wechat_chatbot.core.chat import ChatService
from wechat_chatbot.domain import ChatMessage
from wechat_chatbot.memory.sqlite_store import HistoryStore


class RecordingModel:
    def __init__(self) -> None:
        self.messages: list[ChatMessage] = []

    def reply(self, messages: list[ChatMessage]) -> str:
        self.messages = messages
        return "测试回复"


def test_context_contains_persona_and_previous_exchange(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "chat.db")
    store.save_exchange("alice", "我喜欢科幻", "记住这个话题了")
    model = RecordingModel()
    service = ChatService(model, store, "你叫小岚")

    assert service.reply("alice", "继续聊聊") == "测试回复"
    assert model.messages == [
        ChatMessage("system", "你叫小岚"),
        ChatMessage("user", "我喜欢科幻"),
        ChatMessage("assistant", "记住这个话题了"),
        ChatMessage("user", "继续聊聊"),
    ]


def test_history_persists_and_is_separated_by_user(tmp_path: Path) -> None:
    path = tmp_path / "chat.db"
    store = HistoryStore(path)
    store.save_exchange("alice", "Alice 的消息", "Alice 的回复")
    store.save_exchange("bob", "Bob 的消息", "Bob 的回复")

    reopened = HistoryStore(path)
    assert [message.content for message in reopened.recent("alice")] == [
        "Alice 的消息",
        "Alice 的回复",
    ]
    assert len(reopened.recent("bob")) == 2
    assert reopened.recent("unknown") == []


def test_model_failure_does_not_leave_half_an_exchange(tmp_path: Path) -> None:
    class FailingModel:
        def reply(self, messages: list[ChatMessage]) -> str:
            raise RuntimeError("模拟 API 失败")

    store = HistoryStore(tmp_path / "chat.db")
    service = ChatService(FailingModel(), store, "人设")
    with pytest.raises(RuntimeError, match="模拟 API 失败"):
        service.reply("alice", "这条消息没有成功")
    assert store.recent("alice") == []
