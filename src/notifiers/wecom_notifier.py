"""
企业微信推送模块
使用企业微信群机器人Webhook发送消息
"""
import aiohttp
import asyncio
from typing import Optional
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from src.utils.logger import get_logger

logger = get_logger()


class WeComNotifier:
    """企业微信通知器"""

    def __init__(self, webhook_url: str):
        """
        初始化

        Args:
            webhook_url: 企业微信Webhook URL
        """
        self.webhook_url = webhook_url
        logger.info("企业微信通知器已初始化")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
    )
    async def send_markdown(self, content: str) -> bool:
        """
        发送Markdown消息（带重试机制）

        Args:
            content: Markdown内容

        Returns:
            是否发送成功
        """
        try:
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "content": content
                }
            }

            logger.info("正在发送企业微信消息...")

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    result = await response.json()

                    if result.get("errcode") == 0:
                        logger.info("✅ 企业微信消息发送成功")
                        return True
                    else:
                        error_msg = result.get("errmsg", "未知错误")
                        logger.error(f"企业微信消息发送失败: {error_msg}")
                        logger.error(f"错误码: {result.get('errcode')}")
                        return False

        except asyncio.TimeoutError:
            logger.error("企业微信消息发送超时")
            raise
        except aiohttp.ClientError as e:
            logger.error(f"网络请求失败: {e}")
            raise
        except Exception as e:
            logger.error(f"发送消息时发生错误: {e}")
            raise

    async def send_text(self, content: str) -> bool:
        """
        发送纯文本消息

        Args:
            content: 文本内容

        Returns:
            是否发送成功
        """
        try:
            payload = {
                "msgtype": "text",
                "text": {
                    "content": content
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    result = await response.json()

                    if result.get("errcode") == 0:
                        logger.info("✅ 文本消息发送成功")
                        return True
                    else:
                        error_msg = result.get("errmsg", "未知错误")
                        logger.error(f"文本消息发送失败: {error_msg}")
                        return False

        except Exception as e:
            logger.error(f"发送文本消息失败: {e}")
            return False

    async def test_connection(self) -> bool:
        """
        测试Webhook连接

        Returns:
            是否连接成功
        """
        logger.info("测试企业微信Webhook连接...")

        test_message = "✅ 学术推送系统配置成功！\n\n测试消息发送成功，系统运行正常。"

        return await self.send_text(test_message)
