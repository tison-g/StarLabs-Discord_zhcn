import asyncio
import random
import aiohttp
from loguru import logger

from src.utils.config import Config
from src.utils.constants import Account


async def leave_guild(account: Account, config: Config, guild_id: str) -> bool:
    for retry in range(config.SETTINGS.ATTEMPTS):
        """
        离开Discord公会

        参数:
            token: Discord令牌
            guild_id: 要离开的公会ID
            proxy: 格式为 user:pass@ip:port 的代理
        """
        headers = {
            "sec-ch-ua-platform": '"Windows"',
            "Authorization": account.token,
            "X-Debug-Options": "bugReporterEnabled",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "X-Discord-Timezone": "Etc/GMT-2",
            "X-Discord-Locale": "en-US",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
        }

        try:
            # 配置带有身份验证的代理
            if account.proxy:
                proxy_auth = None
                if "@" in account.proxy:
                    auth, proxy = account.proxy.split("@")
                    user, pwd = auth.split(":")
                    proxy_auth = aiohttp.BasicAuth(user, pwd)
                    proxy_url = f"http://{proxy}"
                else:
                    proxy_url = f"http://{account.proxy}"
            else:
                proxy_url = None
                proxy_auth = None

            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    f"https://discord.com/api/v9/users/@me/guilds/{guild_id}",
                    headers=headers,
                    json={"lurking": False},  # 这个参数有时需要 Discord
                    proxy=proxy_url,
                    proxy_auth=proxy_auth,
                    ssl=False,  # 禁用SSL以使用代理
                ) as response:

                    if response.status in [
                        200,
                        204,
                    ]:  # Discord可能会在成功时返回这两个状态码
                        logger.success(
                            f"{account.index} | 成功离开公会 {guild_id}"
                        )
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(
                            f"{account.index} | 离开公会 {guild_id} 失败。状态: {response.status}, 响应: {error_text}"
                        )
                        return False

        except Exception as e:
            random_pause = random.randint(
                config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
                config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
            )
            logger.error(
                f"{account.index} | 离开公会 {guild_id} 时出错: {str(e)}。暂停 {random_pause} 秒。"
            )
            await asyncio.sleep(random_pause)

    return False