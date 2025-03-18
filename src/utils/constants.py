from dataclasses import dataclass

# 文件路径常量
ACCOUNTS_FILE = "data/accounts.csv"

# Discord验证码站点密钥
DISCORD_CAPTCHA_SITEKEY = "a9b5fb07-92ff-493f-86fe-352a2803b3df"

@dataclass
class Account:
    """
    用于存储Discord账号数据的类
    """
    index: int                  # 账号索引
    token: str                  # Discord令牌
    proxy: str                  # 代理地址
    username: str               # 用户名
    status: str                 # 账号状态
    password: str               # 密码
    new_password: str           # 新密码
    new_name: str              # 新显示名称
    new_username: str          # 新用户名
    messages_to_send: list[str] # 要发送的消息列表

@dataclass
class DataForTasks:
    """
    用于存储任务数据的类
    """
    LEAVE_GUILD_IDS: list[str]                # 要离开的服务器ID列表
    PROFILE_PICTURES: list[str]               # 个人头像图片列表
    EMOJIS_INFO: list[dict]                   # 表情符号信息列表
    INVITE_CODE: str | None                   # 邀请码
    REACTION_CHANNEL_ID: str | None           # 反应频道ID
    REACTION_MESSAGE_ID: str | None           # 反应消息ID
    IF_TOKEN_IN_GUILD_ID: str | None          # 检查令牌是否在指定服务器ID
    BUTTON_PRESSER_BUTTON_DATA: dict | None   # 按钮数据
    BUTTON_PRESSER_APPLICATION_ID: str | None # 按钮应用ID
    BUTTON_PRESSER_GUILD_ID: str | None       # 按钮所在服务器ID
    BUTTON_PRESSER_CHANNEL_ID: str | None     # 按钮所在频道ID
    BUTTON_PRESSER_MESSAGE_ID: str | None     # 按钮所在消息ID

# 主菜单选项
MAIN_MENU_OPTIONS = [
    "AI Chatter",                                    # AI聊天
    "Inviter [Token]",                              # 邀请功能[需要令牌]
    "Press Button [Token]",                         # 按钮点击[需要令牌]
    "Press Reaction [Token]",                       # 添加反应[需要令牌]
    "Change Name [Token]",                          # 更改名称[需要令牌]
    "Change Username [Token + Password]",           # 更改用户名[需要令牌+密码]
    "Change Password [Token + Password]",           # 更改密码[需要令牌+密码]
    "Change Profile Picture [Token]",               # 更改头像[需要令牌]
    "Send message to the channel [Token]",          # 发送频道消息[需要令牌]
    "Token Checker [Token]",                       # 令牌检查器[需要令牌]
    "Leave Guild [Token]",                         # 离开服务器[需要令牌]
    "Show all servers account is in [Token]",      # 显示账号所在的所有服务器[需要令牌]
    "Check if token in specified Guild [Token]",   # 检查令牌是否在指定服务器中[需要令牌]
    "Exit",                                       # 退出
]