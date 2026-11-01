# 在 VS Code 中调试

1. 打开 `wechat-chatbot.code-workspace`。如果出现信任提示，由你确认这是自己的项目。
2. 打开 `src/wechat_chatbot/core/chat.py`，在读取 `recent_history` 的一行按 F9 设置断点。
3. 在“运行和调试”中选择“02 - 单条演示消息”，按 F5。
4. 停下后观察 `user_id`、`text`；按 F10 后检查 `recent_history` 和 `messages`。
5. F10 单步跳过，F11 进入函数，Shift+F11 返回，F5 继续。

第二个观察点是 `models/deepseek.py` 的 `payload`。在真实模式中可以检查请求体，
但不要将 Authorization、密钥或完整调试变量截图公开分享。

调试配置 01/02 不调用 API；配置 03 只有填写 `.env` 后才能调用真实 DeepSeek。
演示模式和真实模式默认使用相同数据库，可用 `--user-id` 或 `--db` 隔离实验。

按 Ctrl+Shift+B 运行 Ruff、格式检查和 pytest。测试也可在左侧测试面板发现和调试。
测试中的 HTTP 使用 `httpx.MockTransport`，不会访问 DeepSeek 或消耗额度。

## 常见问题

- 无法导入包：确认解释器为本项目 `.venv/Scripts/python.exe`，执行 `uv sync --frozen`。
- 断点没有命中：确认选择了本项目调试配置，消息已进入 `ChatService.reply`。
- HTTP 401：检查密钥和服务商；HTTP 402：检查余额；HTTP 429：降低请求频率。
- 网络错误：检查本机网络、代理和 `.env` 中的端点。
- 修改人设没生效：停止本次程序，再重新运行。
- `uv` 命令找不到：重开终端，或使用 `D:\DevTools\uv\uv.exe`。
