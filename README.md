# Discord 自动化机器人 2.0 🤖

一个功能强大且灵活的 Discord 自动化工具，具有多种功能和并行处理能力。

## 🌟 功能
- ✨ 多线程处理
- 🔄 配置重试次数的自动重试
- 🔐 代理支持
- 📝 基于 Excel 的账户管理
- 🎭 与 GPT-4 集成的 AI 聊天
- 🔒 使用线程安全操作的安全文件处理
- 📊 详细的日志系统

### 🎯 可用操作：
- AI 聊天
- 服务器邀请
- 按钮交互
- 反应管理
- 个人资料定制：
  - 更改姓名
  - 更新用户名
  - 更新密码
  - 更改头像
- 消息管理（聊天 + 即时删除）
- 令牌验证
- 服务器管理：
  - 离开公会
  - 服务器列表
  - 公会存在性检查

## 📋 要求
- Python 3.11.6 或更高版本
- 具有 Discord 账户的 Excel 文件
- 有效的 Discord 令牌
- （可选）代理
- 用于 AI 聊天功能的 OpenAI API 密钥

## 🚀 安装

1. 克隆仓库：
```bash
git clone https://github.com/0xStarLabs/StarLabs-Discord.git
cd StarLabs-Discord
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 在 `config.yaml` 中配置您的设置

## 📁 项目结构
```
StarLabs-Discord/
├── data/
│   ├── accounts.xlsx     # Discord 账户数据
│   ├── messages/         # 消息模板
│   └── pictures/         # 个人资料图片
├── src/
│   └── utils/
│       ├── constants.py  # 配置常量
│       ├── reader.py     # 文件处理工具
│       └── ...
└── config.yaml          # 主配置文件
```


## 📝 配置

### 1. accounts.xlsx 结构
| 列             | 示例       | 描述                     |
|---------------|-----------|--------------------------|
| DISCORD_TOKEN | token1    | Discord 账户令牌         |
| PROXY         | proxy1    | 代理地址（可选）         |
| USERNAME      | user1     | 账户用户名               |
| STATUS        | VALID     | 账户状态                 |
| PASSWORD      | pass1     | 当前密码                 |
| NEW_PASSWORD  | newpass1  | 新密码                   |
| NEW_NAME      | name1     | 新显示名称               |
| NEW_USERNAME  | username1 | 新用户名                 |
| MESSAGES_FILE | messages1 | 自定义消息文件           |


### 2. config.yaml 设置
```yaml
SETTINGS:
  THREADS: 1                      # 并行线程数
  ATTEMPTS: 5                     # 失败操作的重试次数
  SHUFFLE_ACCOUNTS: true          # 随机化账户处理顺序
  PAUSE_BETWEEN_ATTEMPTS: [1, 2]  # 重试之间的随机暂停时间
  PAUSE_BETWEEN_ACCOUNTS: [1, 2]  # 账户之间的随机暂停时间
```

### 3. AI 聊天配置
```yaml
AI_CHATTER:
  ANSWER_PERCENTAGE: 50           # 响应消息的概率
  REPLY_PERCENTAGE: 50           # 回复消息与新消息的比例
  MESSAGES_TO_SEND_PER_ACCOUNT: [3, 5]
```

## 🎮 使用
1. 准备您的文件：
   - 使用令牌和账户数据填写 `accounts.xlsx`
   - 使用所需的设置配置 `config.yaml`
   - 将消息模板添加到 `data/messages/`
   - 将个人资料图片添加到 `data/pictures/`

2. 运行机器人：
```bash
python main.py
```

## 🤝 支持
- 通过创建问题报告错误或提出功能请求
- 加入我们的社区进行讨论和更新

## 📜 许可证

MIT 许可证

版权 (c) 2024 [您的名字]

在符合以下条件的情况下，特此免费授予任何获得本软件及相关文档文件（“软件”）副本的人员处理软件的权限，包括但不限于使用、复制、修改、合并、出版、分发、再许可及/或销售软件的副本，以及授予被提供软件的人这样做的权利：

上述版权声明和本许可声明应包含在软件的所有副本或主要部分中。

本软件按“原样”提供，不含任何形式的明示或暗示担保，包括但不限于适销性、特定用途适用性和非侵权的担保。在任何情况下，作者或版权持有人均不对因软件或使用或其他交易中的软件而产生的任何索赔、损害或其他责任负责，无论是在合同诉讼、侵权行为或其他情况下。

⚠️ 免责声明
此工具仅用于教育目的。自行承担风险并遵守 Discord 的服务条款使用。