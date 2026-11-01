"""渠道、对话核心和模型之间使用的最小数据结构。"""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ChatMessage:
    role: Literal["system", "user", "assistant"]
    content: str
