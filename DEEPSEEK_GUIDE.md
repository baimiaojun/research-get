# 🚀 DeepSeek版本使用指南

**没有海外支付账户？没问题！** 使用DeepSeek，支持**支付宝/微信支付**！

## 💰 DeepSeek vs Claude 对比

| 对比项 | DeepSeek | Claude |
|--------|----------|--------|
| **支付方式** | ✅ 支付宝/微信 | ❌ 需要海外信用卡 |
| **价格** | ✅ 0.001元/1K tokens | 💲 $0.003/1K tokens |
| **每月成本** | ✅ **0.1-0.2元** | 💲 $0.6-1.0 |
| **中文能力** | ✅ 优秀 | ✅ 优秀 |
| **效果** | ✅ V3接近GPT-4 | ✅ 顶级 |
| **免费额度** | ✅ 有免费额度 | ✅ 新用户$5 |
| **注册难度** | ✅ 简单 | ⚠️  需要海外手机号 |

**结论**：DeepSeek价格更低，支付更方便，中文能力优秀，**强烈推荐国内用户使用**！

---

## 🎯 快速开始（5分钟）

### 第一步：注册DeepSeek账号

1. **访问DeepSeek平台**
   🔗 https://platform.deepseek.com/

2. **点击"注册"**
   - 使用手机号注册
   - 或使用微信/GitHub登录

3. **完成注册**
   - 验证手机号
   - 完成！

### 第二步：获取API Key

1. **进入API管理页面**
   - 登录后点击"API Keys"
   - 或访问：https://platform.deepseek.com/api_keys

2. **创建API Key**
   - 点击"创建API密钥"
   - 输入名称（如：`学术推送系统`）
   - 点击"确定"

3. **复制API Key**
   ```
   sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   ⚠️ **重要**：这个Key只显示一次，务必保存！

### 第三步：充值（可选）

**新用户通常有免费额度**，可以先免费试用。需要充值时：

1. 点击"充值"
2. 选择金额（最低1元）
3. 使用支付宝/微信支付
4. 完成！

💡 **建议**：先充1-5元试用，够用几个月了。

---

## ⚙️ 配置系统使用DeepSeek

### 方法1：在GitHub配置（推荐）

1. **进入GitHub仓库Secrets**
   - `Settings` → `Secrets and variables` → `Actions`

2. **添加DeepSeek配置**

   添加以下3个Secrets：

   | Name | Value | 说明 |
   |------|-------|------|
   | `AI_SERVICE` | `deepseek` | 指定使用DeepSeek |
   | `DEEPSEEK_API_KEY` | `sk-xxx...` | 你的DeepSeek API Key |
   | `WECOM_WEBHOOK_URL` | `https://qyapi...` | 企业微信Webhook |

3. **完成！**
   - 不需要配置`CLAUDE_API_KEY`
   - 系统会自动使用DeepSeek

### 方法2：本地测试配置

编辑 `.env` 文件：

```bash
# AI服务选择
AI_SERVICE=deepseek

# DeepSeek配置
DEEPSEEK_API_KEY=sk-your-deepseek-key-here

# 企业微信配置
WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx

# 可选配置
PAPERS_TO_SEND=6
LOG_LEVEL=INFO
```

---

## 🧪 测试运行

### GitHub Actions测试

1. **运行配置检查**（需要先更新check_setup.py）
   - Actions → "🔍 检查配置" → Run workflow

2. **运行完整推送**
   - Actions → "Daily Academic Digest" → Run workflow

3. **检查企业微信**
   - 应该收到使用DeepSeek生成摘要的推送

