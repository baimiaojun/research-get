"""
摘要生成器基类
"""
from abc import ABC, abstractmethod
from typing import List
from src.fetchers.base import Paper


class BaseSummarizer(ABC):
    """摘要生成器抽象基类"""

    def __init__(self, summarizer_name: str):
        """
        初始化

        Args:
            summarizer_name: 摘要生成器名称
        """
        self.summarizer_name = summarizer_name

    @abstractmethod
    async def summarize(self, paper: Paper) -> str:
        """
        生成单篇论文摘要

        Args:
            paper: 论文对象

        Returns:
            中文摘要
        """
        pass

    @abstractmethod
    async def summarize_batch(self, papers: List[Paper]) -> List[str]:
        """
        批量生成论文摘要

        Args:
            papers: 论文列表

        Returns:
            摘要列表（与论文列表顺序对应）
        """
        pass
