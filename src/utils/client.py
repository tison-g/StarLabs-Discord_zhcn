from curl_cffi.requests import AsyncSession

async def create_client(proxy: str) -> AsyncSession:
    """
    创建一个异步HTTP客户端会话
    :param proxy: 代理服务器地址
    :return: 配置好的异步会话对象
    """
    # 创建会话对象
    session = AsyncSession(
                impersonate="chrome131",  # 模拟Chrome 131浏览器
                verify=False,             # 禁用SSL验证
                timeout=60,               # 设置超时时间为60秒
            )
    
    # 如果提供了代理，设置代理
    if proxy:
        session.proxies.update({
            "http": "http://" + proxy,
            "https": "http://" + proxy,
        })

    # 更新请求头
    session.headers.update(HEADERS)
    return session

# 默认请求头
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7,zh-TW;q=0.6,zh;q=0.5',
    'content-type': 'application/json',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}