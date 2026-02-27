# ⚡ 快速配置AI服务

**重要**：新的推送格式需要AI生成结构化摘要，必须配置AI服务！

---

## 🚀 方案一：DeepSeek（推荐，5分钟）

### 为什么选DeepSeek？
- ✅ 支持支付宝/微信支付
- ✅ 每月只需0.15元（1毛5）
- ✅ 中文能力优秀
- ✅ 5分钟配置完成

### 配置步骤

#### 1. 注册DeepSeek（2分钟）
访问：https://platform.deepseek.com/
- 手机号注册或微信登录
- 完成验证

#### 2. 获取API Key（1分钟）
- 进入"API Keys"页面
- 点击"创建API密钥"
- 复制密钥（`sk-xxx...`）

#### 3. 充值（可选）
- 新用户有免费额度，可先试用
- 需要充值时：最低1元，支持支付宝/微信

#### 4. 配置到系统（1分钟）

**本地测试**：
编辑 `.env` 文件：
```bash
AI_SERVICE=deepseek
DEEPSEEK_API_KEY=sk-你的密钥
WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=25de2dcf-903e-41c3-a1ee-82ffc7c73fed
```

**GitHub部署**：
在仓库Secrets中添加：
- `AI_SERVICE` = `deepseek`
- `DEEPSEEK_API_KEY` = `sk-你的密钥`

#### 5. 测试
```bash
python3 -m src.main
```

---

## 📋 方案二：Claude（需要海外信用卡）

### 配置步骤

#### 1. 注册Claude
访问：https://console.anthropic.com/
- 需要海外信用卡
- 新用户$5免费额度

#### 2. 获取API Key
- 创建API Key
- 复制密钥（`sk-ant-xxx...`）

#### 3. 配置到系统

**本地测试**：
编辑 `.env` 文件：
```bash
AI_SERVICE=claude
CLAUDE_API_KEY=sk-ant-你的密钥
WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=25de2dcf-903e-41c3-a1ee-82ffc7c73fed
```

**GitHub部署**：
在仓库Secrets中添加：
- `AI_SERVICE` = `claude`
- `CLAUDE_API_KEY` = `sk-ant-你的密钥`

---

## 🎨 新格式效果预览

配置AI后，推送消息格式如下：

```markdown
# 🎓 学术资讯日报
**2026-02-26 周三**

## 📊 今日精选 3 篇前沿论文

---

### 1. Attention Is All You Need

**🏷️ 研究方向**: 深度学习 · 自然语言处理

**💡 核心创新**
提出完全基于注意力机制的Transformer架构，摒弃循环和卷积结构

**⚙️ 技术要点**
• 多头自注意力机制：并行计算序列全局依赖
• 位置编码：使用正弦函数编码位置信息
• 前馈网络：每层包含两个线性变换和ReLU激活

**🎯 主要贡献**
在机器翻译任务上超越RNN模型，训练速度提升，成为现代NLP基础架构

**🔗 资源**: [📄 查看论文](url) · [📥 PDF](url) · [💻 代码](url)

---
```

**对比旧格式**：
- ❌ 旧：直接贴原始英文摘要
- ✅ 新：结构化中文总结，清晰易读

---

## ⚠️ 不配置AI会怎样？

如果设置 `AI_SERVICE=none`：
- 会直接使用arXiv的原始英文摘要
- 格式较差，难以快速获取信息
- **不推荐**

---

## 💰 成本对比

| 服务 | 月成本 | 支付方式 | 推荐度 |
|------|-------|----------|--------|
| DeepSeek | **0.15元** | 支付宝/微信 | ⭐⭐⭐⭐⭐ |
| Claude | $0.6 (≈4元) | 海外信用卡 | ⭐⭐⭐⭐ |
| 不用AI | 免费 | - | ⭐⭐ |

---

## 📖 详细教程

- [DeepSeek完整指南](DEEPSEEK_GUIDE.md)
- [国内用户使用指南](国内用户使用指南.md)
- [部署教程](SETUP_TUTORIAL.md)

---

**🎯 推荐行动**：立即配置DeepSeek，体验新格式！
