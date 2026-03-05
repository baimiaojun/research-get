"""
arXiv数据获取模块
使用arXiv官方Python库获取最新论文
"""
import arxiv
from datetime import datetime, timedelta
from typing import List
from src.fetchers.base import Paper, BaseFetcher
from src.utils.logger import get_logger

logger = get_logger()


class ArxivFetcher(BaseFetcher):
    """arXiv论文获取器"""

    def __init__(self, max_results: int = 50):
        """
        初始化

        Args:
            max_results: 最大结果数
        """
        super().__init__("arxiv")
        self.max_results = max_results

        # arXiv分类（机器学习和信贷风控相关）
        self.categories = [
            "cs.LG",  # Machine Learning
            "cs.AI",  # Artificial Intelligence
            "stat.ML",  # Machine Learning (Statistics)
            "q-fin.RM",  # Quantitative Finance - Risk Management
            "q-fin.ST",  # Quantitative Finance - Statistical Finance
            "q-fin.CP",  # Quantitative Finance - Computational Finance
            "stat.AP",  # Statistics - Applications
            "econ.EM",  # Economics - Econometrics
        ]

    async def fetch_papers(self, days: int = 1) -> List[Paper]:
        """
        获取最近N天的arXiv论文

        Args:
            days: 获取最近几天的论文

        Returns:
            论文列表
        """
        logger.info(f"开始获取arXiv论文（最近{days}天）")

        # 构建查询
        cutoff_date = datetime.now() - timedelta(days=days)

        # 使用分类查询
        category_query = " OR ".join([f"cat:{cat}" for cat in self.categories])
        query = f"({category_query})"

        logger.info(f"查询条件: {query}")
        logger.info(f"截止日期: {cutoff_date.strftime('%Y-%m-%d')}")

        try:
            # 使用arXiv客户端搜索
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,  # 按提交日期排序
                sort_order=arxiv.SortOrder.Descending,  # 降序（最新的在前）
            )

            papers = []
            for result in client.results(search):
                # 检查发表日期
                if result.published.replace(tzinfo=None) < cutoff_date:
                    continue

                # 转换为Paper对象
                paper = self._convert_to_paper(result)
                papers.append(paper)

            logger.info(f"成功获取 {len(papers)} 篇arXiv论文")
            return self._validate_papers(papers)

        except Exception as e:
            logger.error(f"获取arXiv论文失败: {e}")
            return []

    def _convert_to_paper(self, result: arxiv.Result) -> Paper:
        """
        将arXiv结果转换为Paper对象

        Args:
            result: arXiv搜索结果

        Returns:
            Paper对象
        """
        # 提取作者
        authors = [author.name for author in result.authors]

        # 提取分类
        categories = [cat for cat in result.categories]

        # 提取arXiv ID
        arxiv_id = result.entry_id.split("/")[-1]

        # 构建Paper对象
        paper = Paper(
            title=result.title,
            authors=authors,
            abstract=result.summary,
            url=result.entry_id,
            pdf_url=result.pdf_url,
            published_date=result.published.replace(tzinfo=None),
            categories=categories,
            arxiv_id=arxiv_id,
            source="arxiv",
        )

        return paper
