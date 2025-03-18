import asyncio
import random
from loguru import logger
from curl_cffi.requests import AsyncSession

from src.utils.config import Config
from src.utils.constants import Account
from src.model.discord.get_account_info import get_account_info
from src.utils.writer import update_account


async def token_checker(account: Account, config: Config, client: AsyncSession) -> tuple[bool, str] | bool:
        for retry in range(config.SETTINGS.ATTEMPTS):
            try:
                guilds_url = "https://discord.com/api/v9/users/@me/affinities/guilds"
                me_url = "https://discord.com/api/v9/users/@me"

                resp = await client.get(guilds_url, headers={"Authorization": f"{account.token}"})

                if resp.status_code in (401, 403):
                    logger.warning(f"{account.index} | 令牌已锁定: {account.token}")
                    return True, "locked"

                if resp.status_code in (200, 204):
                    response = await client.get(me_url, headers={"Authorization": f"{account.token}"})
                    flags_data = response.json()['flags'] - response.json()['public_flags']
                    if flags_data == 17592186044416:
                        logger.warning(f"{account.index} | 令牌已被隔离: {account.token}")
                        await update_account(account.token, "STATUS", "QUARANTINED")

                        return False, "quarantined"
                    elif flags_data == 1048576:
                        logger.warning(f"{account.index} | 令牌被标记为垃圾邮件发送者: {account.token}")
                        await update_account(account.token, "STATUS", "SPAMMER")
                        
                    elif flags_data == 17592186044416 + 1048576:
                        logger.warning(f"{account.index} | 令牌被标记为垃圾邮件发送者并被隔离: {account.token}")
                        await update_account(account.token, "STATUS", "SPAMMER AND QUARANTINED")

                    logger.success(f"{account.index} | 令牌正常工作!")
                    await update_account(account.token, "STATUS", "OK")

                    if response.json()['username']:
                        try:
                            await update_account(account.token, "USERNAME", response.json()['username'])
                        except Exception as e:
                            logger.error(f"{account.index} | 更新用户名出错: {e}")

                else:
                    logger.error(f"{account.index} | 检查令牌时无效状态码 {resp.status_code}.")

                return True, ""
            except Exception as err:
                random_sleep = random.randint(config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0], config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1])
                logger.error(f"{account.index} | 检查令牌状态失败: {err}. {random_sleep} 秒后重试...")
                await asyncio.sleep(random_sleep)
        
        await update_account(account.token, "STATUS", "UNKNOWN")
        return False, ""