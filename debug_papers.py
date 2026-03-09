"""
调试脚本：查看获取到的论文分类分布
"""
import asyncio
import arxiv
from datetime import datetime, timedelta
from collections import Counter

async def main():
    # 分类列表
    categories = [
        "cs.LG",  # Machine Learning
        "cs.AI",  # Artificial Intelligence
        "stat.ML",  # Machine Learning (Statistics)
        "q-fin.RM",  # Quantitative Finance - Risk Management
        "q-fin.ST",  # Quantitative Finance - Statistical Finance
        "q-fin.CP",  # Quantitative Finance - Computational Finance
        "stat.AP",  # Statistics - Applications
        "econ.EM",  # Economics - Econometrics
    ]

    # 构建查询
    cutoff_date = datetime.now() - timedelta(days=2)
    category_query = " OR ".join([f"cat:{cat}" for cat in categories])
    query = f"({category_query})"

    print(f"查询条件: {query}")
    print(f"截止日期: {cutoff_date.strftime('%Y-%m-%d')}\n")

    # 搜索论文
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=50,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    papers = []
    category_counts = Counter()

    for result in client.results(search):
        if result.published.replace(tzinfo=None) < cutoff_date:
            continue

        papers.append(result)
        # 统计每篇论文的主要分类
        if result.categories:
            primary_cat = result.categories[0]
            category_counts[primary_cat] += 1

    print(f"总共获取到 {len(papers)} 篇论文\n")

    print("=== 分类分布 ===")
    for cat, count in category_counts.most_common():
        print(f"{cat}: {count} 篇")

    print("\n=== 金融相关论文 ===")
    finance_papers = [p for p in papers if any(cat.startswith('q-fin') or cat.startswith('econ') for cat in p.categories)]

    if finance_papers:
        for paper in finance_papers:
            print(f"\n标题: {paper.title}")
            print(f"分类: {', '.join(paper.categories)}")
            print(f"摘要片段: {paper.summary[:200]}...")
    else:
        print("没有找到金融相关的论文")

    print("\n=== 统计相关论文 ===")
    stat_papers = [p for p in papers if any(cat.startswith('stat') for cat in p.categories)]

    if stat_papers:
        for paper in stat_papers[:5]:  # 只显示前5篇
            print(f"\n标题: {paper.title}")
            print(f"分类: {', '.join(paper.categories)}")

if __name__ == "__main__":
    asyncio.run(main())
