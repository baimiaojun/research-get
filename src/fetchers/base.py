"""
数据获取基础模块
定义Paper数据模型和BaseFetcher抽象基类
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Paper:
    """论文数据模型"""

    title: str  # 论文标题
    authors: List[str]  # 作者列表
    abstract: str  # 摘要
    url: str  # 论文链接
    published_date: datetime  # 发表日期
    source: str  # 数据来源（arxiv, paperswithcode, huggingface）

    # 可选字段
    pdf_url: Optional[str] = None  # PDF下载链接
    categories: List[str] = field(default_factory=list)  # 分类标签
    arxiv_id: Optional[str] = None  # arXiv ID
    code_url: Optional[str] = None  # 代码链接
    summary: Optional[str] = None  # AI生成的中文摘要

    def __post_init__(self):
        """数据验证"""
        if not self.title:
            raise ValueError("论文标题不能为空")
        if not self.abstract:
            raise ValueError("论文摘要不能为空")
        if not self.url:
            raise ValueError("论文链接不能为空")

    def get_id(self) -> str:
        """
        获取论文唯一标识符

        Returns:
            论文ID（优先使用arXiv ID，否则使用URL）
        """
        return self.arxiv_id or self.url

    def to_dict(self) -> dict:
        """
        转换为字典

        Returns:
            论文信息字典
        """
        return {
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "url": self.url,
            "pdf_url": self.pdf_url,
            "published_date": self.published_date.isoformat(),
            "categories": self.categories,
            "arxiv_id": self.arxiv_id,
            "code_url": self.code_url,
            "source": self.source,
            "summary": self.summary,
        }

    def __str__(self) -> str:
        """字符串表示"""
        authors_str = ", ".join(self.authors[:3])
        if len(self.authors) > 3:
            authors_str += f" et al. ({len(self.authors)} authors)"
        return f"[{self.source}] {self.title} - {authors_str}"


class BaseFetcher(ABC):
    """数据获取器抽象基类"""

    def __init__(self, source_name: str):
        """
        初始化

        Args:
            source_name: 数据源名称
        """
        self.source_name = source_name

    @abstractmethod
    async def fetch_papers(self, days: int = 1) -> List[Paper]:
        """
        获取论文（异步方法）

        Args:
            days: 获取最近几天的论文

        Returns:
            论文列表
        """
        pass

    def _validate_papers(self, papers: List[Paper]) -> List[Paper]:
        """
        验证论文数据

        Args:
            papers: 论文列表

        Returns:
            验证通过的论文列表
        """
        valid_papers = []
        for paper in papers:
            try:
                # 基本验证已在Paper.__post_init__中完成
                valid_papers.append(paper)
            except Exception as e:
                # 跳过无效论文
                continue
        return valid_papers
