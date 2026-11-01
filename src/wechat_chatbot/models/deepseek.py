"""直接发送 HTTP 请求，便于观察 API 的 URL、请求体和响应结构。"""

from dataclasses import asdict

import httpx

from wechat_chatbot.domain import ChatMessage


class DeepSeekClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.deepseek.com",
        model: str = "deepseek-v4-pro",
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("请先在项目的 .env 文件中填写 DEEPSEEK_API_KEY。")
        self._api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.transport = transport

    def reply(self, messages: list[ChatMessage]) -> str:
        # 调试点：检查模型实际收到的人设、历史和本轮输入。
        payload = {
            "model": self.model,
            "messages": [asdict(message) for message in messages],
            "thinking": {"type": "disabled"},
            "stream": False,
            "max_tokens": 512,
        }
        try:
            with httpx.Client(
                timeout=httpx.Timeout(60.0, connect=10.0), transport=self.transport
            ) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self._api_key}"},
                    json=payload,
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            # 不直接打印服务端响应体或 Authorization，避免凭证进入终端日志。
            raise RuntimeError(
                f"DeepSeek 请求失败（HTTP {exc.response.status_code}）。"
                "请检查密钥、余额、模型名和端点配置。"
            ) from None
        except httpx.RequestError:
            raise RuntimeError("DeepSeek 网络请求失败，请检查网络、代理和端点配置。") from None

        try:
            content = response.json()["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError):
            raise RuntimeError("DeepSeek 返回的数据结构不符合预期。") from None
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("DeepSeek 返回了空回复。")
        return content.strip()
