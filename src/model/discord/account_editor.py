import asyncio
import random
from loguru import logger
from curl_cffi.requests import AsyncSession

from src.model.discord.utils import create_x_super_properties
from src.utils.config import Config
from src.utils.constants import Account
from src.utils.writer import update_account


class AccountEditor:
    def __init__(self, account: Account, config: Config, client: AsyncSession):
        self.account = account
        self.config = config
        self.client = client

    async def change_name(self) -> bool:
        for retry in range(self.config.SETTINGS.ATTEMPTS):
            try:
                headers = {
                    'accept': '*/*',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7,zh-TW;q=0.6,zh;q=0.5',
                    'authorization': self.account.token,
                    'content-type': 'application/json',
                    'origin': 'https://discord.com',
                    'priority': 'u=1, i',
                    'referer': 'https://discord.com/channels/@me',
                    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
                    'x-debug-options': 'bugReporterEnabled',
                    'x-discord-locale': 'en-US',
                    'x-discord-timezone': 'Etc/GMT-2',
                    "x-super-properties": create_x_super_properties()
                    }

                json_data = {
                    'global_name': self.account.new_name,
                }
                
                response = await self.client.patch('https://discord.com/api/v9/users/@me', headers=headers, json=json_data)
                
                if response.status_code == 200 and response.json()['global_name'] == self.account.new_name:
                    logger.success(f"{self.account.index} | 名字已更改为 {self.account.new_name}")
                    return True

            except Exception as e:
                random_sleep = random.randint(self.config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0], self.config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1])
                logger.error(f"{self.account.index} | 更改名字时出错: {e}. 重试中，等待 {random_sleep} 秒...")
                await asyncio.sleep(random_sleep)

        return False
    
    async def change_username(self) -> bool:
        for retry in range(self.config.SETTINGS.ATTEMPTS):
            try:
                headers = {
                    'accept': '*/*',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7,zh-TW;q=0.6,zh;q=0.5',
                    'authorization': self.account.token,
                    'content-type': 'application/json',
                    'origin': 'https://discord.com',
                    'priority': 'u=1, i',
                    'referer': 'https://discord.com/channels/@me',
                    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
                    'x-debug-options': 'bugReporterEnabled',
                    'x-discord-locale': 'en-US',
                    'x-discord-timezone': 'Etc/GMT-2',
                    'x-super-properties': create_x_super_properties(),
                }

                json_data = {
                    'username': self.account.new_username,
                    'password': self.account.password,
                }

                response = await self.client.patch('https://discord.com/api/v9/users/@me', headers=headers, json=json_data)
                
                if response.status_code == 200 and response.json()['username'] == self.account.new_username:
                    await update_account(self.account.token, "USERNAME", self.account.new_username)
                    logger.success(f"{self.account.index} | 用户名已更改为 {self.account.new_username}")
                    return True

            except Exception as e:
                random_sleep = random.randint(self.config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0], self.config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1])
                logger.error(f"{self.account.index} | 更改用户名时出错: {e}. 重试中，等待 {random_sleep} 秒...")
                await asyncio.sleep(random_sleep)

        return False
    
    async def change_password(self) -> bool:
        for retry in range(self.config.SETTINGS.ATTEMPTS):
            try:
                headers = {
                    'accept': '*/*',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7,zh-TW;q=0.6,zh;q=0.5',
                    'authorization': self.account.token,
                    'content-type': 'application/json',
                    'origin': 'https://discord.com',
                    'priority': 'u=1, i',
                    'referer': 'https://discord.com/channels/@me',
                    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
                    'x-debug-options': 'bugReporterEnabled',
                    'x-discord-locale': 'en-US',
                    'x-discord-timezone': 'Etc/GMT-2',
                    'x-super-properties': create_x_super_properties(),
                }

                json_data = {
                    'password': self.account.password,
                    'new_password': self.account.new_password,
                }

                response = await self.client.patch('https://discord.com/api/v9/users/@me', headers=headers, json=json_data)

                if "Password is too weak or common to use." in response.text:
                    logger.error(f"{self.account.index} | 密码 {self.account.new_password} 太弱或太常见，无法使用。")
                    return False
                
                if response.status_code == 200:
                    response_data = response.json()
                    if 'token' in response_data and response_data['token']:
                        await update_account(self.account.token, "DISCORD_TOKEN", response_data['token'])
                        await update_account(self.account.token, "PASSWORD", self.account.new_password)
                        logger.success(f"{self.account.index} | 密码更改成功。令牌已更新。")
                        return True
                    else:
                        logger.warning(f"{self.account.index} | 密码已更改，但未返回令牌。")
                        return True
                else:
                    logger.error(f"{self.account.index} | 更改密码失败。状态: {response.status_code}")

            except Exception as e:
                random_sleep = random.randint(self.config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0], self.config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1])
                logger.error(f"{self.account.index} | 更改密码时出错: {e}. 重试中，等待 {random_sleep} 秒...")
                await asyncio.sleep(random_sleep)

        return False
    
    async def change_profile_picture(self) -> bool:
        for retry in range(self.config.SETTINGS.ATTEMPTS):
            try:
                headers = {
                    'accept': '*/*',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7,zh-TW;q=0.6,zh;q=0.5',
                    'authorization': self.account.token,
                    'content-type': 'application/json',
                    'origin': 'https://discord.com',
                    'priority': 'u=1, i',
                    'referer': 'https://discord.com/channels/@me',
                    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
                    'x-debug-options': 'bugReporterEnabled',
                    'x-discord-locale': 'en-US',
                    'x-discord-timezone': 'Etc/GMT-2',
                    'x-super-properties': create_x_super_properties(),
                   }
                
                if self.config.SETTINGS.RANDOM_PROFILE_PICTURES:
                    profile_picture = random.choice(self.config.DATA_FOR_TASKS.PROFILE_PICTURES)
                else:
                    if len(self.config.DATA_FOR_TASKS.PROFILE_PICTURES) < self.account.index:
                        logger.error(f"{self.account.index} | 个人资料图片数量不足。请在 data/pictures 文件夹中添加更多图片。")
                        return False
                    else:
                        profile_picture = self.config.DATA_FOR_TASKS.PROFILE_PICTURES[self.account.index]

                json_data = {
                    'avatar': f"data:image/png;base64,{profile_picture}",
                }

                response = await self.client.patch('https://discord.com/api/v9/users/@me', headers=headers, json=json_data)
                
                if response.status_code == 200:
                    logger.success(f"{self.account.index} | 个人资料图片已更改!")
                    return True

            except Exception as e:
                random_sleep = random.randint(self.config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0], self.config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1])
                logger.error(f"{self.account.index} | 更改名字时出错: {e}. 重试中，等待 {random_sleep} 秒...")
                await asyncio.sleep(random_sleep)

        return False
