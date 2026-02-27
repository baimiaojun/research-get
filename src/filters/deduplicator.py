"""
去重模块
基于arXiv ID和标题相似度进行去重
"""
from typing import List
from src.fetchers.base import Paper
from src.utils.logger import get_logger

logger = get_logger()


class Deduplicator:
    """论文去重器"""

    def __init__(self, similarity_threshold: float = 0.9):
        """
        初始化

        Args:
            similarity_threshold: 标题相似度阈值（0-1）
        """
        self.similarity_threshold = similarity_threshold

    def deduplicate(self, papers: List[Paper]) -> List[Paper]:
        """
        对论文列表去重

        Args:
            papers: 论文列表

        Returns:
            去重后的论文列表
        """
        if not papers:
            return []

        logger.info(f"开始去重 {len(papers)} 篇论文")

        unique_papers = []
        seen_ids = set()
        seen_titles = []

        for paper in papers:
            # 1. 基于arXiv ID去重（优先）
            paper_id = paper.get_id()
            if paper_id in seen_ids:
                logger.debug(f"重复ID {paper_id}: {paper.title[:50]}...")
                continue

            # 2. 基于标题相似度去重
            if self._is_similar_to_any(paper.title, seen_titles):
                logger.debug(f"重复标题: {paper.title[:50]}...")
                continue

            # 添加到唯一列表
            unique_papers.append(paper)
            seen_ids.add(paper_id)
            seen_titles.append(paper.title.lower())

        logger.info(f"去重完成: {len(papers)} → {len(unique_papers)} 篇论文")
        logger.info(f"移除了 {len(papers) - len(unique_papers)} 篇重复论文")

        return unique_papers

    def _is_similar_to_any(self, title: str, seen_titles: List[str]) -> bool:
        """
        检查标题是否与已见标题相似

        Args:
            title: 待检查的标题
            seen_titles: 已见标题列表

        Returns:
            是否相似
        """
        title_lower = title.lower().strip()

        for seen_title in seen_titles:
            similarity = self._calculate_similarity(title_lower, seen_title)
            if similarity >= self.similarity_threshold:
                return True

        return False

    def _calculate_similarity(self, title1: str, title2: str) -> float:
        """
        计算两个标题的相似度（简单版本：基于字符集合）

        Args:
            title1: 标题1
            title2: 标题2

        Returns:
            相似度（0-1）
        """
        # 简单方法：完全相同
        if title1 == title2:
            return 1.0

        # 计算Jaccard相似度（基于单词集合）
        words1 = set(title1.split())
        words2 = set(title2.split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union) if union else 0.0

    def merge_paper_lists(self, *paper_lists: List[Paper]) -> List[Paper]:
        """
        合并多个论文列表并去重

        Args:
            paper_lists: 多个论文列表

        Returns:
            合并去重后的论文列表
        """
        # 合并所有列表
        all_papers = []
        for papers in paper_lists:
            all_papers.extend(papers)

        logger.info(f"合并 {len(paper_lists)} 个列表，共 {len(all_papers)} 篇论文")

        # 去重
        return self.deduplicate(all_papers)
