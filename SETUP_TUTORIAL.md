# 📖 学术推送系统 - 5分钟快速部署指南

本教程将手把手教你部署学术资讯推送系统，**全程不超过10分钟**！

## 📋 前置要求

- ✅ 一个GitHub账号（没有的话[点这里注册](https://github.com/signup)）
- ✅ 一个企业微信账号
- ✅ 一张信用卡（用于Claude API，新用户有$5免费额度）

---

## 第一步：Fork本仓库（1分钟）

### 操作步骤

1. **点击页面右上角的 `Fork` 按钮**

   > 📍 位置：仓库页面右上角，Star按钮旁边

   ```
   [Watch ▼] [Star ⭐] [Fork 🍴]
                          ↑
                      点这里
   ```

2. **等待几秒钟**，GitHub会自动将仓库复制到你的账号

3. **跳转成功**后，你会看到 `your-username/学术资料同步`

✅ **完成标志**：仓库URL变为 `github.com/你的用户名/学术资料同步`

---

## 第二步：获取Claude API Key（2分钟）

### 操作步骤

1. **访问 Claude控制台**

   🔗 https://console.anthropic.com/

2. **注册/登录账号**
   - 推荐使用Google账号快速登录
   - 需要绑定手机号验证

3. **创建API Key**

   - 点击左侧菜单 `API Keys`
   - 点击右上角 `Create Key` 按钮
   - 输入名称（如：`academic-push`）
   - 点击 `Create Key`

4. **复制API Key**

   ```
   sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

   ⚠️ **重要**：这个Key只显示一次，务必复制保存！

### 💡 关于费用

- ✅ 新用户有 **$5 免费额度**
- ✅ 每天推送成本约 **$0.02**
- ✅ 免费额度可用 **8个月左右**
- ✅ 用完后可充值，最低$5

✅ **完成标志**：你已复制了类似 `sk-ant-api03-...` 的密钥

---

## 第三步：获取企业微信Webhook（2分钟）

### 操作步骤

1. **打开企业微信客户端**（手机或电脑都可以）

2. **创建或选择一个群聊**
   - 可以创建一个新群（只有你自己）
   - 或使用已有的群聊

3. **添加群机器人**

   - 点击群聊右上角 `···` （更多）
   - 选择 `群机器人`
   - 点击 `添加机器人`
   - 选择 `添加群机器人`

4. **配置机器人**

   - 输入机器人名称（如：`学术资讯助手`）
   - 点击 `添加`

5. **复制Webhook地址**

   ```
   https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```

   📱 **手机端**：长按Webhook地址复制

   💻 **电脑端**：点击复制按钮

### 💡 提示

- ✅ Webhook是永久有效的，除非你删除机器人
- ✅ 可以随时在群设置中查看Webhook地址
- ✅ 不要分享Webhook给别人，否则任何人都能向你的群发消息

✅ **完成标志**：你已复制了类似 `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=...` 的地址

---

## 第四步：在GitHub配置Secrets（3分钟）

### 操作步骤

1. **进入你Fork的仓库**

   🔗 `github.com/你的用户名/学术资料同步`

2. **点击 `Settings` 标签**

   ```
   [< > Code] [Issues] [Pull requests] [Actions] [Settings]
                                                    ↑
                                                 点这里
   ```

   ⚠️ **注意**：如果看不到Settings，说明你不在自己Fork的仓库

3. **进入Secrets配置页面**

   - 左侧菜单找到 `Secrets and variables`
   - 点击展开，选择 `Actions`

   ```
   Security
   └─ Secrets and variables
      └─ Actions ← 点这里
   ```

4. **添加第一个Secret - Claude API Key**

   - 点击右上角绿色按钮 `New repository secret`
   - **Name** 输入：`CLAUDE_API_KEY`（必须完全一致，包括大小写）
   - **Secret** 粘贴：你在第二步复制的API Key（`sk-ant-api03-...`）
   - 点击 `Add secret`

5. **添加第二个Secret - 企业微信Webhook**

   - 再次点击 `New repository secret`
   - **Name** 输入：`WECOM_WEBHOOK_URL`（必须完全一致）
   - **Secret** 粘贴：你在第三步复制的Webhook URL（`https://qyapi.weixin.qq.com/...`）
   - 点击 `Add secret`

### 📸 配置检查清单

完成后，你应该看到两个Secrets：

```
CLAUDE_API_KEY          Updated now by you
WECOM_WEBHOOK_URL       Updated now by you
```

✅ **完成标志**：Secrets页面显示2个已配置的密钥

---

## 第五步：测试配置（1分钟）

### 操作步骤

1. **进入Actions标签**

   ```
   [< > Code] [Issues] [Pull requests] [Actions] [Settings]
                                          ↑
                                       点这里
   ```

2. **首次启用Actions**（仅第一次需要）

   如果看到绿色按钮 `I understand my workflows, go ahead and enable them`，点击启用

3. **运行配置检查**

   - 左侧选择 `🔍 检查配置`
   - 右侧点击 `Run workflow` 下拉按钮
   - 再点击绿色的 `Run workflow` 按钮
   - 等待几秒，页面刷新

4. **查看运行状态**

   - 会看到一个黄色圆圈⭕（运行中）
   - 等待30秒-1分钟
   - 变成绿色✅表示成功，红色❌表示失败

5. **查看详细日志**（可选）

   - 点击运行记录
   - 点击 `check` 任务
   - 展开步骤查看详细输出

### ✅ 成功的标志

运行成功后，你会看到：
```
✅ 所有必需的环境变量已配置
✅ Claude API 连接成功
✅ 企业微信推送测试成功，请检查群消息
🎉 所有检查通过！系统配置成功！
```

**同时，企业微信群会收到一条测试消息**：
```
✅ 学术推送系统配置成功！每天早上8点见~
```

---

## 第六步：测试完整推送（1分钟）

配置检查通过后，测试完整的论文推送流程：

1. **选择推送工作流**

   - 左侧选择 `Daily Academic Digest`
   - 右侧点击 `Run workflow` → `Run workflow`

2. **等待运行**

   - 这次会稍长，大约1-2分钟
   - 因为要获取论文、生成摘要等

3. **检查企业微信**

   你应该收到类似这样的推送：

   ```markdown
   # 🎓 学术资讯日报 | 2026-02-26

   ## 📊 今日精选 6 篇论文

   ### 1. [论文标题](链接)
   **作者**: 作者名
   **领域**: Machine Learning

   AI生成的150字中文摘要...

   [📄 查看论文](url) | [💻 查看代码](url)

   ---
   ```

✅ **完成标志**：企业微信收到精美的论文推送消息

---

## 🎉 恭喜！部署完成！

现在系统已经完全配置好了，**每天早上8:00会自动推送**！

### 🔄 自动运行说明

- ⏰ 每天北京时间 **8:00** 自动运行
- 📊 推送 **5-8篇** 最相关论文
- 🤖 使用 **Claude AI** 生成中文摘要
- 💰 每天成本约 **$0.02**

### 🎛️ 可选：调整配置

#### 修改推送时间

1. 编辑文件 `.github/workflows/daily_push.yml`
2. 找到这一行：
   ```yaml
   cron: '0 0 * * *'  # UTC 00:00 = 北京时间 08:00
   ```
3. 修改为其他时间（使用UTC时区）：
   - `0 12 * * *` = 北京时间 20:00
   - `0 22 * * *` = 北京时间 06:00
   - 在线工具：[Crontab Generator](https://crontab.guru/)

#### 修改关注领域

1. 编辑文件 `config/keywords.yml`
2. 添加/删除你感兴趣的关键词
3. 保存后立即生效

#### 修改推送数量

1. 进入 `Settings` → `Secrets and variables` → `Actions`
2. 添加新Secret：
   - Name: `PAPERS_TO_SEND`
   - Value: `8`（想要的数量）

---

## ❓ 常见问题

### Q1: 为什么Actions运行失败？

**检查步骤**：
1. 确认Secrets名称完全正确（大小写敏感）
2. 确认API Key以 `sk-ant-` 开头
3. 确认Webhook以 `https://qyapi.weixin.qq.com/` 开头
4. 查看Actions日志的详细错误信息

### Q2: 如何查看运行日志？

1. `Actions` 标签
2. 点击某次运行记录
3. 点击 `push` 任务
4. 展开各步骤查看输出
5. 可下载日志文件

### Q3: 如何临时停止推送？

1. `Actions` → `Daily Academic Digest`
2. 右上角 `···` → `Disable workflow`
3. 需要恢复时 → `Enable workflow`

### Q4: 没有收到推送怎么办？

**排查步骤**：
1. 检查GitHub Actions是否成功运行（绿色✅）
2. 运行"检查配置"验证设置
3. 查看Actions日志寻找错误
4. 确认企业微信机器人未被删除
5. 手动触发一次测试

### Q5: 推送的论文不相关？

**调整方法**：
1. 编辑 `config/keywords.yml`
2. 添加更多领域关键词到 `must_have`
3. 添加排除关键词到 `exclude`
4. 调整权重配置

### Q6: Claude API额度用完了？

1. 访问 [Claude Console](https://console.anthropic.com/)
2. 进入 `Billing` 页面
3. 点击 `Add credits` 充值（最低$5）
4. 每月成本约$0.6，非常便宜

### Q7: 可以推送到多个群吗？

可以！有两种方法：
1. **简单方法**：创建多个机器人，用`,`分隔多个Webhook（需修改代码）
2. **推荐方法**：在企业微信中设置消息转发

### Q8: 如何备份数据？

系统会自动将日志上传到GitHub Actions：
1. `Actions` → 点击运行记录
2. 下方 `Artifacts` 部分
3. 下载日志文件
4. 日志保留7天

---

## 📚 更多资源

- [配置详解文档](docs/configuration.md)
- [常见问题FAQ](docs/faq.md)
- [提交Issue反馈问题](../../issues)

---

## 💡 使用技巧

1. **收藏关键论文**：看到好论文立即保存链接
2. **定期调整关键词**：根据研究方向更新keywords.yml
3. **查看Actions历史**：了解推送了哪些论文
4. **下载日志**：分析论文趋势

---

**🎉 享受每天的学术资讯吧！有问题随时提Issue！**
