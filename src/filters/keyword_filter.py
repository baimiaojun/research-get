"""
关键词过滤模块
基于配置的关键词对论文进行评分和筛选
"""
import yaml
from pathlib import Path
from typing import List, Tuple, Dict, Any
from src.fetchers.base import Paper
from src.utils.logger import get_logger

logger = get_logger()


class KeywordFilter:
    """关键词过滤器"""

    def __init__(self, keywords_file: str = "config/keywords.yml"):
        """
        初始化

        Args:
            keywords_file: 关键词配置文件路径
        """
        self.keywords_file = Path(keywords_file)
        self.config = self._load_config()

        # 提取配置
        self.domains = self.config.get("domains", {})
        self.exclude_keywords = self.config.get("exclude", [])
        self.weights = self.config.get("weights", {})

        # 收集所有must_have和boost关键词
        self.must_have_keywords = []
        self.boost_keywords = []
        for domain_config in self.domains.values():
            self.must_have_keywords.extend(domain_config.get("must_have", []))
            self.boost_keywords.extend(domain_config.get("boost", []))

        logger.info(f"关键词过滤器已初始化")
        logger.info(f"  - 核心关键词: {len(self.must_have_keywords)} 个")
        logger.info(f"  - 增强关键词: {len(self.boost_keywords)} 个")
        logger.info(f"  - 排除关键词: {len(self.exclude_keywords)} 个")

    def _load_config(self) -> Dict[str, Any]:
        """
        加载关键词配置

        Returns:
            配置字典
        """
        try:
            with open(self.keywords_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            logger.info(f"成功加载关键词配置: {self.keywords_file}")
            return config
        except Exception as e:
            logger.error(f"加载关键词配置失败: {e}")
            return {}

    def should_exclude(self, paper: Paper) -> bool:
        """
        检查论文是否应该被排除

        Args:
            paper: 论文对象

        Returns:
            是否应该排除
        """
        text = f"{paper.title} {paper.abstract}".lower()

        for keyword in self.exclude_keywords:
            if keyword.lower() in text:
                logger.debug(f"排除论文（包含关键词 '{keyword}'）: {paper.title}")
                return True

        return False

    def calculate_score(self, paper: Paper) -> float:
        """
        计算论文相关性得分

        Args:
            paper: 论文对象

        Returns:
            得分（越高越相关）
        """
        score = 0.0

        title_lower = paper.title.lower()
        abstract_lower = paper.abstract.lower()

        # 标题包含must_have关键词
        title_match_weight = self.weights.get("title_match", 10)
        for keyword in self.must_have_keywords:
            if keyword.lower() in title_lower:
                score += title_match_weight
                logger.debug(f"标题匹配 '{keyword}': +{title_match_weight}")

        # 摘要包含must_have关键词
        abstract_match_weight = self.weights.get("abstract_match", 5)
        for keyword in self.must_have_keywords:
            if keyword.lower() in abstract_lower:
                score += abstract_match_weight
                logger.debug(f"摘要匹配 '{keyword}': +{abstract_match_weight}")

        # 包含boost关键词
        boost_weight = self.weights.get("boost_keyword", 2)
        text = f"{title_lower} {abstract_lower}"
        for keyword in self.boost_keywords:
            if keyword.lower() in text:
                score += boost_weight
                logger.debug(f"增强关键词 '{keyword}': +{boost_weight}")

        # 来源加权
        if paper.source == "huggingface":
            bonus = self.weights.get("huggingface_source", 3)
            score += bonus
            logger.debug(f"Hugging Face来源: +{bonus}")
        elif paper.source == "paperswithcode" and paper.code_url:
            bonus = self.weights.get("paperswithcode", 2)
            score += bonus
            logger.debug(f"Papers with Code来源: +{bonus}")

        return score

    def filter_and_rank(
        self,
        papers: List[Paper],
        min_score: float = 0.0,
    ) -> List[Tuple[Paper, float]]:
        """
        过滤并排序论文

        Args:
            papers: 论文列表
            min_score: 最低分数阈值

        Returns:
            (论文, 得分) 元组列表，按得分降序排列
        """
        logger.info(f"开始过滤和评分 {len(papers)} 篇论文")

        scored_papers = []

        for paper in papers:
            # 检查是否应该排除
            if self.should_exclude(paper):
                continue

            # 计算得分
            score = self.calculate_score(paper)

            # 过滤低分论文
            if score >= min_score:
                scored_papers.append((paper, score))
                logger.debug(f"得分 {score:.1f}: {paper.title[:50]}...")

        # 按得分降序排序
        scored_papers.sort(key=lambda x: x[1], reverse=True)

        logger.info(f"过滤完成: {len(scored_papers)} 篇论文通过筛选")

        if scored_papers:
            logger.info(f"最高分: {scored_papers[0][1]:.1f}")
            logger.info(f"最低分: {scored_papers[-1][1]:.1f}")

        return scored_papers

    def get_top_papers(
        self,
        papers: List[Paper],
        count: int = 6,
        min_score: float = 0.0,
    ) -> List[Tuple[Paper, float]]:
        """
        获取评分最高的N篇论文

        Args:
            papers: 论文列表
            count: 需要的论文数量
            min_score: 最低分数阈值

        Returns:
            (论文, 得分) 元组列表
        """
        scored_papers = self.filter_and_rank(papers, min_score)

        top_papers = scored_papers[:count]

        logger.info(f"选出Top {len(top_papers)} 篇论文（目标 {count} 篇）")

        return top_papers
