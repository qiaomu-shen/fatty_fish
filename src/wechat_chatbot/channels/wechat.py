"""微信接入预留位置，当前尚未实现登录、收发或凭证保存。

后续适配器负责：
1. 将微信入站事件转换成 user_id 和 text。
2. 调用 ChatService.reply(user_id, text)。
3. 使用真实账号、收件人和会话凭证投递 answer。

接入验证通过前，不在这里假定官方 OpenClaw 插件可以独立运行。
"""
