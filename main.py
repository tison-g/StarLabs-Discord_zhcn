from loguru import logger
import urllib3
import sys
import asyncio

from process import start

# 主函数
async def main():
    configuration()
    await start()

# 配置函数
def configuration():
    urllib3.disable_warnings()  # 禁用警告
    logger.remove()  # 移除默认日志记录
    logger.add(
        sys.stdout,
        colorize=True,
        format="<light-cyan>{time:HH:mm:ss}</light-cyan> | <level>{level: <8}</level> | <fg #ffffff>{name}:{line}</fg #ffffff> - <bold>{message}</bold>",
    )

if __name__ == "__main__":
    asyncio.run(main())  # 运行主函数