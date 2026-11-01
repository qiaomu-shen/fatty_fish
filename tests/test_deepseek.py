import json

import httpx
import pytest

from wechat_chatbot.domain import ChatMessage
from wechat_chatbot.models.deepseek import DeepSeekClient


def test_request_payload_without_real_network() -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://api.deepseek.com/chat/completions"
        assert request.headers["Authorization"] == "Bearer test-only-key"
        payload = json.loads(request.content)
        assert payload["model"] == "deepseek-v4-pro"
        assert payload["messages"] == [{"role": "user", "content": "你好"}]
        assert payload["thinking"] == {"type": "disabled"}
        return httpx.Response(200, json={"choices": [{"message": {"content": "你好呀"}}]})

    client = DeepSeekClient("test-only-key", transport=httpx.MockTransport(handle))
    assert client.reply([ChatMessage("user", "你好")]) == "你好呀"


def test_api_errors_do_not_include_server_body_or_key() -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": "test-only-secret"})

    client = DeepSeekClient("test-only-secret", transport=httpx.MockTransport(handle))
    with pytest.raises(RuntimeError, match="HTTP 401") as caught:
        client.reply([ChatMessage("user", "你好")])
    assert "test-only-secret" not in str(caught.value)


def test_missing_key_fails_before_any_request() -> None:
    with pytest.raises(ValueError, match="DEEPSEEK_API_KEY"):
        DeepSeekClient("")
