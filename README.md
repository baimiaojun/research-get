# 🎓 学术资讯每日推送系统

每天早上8点，自动推送AI/机器学习/深度学习/统计学领域最新论文到企业微信

## 💡 没有海外信用卡？

**推荐使用DeepSeek** - 支持支付宝/微信支付，每月成本不到2毛钱！

👉 [DeepSeek使用指南](DEEPSEEK_GUIDE.md)

---

## 🚀 5分钟快速开始

### 1️⃣ Fork本仓库
点击页面右上角的 **Fork** 按钮，将本仓库复制到你的GitHub账号

### 2️⃣ 获取密钥

**方案A：使用DeepSeek**（推荐，支持国内支付）
- **DeepSeek API Key**: 访问 [DeepSeek Platform](https://platform.deepseek.com/)，注册并创建API Key
- **企业微信Webhook**: 在企业微信群中添加群机器人，获取Webhook URL
- 💰 **成本**：每月不到0.2元

**方案B：使用Claude**（需要海外信用卡）
- **Claude API Key**: 访问 [Claude Console](https://console.anthropic.com/)，注册并创建API Key
- **企业微信Webhook**: 在企业微信群中添加群机器人，获取Webhook URL
- 💰 **成本**：每月约$0.6（新用户$5免费额度）

### 3️⃣ 配置Secrets
详见 👉 [📖 超详细图文教程](SETUP_TUTORIAL.md)

在你Fork的仓库中：
1. 点击 `Settings` → `Secrets and variables` → `Actions`
2. 添加secrets：

**使用DeepSeek（推荐）**:
- `AI_SERVICE`: 填 `deepseek`
- `DEEPSEEK_API_KEY`: 你的DeepSeek API密钥
- `WECOM_WEBHOOK_URL`: 企业微信Webhook地址

**或使用Claude**:
- `AI_SERVICE`: 填 `claude`
- `CLAUDE_API_KEY`: 你的Claude API密钥
- `WECOM_WEBHOOK_URL`: 企业微信Webhook地址

### 4️⃣ 测试运行
1. 点击 `Actions` 标签
2. 选择 "🔍 检查配置" → 点击 `Run workflow` 验证配置
3. 选择 "Daily Academic Digest" → 点击 `Run workflow` 测试完整推送

### 5️⃣ 完成！
✅ 每天早上8:00自动推送学术资讯到企业微信

---

## ✨ 功能特点

- 🤖 **AI智能摘要** - 使用Claude 3.5 Sonnet生成150字中文摘要
- 📊 **每日精选** - 智能筛选5-8篇最相关论文
- 🎯 **关键词过滤** - 基于你的研究领域智能筛选
- 💰 **成本极低** - 每月不到$1，新用户免费额度可用2-3个月
- 🔄 **全自动运行** - GitHub Actions定时调度，无需服务器
- 🎨 **精美格式** - Markdown格式，阅读体验优秀

## 📱 推送效果预览

```markdown
# 🎓 学术资讯日报 | 2026-02-26

## 📊 今日精选 6 篇论文

### 1. Attention Is All You Need
**作者**: Vaswani et al.
**领域**: Deep Learning, NLP

本文提出了Transformer架构，完全基于注意力机制而不使用循环或卷积。
该方法在机器翻译任务上超越了RNN模型，训练速度更快且效果更好。
Transformer已成为现代NLP的基础架构，广泛应用于GPT、BERT等模型。

[📄 查看论文](https://arxiv.org/abs/...) | [💻 查看代码](https://github.com/...)

---
```

## 💡 使用场景

- 🔬 **科研工作者** - 跟踪最新研究进展，不错过重要论文
- 💼 **AI从业者** - 了解行业动态，把握技术趋势
- 🎓 **学生学习** - 学习前沿技术，拓展知识视野

## 🛠 自定义配置

### 修改关注领域
编辑 `config/keywords.yml` 文件，添加/删除你感兴趣的关键词：

```yaml
domains:
  statistics:
    must_have: [statistical learning, bayesian, causal inference]
    boost: [regression, probability]
  # 添加更多领域...
```

### 修改推送时间
编辑 `.github/workflows/daily_push.yml`：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 00:00 = 北京时间 08:00
  # 修改为其他时间，如 '0 12 * * *' = 北京时间 20:00
```

### 修改推送数量
在GitHub Secrets中添加 `PAPERS_TO_SEND`（可选，默认6篇）

## 📊 成本说明

### 使用DeepSeek（推荐）

| 项目 | 费用 |
|------|------|
| GitHub Actions | **免费**（公开仓库无限制） |
| DeepSeek API | **~0.005元/天** ≈ 0.15元/月 |
| 企业微信 | **免费** |
| **总计** | **< 0.2元/月** |

### 使用Claude

| 项目 | 费用 |
|------|------|
| GitHub Actions | **免费**（公开仓库无限制） |
| Claude API | **~$0.02/天** ≈ $0.6/月 |
| 企业微信 | **免费** |
| **总计** | **< $1/月** |

💡 **对比**：DeepSeek比Claude便宜约**27倍**，新用户都有免费额度可试用！

## 📖 详细文档

- [📖 超详细图文部署教程](SETUP_TUTORIAL.md) - 带截图的傻瓜式教程
- [⚙️ 配置说明](docs/configuration.md) - 高级配置选项
- [❓ 常见问题](docs/faq.md) - 疑难解答

## 🔧 常见问题快速解答

<details>
<summary><b>如何查看运行日志？</b></summary>

1. 点击仓库的 `Actions` 标签
2. 点击某次运行记录
3. 展开步骤查看详细日志
4. 可以下载日志文件供分析
</details>

<details>
<summary><b>如何临时停止推送？</b></summary>

1. 进入 `Actions` → `Daily Academic Digest`
2. 点击右上角 `···` → `Disable workflow`
3. 需要恢复时再 `Enable workflow`
</details>

<details>
<summary><b>为什么没有收到推送？</b></summary>

1. 检查GitHub Actions是否成功运行（Actions标签查看）
2. 运行"🔍 检查配置"工作流验证设置
3. 查看日志文件排查错误
4. 确认企业微信Webhook URL正确
</details>

<details>
<summary><b>费用会很高吗？</b></summary>

不会！每月成本不到$1：
- GitHub Actions完全免费
- Claude API每天约$0.02（6篇论文摘要）
- 新用户$5免费额度可用8个月
</details>

## 🤝 问题反馈

遇到问题？欢迎提交 [Issue](../../issues)

## 📄 许可证

MIT License - 自由使用和修改

---

**⭐ 如果觉得有用，请给个Star支持一下！**
