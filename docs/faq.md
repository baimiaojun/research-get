# ❓ 常见问题解答 (FAQ)

## 📋 目录

- [部署相关](#部署相关)
- [运行相关](#运行相关)
- [配置相关](#配置相关)
- [内容相关](#内容相关)
- [费用相关](#费用相关)
- [故障排查](#故障排查)

---

## 部署相关

### Q: 必须要有编程基础吗？

**A:** 不需要！本项目已经完全配置好，你只需要：
1. Fork仓库（点一下按钮）
2. 获取两个密钥（跟着教程复制粘贴）
3. 在GitHub网页上填入密钥

全程不需要写代码，跟着[图文教程](../SETUP_TUTORIAL.md)操作即可。

### Q: 需要自己的服务器吗？

**A:** 完全不需要！系统运行在GitHub Actions上，完全免费，无需任何服务器。

### Q: Fork后需要做什么？

**A:** Fork后需要：
1. 获取Claude API Key
2. 获取企业微信Webhook
3. 在仓库Settings中配置这两个Secrets
4. 运行配置检查验证

详见：[快速部署指南](../SETUP_TUTORIAL.md)

### Q: 配置错了怎么办？

**A:** 随时可以修改：
1. 进入 `Settings` → `Secrets and variables` → `Actions`
2. 点击要修改的Secret后面的 `Update`
3. 输入新值并保存

---

## 运行相关

### Q: 如何查看运行日志？

**A:** 详细步骤：
1. 点击仓库的 `Actions` 标签
2. 点击某次运行记录
3. 点击 `push` 任务
4. 展开各步骤查看详细输出
5. 右上角可下载完整日志

### Q: 如何手动触发运行？

**A:**
1. 进入 `Actions` 标签
2. 左侧选择 `Daily Academic Digest`
3. 右侧点击 `Run workflow` → `Run workflow`
4. 等待1-2分钟即可

### Q: 如何临时停止每日推送？

**A:**
1. `Actions` → `Daily Academic Digest`
2. 右上角三个点 `···` → `Disable workflow`
3. 需要恢复时：`Enable workflow`

### Q: 如何修改推送时间？

**A:** 编辑 `.github/workflows/daily_push.yml` 文件：

```yaml
schedule:
  - cron: '0 0 * * *'  # 当前：北京时间 08:00
```

修改cron表达式（使用UTC时区）：
- `0 0 * * *` = 北京时间 08:00
- `0 12 * * *` = 北京时间 20:00
- `0 22 * * *` = 北京时间 06:00（次日）

💡 提示：使用 [Crontab.guru](https://crontab.guru/) 生成cron表达式

### Q: 每天什么时候推送？

**A:** 默认每天北京时间早上 **8:00** 推送。可以修改cron表达式调整时间。

### Q: 为什么有时候推送时间不准确？

**A:** GitHub Actions的定时任务可能会延迟5-10分钟，这是正常现象。如果延迟超过30分钟，可能是GitHub平台负载较高。

---

## 配置相关

### Q: 如何修改每日推送的论文数量？

**A:** 两种方法：

**方法1：添加Secret（推荐）**
1. `Settings` → `Secrets and variables` → `Actions`
2. `New repository secret`
3. Name: `PAPERS_TO_SEND`
4. Value: `8`（你想要的数量）

**方法2：修改代码**
编辑 `src/config.py`，修改默认值

### Q: 如何修改关注的领域？

**A:** 编辑 `config/keywords.yml` 文件：

```yaml
domains:
  statistics:
    must_have: [statistical learning, bayesian, causal inference]
    boost: [regression, probability]
  machine_learning:
    must_have: [machine learning, supervised learning]
    boost: [classification, clustering]
  # 添加新领域
  your_field:
    must_have: [关键词1, 关键词2]
    boost: [相关词1, 相关词2]
```

保存后立即生效，下次推送会使用新配置。

### Q: 如何排除某些主题？

**A:** 在 `config/keywords.yml` 中添加到 `exclude` 列表：

```yaml
exclude:
  - medical imaging
  - drug discovery
  - protein folding
  - 你想排除的主题
```

### Q: 如何调整摘要的提示词？

**A:** 编辑 `config/prompts.yml` 文件，修改 `summarize_paper` 模板。

---

## 内容相关

### Q: 推送的论文不相关怎么办？

**A:** 优化关键词配置：
1. 在 `config/keywords.yml` 中添加更精准的 `must_have` 关键词
2. 添加不相关主题到 `exclude` 列表
3. 调整 `boost` 关键词增加相关论文权重

### Q: 为什么有时候推送的论文少于6篇？

**A:** 可能的原因：
1. 当天符合条件的新论文较少
2. 关键词过滤太严格
3. 缓存机制过滤了已推送的论文

解决方法：
- 放宽关键词条件
- 检查日志查看过滤情况

### Q: 会重复推送同一篇论文吗？

**A:** 不会。系统有缓存机制，会记录最近7天推送过的论文ID，避免重复推送。

### Q: 论文摘要是AI生成的吗？质量如何？

**A:** 是的，使用Claude 3.5 Sonnet生成：
- 150字以内的中文摘要
- 3句话结构：问题动机 + 方法创新 + 效果价值
- 质量优秀，易于理解

### Q: 可以添加其他数据源吗？

**A:** 可以！当前主要使用arXiv。计划中的数据源：
- Papers with Code（包含代码实现）
- Hugging Face Daily Papers（AI社区精选）

欢迎贡献代码添加新数据源！

---

## 费用相关

### Q: 使用成本是多少？

**A:** 成本明细：
- **GitHub Actions**: 完全免费（公开仓库）
- **Claude API**: ~$0.02/天 ≈ $0.6/月
- **企业微信**: 完全免费
- **总计**: **< $1/月**

### Q: 新用户有免费额度吗？

**A:** 有！Claude新用户有 **$5 免费额度**：
- 按每天$0.02计算
- 可以免费使用约 **8-10个月**
- 足够评估是否长期使用

### Q: 免费额度用完了怎么办？

**A:**
1. 访问 [Claude Console](https://console.anthropic.com/)
2. 进入 `Billing` 页面充值
3. 最低充值 $5
4. 可使用信用卡支付

### Q: 如何查看API使用量？

**A:**
1. 访问 [Claude Console](https://console.anthropic.com/)
2. 进入 `Usage` 页面
3. 查看每日使用量和剩余额度

### Q: 可以降低成本吗？

**A:** 可以通过以下方式：
1. 减少每日推送论文数量（`PAPERS_TO_SEND`）
2. 减少推送频率（如改为每周推送）
3. 使用更便宜的模型（但质量会下降）

---

## 故障排查

### Q: Actions运行失败怎么办？

**A:** 排查步骤：

**1. 检查Secrets配置**
- 名称是否完全正确（区分大小写）
- `CLAUDE_API_KEY` 和 `WECOM_WEBHOOK_URL`
- 值是否完整复制（没有多余空格）

**2. 运行配置检查**
- `Actions` → `🔍 检查配置` → `Run workflow`
- 查看哪个环节失败

**3. 查看详细日志**
- 点击失败的运行记录
- 查看红色 ❌ 的步骤
- 展开查看错误信息

**4. 常见错误**
- `Authentication failed`: API Key不正确
- `Webhook failed`: 企业微信Webhook错误
- `Rate limit`: API调用频率限制（稍后重试）

### Q: 没有收到企业微信推送？

**A:** 排查清单：

- [ ] GitHub Actions运行成功（绿色✅）
- [ ] 企业微信机器人未被删除
- [ ] Webhook URL正确
- [ ] 群聊未被解散
- [ ] 查看Actions日志确认推送成功

**测试方法**：
运行"检查配置"工作流，看是否收到测试消息。

### Q: Claude API认证失败？

**A:** 检查项：
1. API Key是否以 `sk-ant-` 开头
2. API Key是否完整（很长，包含随机字符）
3. API Key是否已激活（访问Console查看）
4. 账户是否有余额

### Q: 企业微信推送失败？

**A:** 检查项：
1. Webhook URL是否以 `https://qyapi.weixin.qq.com/` 开头
2. 机器人是否被删除
3. URL是否完整（包含key参数）
4. 网络是否通畅

**重新获取Webhook**：
群设置 → 群机器人 → 选择机器人 → 查看Webhook地址

### Q: 日志在哪里下载？

**A:**
1. `Actions` → 点击某次运行
2. 页面下方 `Artifacts` 部分
3. 点击 `logs-xxx` 下载
4. 日志保留7天

### Q: 如何报告bug？

**A:**
1. 收集信息：
   - 错误截图
   - Actions日志
   - 配置信息（隐藏敏感部分）
2. 提交Issue：[GitHub Issues](../../issues)
3. 描述问题：
   - 预期行为
   - 实际行为
   - 复现步骤

---

## 高级问题

### Q: 可以自定义推送格式吗？

**A:** 可以！编辑 `src/notifiers/formatter.py` 文件，修改 `format_digest` 方法。

支持的Markdown格式：
- 标题：`#` `##` `###`
- 粗体：`**文本**`
- 链接：`[文本](URL)`
- 分隔线：`---`

### Q: 可以推送到多个群吗？

**A:** 可以通过以下方式：

**方法1：多个Webhook（需修改代码）**
在 `src/notifiers/wecom_notifier.py` 中添加循环推送逻辑。

**方法2：企业微信消息转发**
在企业微信中设置消息自动转发到其他群。

### Q: 可以添加邮件推送吗？

**A:** 可以！需要添加邮件通知模块：
1. 创建 `src/notifiers/email_notifier.py`
2. 在 `src/main.py` 中调用
3. 添加SMTP配置到Secrets

欢迎贡献代码！

### Q: 如何调试本地开发？

**A:**
1. 克隆仓库到本地
2. 安装依赖：`pip install -r requirements.txt`
3. 创建 `.env` 文件：
   ```
   CLAUDE_API_KEY=your_key
   WECOM_WEBHOOK_URL=your_webhook
   ```
4. 运行：`python -m src.main`

### Q: 如何贡献代码？

**A:**
1. Fork本仓库
2. 创建功能分支：`git checkout -b feature/xxx`
3. 提交代码：`git commit -am 'Add xxx'`
4. 推送分支：`git push origin feature/xxx`
5. 提交Pull Request

---

## 📞 获取帮助

如果以上答案没有解决你的问题：

1. **查看详细教程**: [SETUP_TUTORIAL.md](../SETUP_TUTORIAL.md)
2. **查看配置文档**: [configuration.md](configuration.md)
3. **提交Issue**: [GitHub Issues](../../issues)
4. **查看源代码**: 代码有详细注释

---

**💡 提示**: 大部分问题都可以通过运行"检查配置"工作流来诊断！
