# 微信聊天机器人：初始工程

Windows + VS Code + Python + uv。先读懂并调试自己的聊天核心，再接入微信。

## 第一次运行

打开本目录中的 `wechat-chatbot.code-workspace`，按 F5，选择
“01 - 离线演示聊天”。在下方集成终端输入消息，`/quit` 退出。
离线演示用于观察数据流，回复是固定规则生成的，不会消耗 API 额度。

终端中也可以运行：

```powershell
uv run wechat-chatbot --mode demo
uv run wechat-chatbot --mode demo --message "你好"
```

## 调用 DeepSeek

本地 `.env` 已预留，填写自己的 `DEEPSEEK_API_KEY`。默认端点是 DeepSeek 官方，
模型为 `deepseek-v4-pro`；如果使用第三方服务商，需核对其端点和模型标识。
之后选择调试配置 03，或手动运行：

```powershell
uv run wechat-chatbot --mode deepseek
```

密钥、聊天数据、日志和虚拟环境已被 `.gitignore` 排除。安装验证只使用离线演示和模拟 HTTP，
尚未替你调用真实 API 或绑定微信。

## 阅读顺序

1. `src/wechat_chatbot/app.py`：启动和组装。
2. `core/chat.py`：一轮聊天的完整流程。
3. `models/demo.py` / `models/deepseek.py`：替换模型实现。
4. `memory/sqlite_store.py`：历史记录如何保存与恢复。
5. `persona/`：人设、资料和手工长期记忆。
6. `channels/` / `proactive/`：当前终端入口，以及后续微信和主动聊天扩展位置。

更多说明：`docs/architecture.md`、`docs/debugging.md`、`docs/wechat-integration.md`。

## 开发命令

```powershell
uv sync --frozen
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
```

也可以按 Ctrl+Shift+B 执行全部检查。项目虚拟环境位于 `.venv`；工具安装在
`D:\DevTools`，Python 运行时由 uv 管理。VS Code 已配置项目解释器和 Python 开发扩展。

## 当前范围

可运行：离线演示、DeepSeek 客户端、连续对话、人设加载、SQLite 历史、调试和测试。
待后续实现：微信登录收发、自动长期记忆、主动消息、后台常驻。

初始代码和文档不使用 Linux 专用 API，不需要 Docker、ROS2、CUDA 或 OpenClaw。