### 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
python -m src.main
```

---

## 📊 成本估算

### DeepSeek定价

- **输入**: 0.001元 / 1K tokens
- **输出**: 0.002元 / 1K tokens

### 每日成本

每天推送6篇论文：
- 每篇论文约300 tokens输入 + 150 tokens输出
- 每天总计：约2700 tokens
- **每天成本**：约 **0.005元**（半分钱）
- **每月成本**：约 **0.15元**（1毛5）

**对比Claude**：
- Claude每月 ≈ 4元（$0.6）
- DeepSeek每月 ≈ 0.15元
- **便宜27倍！** 💰

---

## 🎨 高级配置

### 选择其他模型

DeepSeek提供多个模型：

1. **deepseek-chat**（推荐）
   - 通用对话模型
   - 适合摘要生成
   - 价格最低

2. **deepseek-coder**
   - 代码专用模型
   - 适合技术论文

配置方法（添加到Secrets或.env）：

```bash
DEEPSEEK_MODEL=deepseek-chat
```

### 调整摘要长度

```bash
AI_MAX_TOKENS=300  # 更长的摘要（默认200）
```

### 调整生成温度

```bash
AI_TEMPERATURE=0.5  # 更保守（默认0.7）
AI_TEMPERATURE=0.9  # 更有创意
```

---

## ❓ 常见问题

### Q1: DeepSeek和Claude效果差别大吗？

**A**: 对于论文摘要任务，DeepSeek V3效果非常好，接近Claude水平。中文能力甚至更强。

### Q2: 可以同时支持两个API吗？

**A**: 可以！配置两个API Key，通过`AI_SERVICE`切换：
- 设置为`deepseek`使用DeepSeek
- 设置为`claude`使用Claude

### Q3: 免费额度有多少？

**A**: DeepSeek新用户通常有一定免费额度，具体以官网为准。通常够试用几周。

### Q4: 如何查看API使用量？

**A**:
1. 登录 https://platform.deepseek.com/
2. 进入"用量统计"页面
3. 查看每日使用量和余额

### Q5: API请求失败怎么办？

**A**: 检查：
1. API Key是否正确
2. 账户是否有余额
3. 网络是否正常
4. 查看日志了解详细错误

### Q6: 可以切换回Claude吗？

**A**: 随时可以！修改`AI_SERVICE`为`claude`并配置`CLAUDE_API_KEY`即可。

---

## 🔄 从Claude迁移到DeepSeek

如果你之前配置了Claude，想换成DeepSeek：

### 步骤1：获取DeepSeek API Key
（参考上面的"快速开始"）

### 步骤2：修改GitHub Secrets

1. 添加新Secrets：
   - `AI_SERVICE` = `deepseek`
   - `DEEPSEEK_API_KEY` = `你的key`

2. 保留或删除`CLAUDE_API_KEY`（保留的话以后还能切换回来）

### 步骤3：测试

运行一次workflow，检查是否正常工作。

---

## 📝 完整配置示例

### GitHub Secrets配置

```
AI_SERVICE = deepseek
DEEPSEEK_API_KEY = sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WECOM_WEBHOOK_URL = https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx
PAPERS_TO_SEND = 6
```

### .env文件配置（本地测试）

```bash
# AI服务
AI_SERVICE=deepseek
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 企业微信
WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx

# 可选
PAPERS_TO_SEND=6
LOG_LEVEL=INFO
AI_MAX_TOKENS=200
AI_TEMPERATURE=0.7
```

---

## 🎉 总结

### 为什么选择DeepSeek？

✅ **支持国内支付** - 支付宝/微信，方便快捷
✅ **价格极低** - 每月1-2毛钱，几乎免费
✅ **效果优秀** - V3模型接近GPT-4水平
✅ **中文能力强** - 专门优化过中文
✅ **注册简单** - 国内手机号即可
✅ **有免费额度** - 新用户可免费试用

### 开始使用

1. 注册DeepSeek账号
2. 获取API Key
3. 配置到GitHub Secrets
4. 享受每日学术资讯！

**💰 每月成本不到2毛钱，比买一瓶水还便宜！**

---

## 🔗 相关链接

- **DeepSeek平台**: https://platform.deepseek.com/
- **API文档**: https://platform.deepseek.com/api-docs/
- **价格说明**: https://platform.deepseek.com/pricing
- **项目README**: [README.md](README.md)
- **部署教程**: [SETUP_TUTORIAL.md](SETUP_TUTORIAL.md)

---

**🚀 开始使用DeepSeek，享受低成本、高质量的AI摘要服务！**
