import argparse
from pathlib import Path

from wechat_chatbot.channels.console import run_console
from wechat_chatbot.config import load_settings
from wechat_chatbot.core.chat import ChatService
from wechat_chatbot.core.persona import load_persona
from wechat_chatbot.memory.sqlite_store import HistoryStore
from wechat_chatbot.models.base import ModelClient
from wechat_chatbot.models.deepseek import DeepSeekClient
from wechat_chatbot.models.demo import DemoClient


def main() -> int:
    parser = argparse.ArgumentParser(description="微信聊天机器人：可独立调试的初始工程")
    parser.add_argument("--mode", choices=("demo", "deepseek"), default="demo")
    parser.add_argument("--message", help="只处理这一条消息，完成后退出")
    parser.add_argument("--user-id", default="local-user")
    parser.add_argument("--db", type=Path, help="覆盖数据库路径，适合隔离演示和测试")
    args = parser.parse_args()
    settings = load_settings()
    try:
        model: ModelClient
        if args.mode == "deepseek":
            model = DeepSeekClient(settings.api_key, settings.base_url, settings.model)
        else:
            model = DemoClient()
        database_path = args.db or settings.database_path
        service = ChatService(
            model=model,
            history=HistoryStore(database_path),
            persona=load_persona(settings.root / "persona"),
        )
        print(f"模式：{args.mode}；聊天记录：{database_path}")
        if args.message is not None:
            print(f"小岚 > {service.reply(args.user_id, args.message)}")
        else:
            run_console(service, args.user_id)
    except (RuntimeError, ValueError) as exc:
        print(f"启动或请求失败：{exc}")
        return 1
    return 0
