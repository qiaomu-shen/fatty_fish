from wechat_chatbot.core.chat import ChatService


def run_console(service: ChatService, user_id: str) -> None:
    print("输入消息后回车；输入 /quit 退出。")
    while True:
        try:
            text = input("你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n聊天已结束。")
            return
        if text == "/quit":
            return
        if not text:
            continue
        try:
            print(f"小岚 > {service.reply(user_id, text)}")
        except (RuntimeError, ValueError) as exc:
            print(f"错误：{exc}")
