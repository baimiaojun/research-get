# ⚙️ 配置说明

本文档详细介绍系统的各项配置选项。

## 📋 目录

- [环境变量配置](#环境变量配置)
- [关键词配置](#关键词配置)
- [提示词配置](#提示词配置)
- [推送时间配置](#推送时间配置)
- [高级配置](#高级配置)

---

## 环境变量配置

环境变量在GitHub仓库的Secrets中配置：`Settings` → `Secrets and variables` → `Actions`

### 必需配置

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `CLAUDE_API_KEY` | Claude API密钥 | `sk-ant-api03-...` |
| `WECOM_WEBHOOK_URL` | 企业微信Webhook地址 | `https://qyapi.weixin.qq.com/...` |

### 可选配置

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `PAPERS_TO_SEND` | 每日推送论文数量 | `6` | `8` |
| `LOG_LEVEL` | 日志级别 | `INFO` | `DEBUG` |
| `ENABLE_ARXIV` | 是否启用arXiv | `true` | `false` |

#### 配置示例

添加可选配置：

1. 进入仓库的 `Settings` → `Secrets and variables` → `Actions`
2. 点击 `New repository secret`
3. Name: `PAPERS_TO_SEND`
4. Value: `8`
5. 点击 `Add secret`

---

## 关键词配置

关键词配置文件：`config/keywords.yml`

### 文件结构

```yaml
domains:          # 研究领域
  domain_name:    # 领域名称
    must_have:    # 核心关键词（论文必须包含）
      - keyword1
      - keyword2
    boost:        # 增强关键词（提高得分）
      - keyword3

exclude:          # 排除关键词（包含则过滤）
  - keyword4

weights:          # 评分权重
  title_match: 10
  abstract_match: 5
```

### 配置说明

#### domains（研究领域）

定义你关注的研究领域和关键词。

**示例：添加新领域**

```yaml
domains:
  # 现有领域
  statistics:
    must_have: [statistical learning, bayesian]
    boost: [regression, probability]

  # 添加新领域：推荐系统
  recommender_systems:
    must_have:
      - recommender system
      - collaborative filtering
      - matrix factorization
    boost:
      - recommendation
      - personalization
      - CTR prediction
```

#### must_have（核心关键词）

- **作用**：论文标题或摘要必须包含这些关键词之一
- **评分**：标题包含 +10分，摘要包含 +5分
- **建议**：添加领域的核心术语

**示例**：

```yaml
machine_learning:
  must_have:
    - machine learning
    - deep learning
    - neural network
    - supervised learning
    - unsupervised learning
```

#### boost（增强关键词）

- **作用**：包含这些关键词会提高得分，但不是必需的
- **评分**：每个关键词 +2分
- **建议**：添加相关但不是核心的术语

**示例**：

```yaml
deep_learning:
  boost:
    - CNN
    - RNN
    - transformer
    - attention
    - ResNet
```

#### exclude（排除关键词）

- **作用**：论文包含这些关键词会被直接过滤掉
- **用途**：排除不感兴趣的子领域

**示例**：

```yaml
exclude:
  - medical imaging      # 排除医学影像
  - drug discovery       # 排除药物发现
  - protein folding      # 排除蛋白质折叠
  - financial trading    # 排除金融交易
```

#### weights（评分权重）

- **作用**：控制不同匹配方式的得分权重

**可配置权重**：

```yaml
weights:
  title_match: 10          # 标题包含must_have关键词
  abstract_match: 5        # 摘要包含must_have关键词
  boost_keyword: 2         # 包含boost关键词
  huggingface_source: 3    # 来自Hugging Face
  paperswithcode: 2        # 来自Papers with Code
```

### 配置技巧

#### 1. 如何扩大论文范围？

- 添加更多 `must_have` 关键词
- 减少 `exclude` 关键词
- 降低评分权重

**示例**：

```yaml
# 原配置：只关注深度学习
deep_learning:
  must_have:
    - deep learning
    - neural network

# 扩大后：包含更多AI领域
ai_broad:
  must_have:
    - artificial intelligence
    - machine learning
    - deep learning
    - neural network
    - computer vision
    - natural language processing
```

#### 2. 如何缩小论文范围？

- 使用更具体的 `must_have` 关键词
- 添加更多 `exclude` 关键词
- 提高评分权重

**示例**：

```yaml
# 只关注Transformer相关
transformer:
  must_have:
    - transformer
    - attention mechanism
    - self-attention
  exclude:
    - CNN
    - RNN
    - LSTM
```

#### 3. 如何调整领域优先级？

通过调整权重来控制不同领域的优先级。

**示例**：

```yaml
# 优先推送深度学习领域论文
weights:
  title_match: 15          # 提高标题匹配权重
  abstract_match: 8        # 提高摘要匹配权重
  boost_keyword: 3
```

---

## 提示词配置

提示词配置文件：`config/prompts.yml`

### 默认提示词

```yaml
summarize_paper: |
  请用中文简洁总结以下学术论文的核心内容（150字以内）：

  标题：{title}
  摘要：{abstract}

  要求：
  1. 第一句说明研究的问题和动机
  2. 第二句说明主要方法或创新点
  3. 第三句说明效果或应用价值

  请直接给出总结，不要包含"总结："等前缀。
```

### 自定义提示词

可以根据需要修改提示词，以获得不同风格的摘要。

**示例：更简洁的摘要**

```yaml
summarize_paper: |
  用中文100字总结这篇论文：

  标题：{title}
  摘要：{abstract}

  要求：简洁、专业、突出创新点。
```

**示例：更详细的摘要**

```yaml
summarize_paper: |
  请用中文详细总结以下学术论文（200字以内）：

  标题：{title}
  摘要：{abstract}

  要求：
  1. 研究背景和问题
  2. 主要方法和技术细节
  3. 实验结果和性能指标
  4. 应用价值和未来方向

  使用专业术语，保持客观。
```

### 可用变量

- `{title}`: 论文标题
- `{abstract}`: 论文摘要
- `{count}`: 论文数量（批量摘要）
- `{papers_list}`: 论文列表（批量摘要）

---

## 推送时间配置

推送时间在GitHub Actions工作流中配置：`.github/workflows/daily_push.yml`

### 修改推送时间

编辑文件中的cron表达式：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 00:00 = 北京时间 08:00
```

### Cron表达式说明

格式：`分 时 日 月 星期`

**常用时间配置**：

| 北京时间 | UTC时间 | Cron表达式 |
|---------|---------|-----------|
| 08:00 | 00:00 | `0 0 * * *` |
| 09:00 | 01:00 | `0 1 * * *` |
| 12:00 | 04:00 | `0 4 * * *` |
| 18:00 | 10:00 | `0 10 * * *` |
| 20:00 | 12:00 | `0 12 * * *` |
| 22:00 | 14:00 | `0 14 * * *` |

**注意**：GitHub Actions使用UTC时区，北京时间 = UTC + 8小时

### 在线工具

使用 [Crontab.guru](https://crontab.guru/) 生成和验证cron表达式。

### 修改推送频率

**每周推送（周一）**：

```yaml
schedule:
  - cron: '0 0 * * 1'  # 每周一UTC 00:00
```

**每两天推送**：

```yaml
schedule:
  - cron: '0 0 */2 * *'  # 每两天UTC 00:00
```

**工作日推送（周一到周五）**：

```yaml
schedule:
  - cron: '0 0 * * 1-5'  # 周一到周五UTC 00:00
```

---

## 高级配置

### 1. 启用多个数据源

编辑 `src/config.py` 或添加环境变量：

```yaml
# 在GitHub Secrets中添加
ENABLE_ARXIV: true
ENABLE_PAPERSWITHCODE: true
ENABLE_HUGGINGFACE: true
```

**注意**：Papers with Code和Hugging Face数据源需要实现对应的fetcher。

### 2. 调整arXiv查询范围

编辑 `src/fetchers/arxiv_fetcher.py`：

```python
# 添加更多分类
self.categories = [
    "cs.LG",   # Machine Learning
    "cs.AI",   # Artificial Intelligence
    "stat.ML", # Statistics ML
    "cs.CV",   # Computer Vision
    "cs.CL",   # NLP
    "cs.NE",   # Neural Computing
    "cs.RO",   # Robotics (新增)
    "cs.IR",   # Information Retrieval (新增)
]
```

### 3. 修改Claude模型

编辑 `src/config.py` 或添加环境变量：

```python
# 使用更快的模型（成本更低）
claude_model: str = "claude-3-5-haiku-20241022"

# 或使用更强的模型（质量更高）
claude_model: str = "claude-opus-4-6"
```

### 4. 调整摘要长度

编辑 `src/config.py`：

```python
# 生成更长的摘要
claude_max_tokens: int = 300

# 生成更短的摘要
claude_max_tokens: int = 150
```

### 5. 修改缓存保留时间

编辑 `src/config.py` 或添加环境变量：

```yaml
# 缓存保留14天（避免短期内重复推送）
CACHE_DAYS: 14

# 缓存保留3天（更快看到重复论文）
CACHE_DAYS: 3
```

### 6. 自定义Markdown格式

编辑 `src/notifiers/formatter.py` 中的 `format_digest` 方法。

**示例：添加自定义emoji**

```python
def _get_source_emoji(self, source: str) -> str:
    emoji_map = {
        "arxiv": "📚",
        "paperswithcode": "💻",
        "huggingface": "🤗",
        "custom_source": "🌟",  # 添加自定义来源
    }
    return emoji_map.get(source.lower(), "📄")
```

---

## 💡 配置建议

### 初学者配置

- 使用默认配置
- 只修改 `config/keywords.yml` 添加自己的关键词
- 每日6篇论文

### 科研工作者配置

- 添加具体的研究方向关键词
- 提高论文数量到8-10篇
- 启用Papers with Code数据源（获取代码链接）

### 团队共享配置

- 放宽关键词范围，覆盖团队所有方向
- 提高论文数量到12-15篇
- 添加多个企业微信Webhook（推送到多个群）

---

## 📞 需要帮助？

- 查看 [README.md](../README.md) - 项目说明
- 查看 [SETUP_TUTORIAL.md](../SETUP_TUTORIAL.md) - 部署教程
- 查看 [FAQ.md](faq.md) - 常见问题
- 提交 [Issue](../../issues) - 反馈问题
