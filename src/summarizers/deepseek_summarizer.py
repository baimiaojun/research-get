"""
DeepSeek AI摘要生成模块
使用DeepSeek API生成中文论文摘要（支持国内支付）
"""
import yaml
import asyncio
import aiohttp
from pathlib import Path
from typing import List
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from src.fetchers.base import Paper
from src.summarizers.base import BaseSummarizer
from src.utils.logger import get_logger

logger = get_logger()


class DeepSeekSummarizer(BaseSummarizer):
    """DeepSeek AI摘要生成器"""

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek-chat",
        max_tokens: int = 200,
        temperature: float = 0.7,
        prompts_file: str = "config/prompts.yml",
    ):
        """
        初始化

        Args:
            api_key: DeepSeek API密钥
            model: 模型名称（deepseek-chat 或 deepseek-coder）
            max_tokens: 最大token数
            temperature: 生成温度
            prompts_file: 提示词配置文件
        """
        super().__init__("deepseek")

        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.base_url = "https://api.deepseek.com/v1/chat/completions"

        # 加载提示词模板
        self.prompts = self._load_prompts(prompts_file)

        logger.info(f"DeepSeek摘要生成器已初始化")
        logger.info(f"  - 模型: {model}")
        logger.info(f"  - Max tokens: {max_tokens}")

    def _load_prompts(self, prompts_file: str) -> dict:
        """
        加载提示词配置

        Args:
            prompts_file: 提示词文件路径

        Returns:
            提示词字典
        """
        try:
            with open(Path(prompts_file), "r", encoding="utf-8") as f:
                prompts = yaml.safe_load(f)
            logger.info(f"成功加载提示词配置: {prompts_file}")
            return prompts
        except Exception as e:
            logger.error(f"加载提示词配置失败: {e}")
            # 返回默认提示词
            return {
                "summarize_paper": (
                    "请用中文简洁总结以下学术论文（150字以内）：\n\n"
                    "标题：{title}\n摘要：{abstract}\n\n"
                    "请直接给出总结，不要包含前缀。"
                )
            }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
    )
    async def summarize(self, paper: Paper) -> str:
        """
        生成单篇论文摘要（带重试机制）

        Args:
            paper: 论文对象

        Returns:
            中文摘要
        """
        try:
            # 构建提示词
            prompt_template = self.prompts.get("summarize_paper", "")
            prompt = prompt_template.format(
                title=paper.title,
                abstract=paper.abstract[:1000],  # 限制摘要长度避免过长
            )

            # 调用DeepSeek API
            logger.debug(f"正在生成摘要: {paper.title[:50]}...")

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"DeepSeek API错误 ({response.status}): {error_text}")
                        raise Exception(f"API请求失败: {response.status}")

                    result = await response.json()

                    # 提取摘要
                    summary = result["choices"][0]["message"]["content"].strip()

                    logger.debug(f"摘要生成成功: {summary[:50]}...")

                    return summary

        except Exception as e:
            logger.error(f"生成摘要失败 ({paper.title[:50]}...): {e}")
            # 返回原始摘要的前150字作为备用
            return paper.abstract[:150] + "..."

    async def summarize_batch(self, papers: List[Paper]) -> List[str]:
        """
        批量生成论文摘要（并发执行）

        Args:
            papers: 论文列表

        Returns:
            摘要列表
        """
        logger.info(f"开始批量生成 {len(papers)} 篇论文的摘要")

        # 并发执行
        tasks = [self.summarize(paper) for paper in papers]
        summaries = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理异常结果
        processed_summaries = []
        for i, summary in enumerate(summaries):
            if isinstance(summary, Exception):
                logger.error(f"第{i+1}篇论文摘要生成失败: {summary}")
                # 使用原始摘要作为备用
                processed_summaries.append(papers[i].abstract[:150] + "...")
            else:
                processed_summaries.append(summary)

        logger.info(f"批量摘要生成完成")
        return processed_summaries

    async def summarize_and_update(self, papers: List[Paper]) -> List[Paper]:
        """
        生成摘要并更新Paper对象

        Args:
            papers: 论文列表

        Returns:
            更新后的论文列表
        """
        summaries = await self.summarize_batch(papers)

        # 更新Paper对象
        for paper, summary in zip(papers, summaries):
            paper.summary = summary

        return papers
