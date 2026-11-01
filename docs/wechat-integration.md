# 微信接入：下一阶段

当前 `channels/wechat.py` 只有职责说明，尚未实现任何账号登录或消息收发。
本工程不会扫描微信客户端、读取其他好友聊天记录或启动定时发送。

接入前先做一个小验证：扫码绑定 → 收一条自己的消息 → 回复一条 → 记录重连行为。
主动发送再分别验证短延时、隔夜和较长未互动后的行为。

腾讯维护的现有微信插件依赖 OpenClaw。后续需要确认采用独立适配还是最小桥接，
不能直接把插件当成可独立运行的 Python 库。无论接法如何，ChatService 保持独立。

适配层须保存真实的账号、收件人和会话凭证；昵称或手机号不能直接当作接口收件人 ID。
每个用户会话须独立保存，不能把不同人的历史拼到同一个上下文。

参考：

- https://github.com/Tencent/openclaw-weixin
- https://github.com/Tencent/openclaw-weixin/blob/main/docs/protocol.md
- https://docs.openclaw.ai/channels/wechat
