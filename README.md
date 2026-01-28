# 📈 基金智能分析系统

[![GitHub stars](https://img.shields.io/github/stars/ZhuLinsen/daily_stock_analysis?style=social)](https://github.com/ZhuLinsen/daily_stock_analysis/stargazers)
[![CI](https://github.com/ZhuLinsen/daily_stock_analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/ZhuLinsen/daily_stock_analysis/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Ready-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)

> 🤖 基于 AI 大模型的基金智能分析系统，每日自动分析并推送「投资决策仪表盘」到企业微信/飞书/Telegram/邮箱

[English](docs/README_EN.md) | 简体中文

![运行效果演示](./sources/all_2026-01-13_221547.gif)

## ✨ 功能特性

### 🎯 核心功能
- **AI 决策仪表盘** - 一句话核心结论 + 精确买卖时机 + 检查清单
- **多维度分析** - 净值走势 + 持仓结构 + 基金经理分析 + 市场行情
- **市场复盘** - 每日市场概览、板块涨跌、资金流向
- **多渠道推送** - 支持企业微信、飞书、Telegram、邮件（自动识别）
- **零成本部署** - GitHub Actions 免费运行，无需服务器
- **💰 白嫖 Gemini API** - Google AI Studio 提供免费额度，个人使用完全够用
- **🔄 多模型支持** - 支持 OpenAI 兼容 API（DeepSeek、通义千问等）作为备选

### 📊 数据来源
- **基金数据**: AkShare（免费）、天天基金、东方财富
- **新闻搜索**: Tavily、SerpAPI、Bocha
- **AI 分析**: 
  - 主力：Google Gemini（gemini-3-flash-preview）—— [免费获取](https://aistudio.google.com/)
  - 备选：应大家要求，也支持了OpenAI 兼容 API（DeepSeek、通义千问、Moonshot 等）

### 🛡️ 投资理念内置
- ❌ **严禁追高** - 短期涨幅 > 10% 自动标记「危险」
- ✅ **趋势投资** - 中长期趋势向上，回调买入
- 📍 **精确时机** - 买入时机、止损位、目标收益
- 📋 **检查清单** - 每项条件用 ✅⚠️❌ 标记

## 🚀 快速开始

### 方式一：GitHub Actions（推荐，零成本）

**无需服务器，每天自动运行！**

#### 1. Fork 本仓库(顺便点下⭐呀)

点击右上角 `Fork` 按钮

#### 2. 配置 Secrets

进入你 Fork 的仓库 → `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**AI 模型配置（二选一）**

| Secret 名称 | 说明 | 必填 |
|------------|------|:----:|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/) 获取免费 Key | ✅* |
| `OPENAI_API_KEY` | OpenAI 兼容 API Key（支持 DeepSeek、通义千问等） | 可选 |
| `OPENAI_BASE_URL` | OpenAI 兼容 API 地址（如 `https://api.deepseek.com/v1`） | 可选 |
| `OPENAI_MODEL` | 模型名称（如 `deepseek-chat`） | 可选 |

> *注：`GEMINI_API_KEY` 和 `OPENAI_API_KEY` 至少配置一个

**通知渠道配置（可同时配置多个，全部推送）**

| Secret 名称 | 说明 | 必填 |
|------------|------|:----:|
| `WECHAT_WEBHOOK_URL` | 企业微信 Webhook URL | 可选 |
| `FEISHU_WEBHOOK_URL` | 飞书 Webhook URL | 可选 |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token（@BotFather 获取） | 可选 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 可选 |
| `EMAIL_SENDER` | 发件人邮箱（如 `xxx@qq.com`） | 可选 |
| `EMAIL_PASSWORD` | 邮箱授权码（非登录密码） | 可选 |
| `EMAIL_RECEIVERS` | 收件人邮箱（多个用逗号分隔，留空则发给自己） | 可选 |
| `PUSHPLUS_TOKEN` | PushPlus Token（[获取地址](https://www.pushplus.plus)，国内推送服务） | 可选 |
| `CUSTOM_WEBHOOK_URLS` | 自定义 Webhook（支持钉钉等，多个用逗号分隔） | 可选 |
| `CUSTOM_WEBHOOK_BEARER_TOKEN` | 自定义 Webhook 的 Bearer Token（用于需要认证的 Webhook） | 可选 |
| `SINGLE_STOCK_NOTIFY` | 单股推送模式：设为 `true` 则每分析完一只股票立即推送 | 可选 |
| `REPORT_TYPE` | 报告类型：`simple`(精简) 或 `full`(完整)，Docker环境推荐设为 `full` | 可选 |
| `ANALYSIS_DELAY` | 个股分析和大盘分析之间的延迟（秒），避免API限流，如 `10` | 可选 |

> *注：至少配置一个渠道，配置多个则同时推送
>
> 📖 更多配置（Pushover 手机推送、飞书云文档等）请参考 [完整配置指南](docs/full-guide.md)

**其他配置**

| Secret 名称 | 说明 | 必填 |
|------------|------|:----:|
| `FUND_LIST` | 自选基金代码，如 `000001,110022,161725,040046` | ✅ |
| `TAVILY_API_KEYS` | [Tavily](https://tavily.com/) 搜索 API（新闻搜索） | 推荐 |
| `BOCHA_API_KEYS` | [博查搜索](https://open.bocha.cn/) Web Search API（中文搜索优化，支持AI摘要，多个key用逗号分隔） | 可选 |
| `SERPAPI_API_KEYS` | [SerpAPI](https://serpapi.com/) 备用搜索 | 可选 |
| `TUSHARE_TOKEN` | [Tushare Pro](https://tushare.pro/) Token | 可选 |

#### 3. 启用 Actions

进入 `Actions` 标签 → 点击 `I understand my workflows, go ahead and enable them`

#### 4. 手动测试

`Actions` → `每日基金分析` → `Run workflow` → 选择模式 → `Run workflow`

#### 5. 完成！

默认每个工作日 **18:00（北京时间）** 自动执行

### 方式二：本地运行 / Docker 部署

> 📖 本地运行、Docker 部署详细步骤请参考 [完整配置指南](docs/full-guide.md)

## 📱 推送效果

### 决策仪表盘
```
📊 2026-01-10 决策仪表盘
3只基金 | 🟢买入:1 🟡观望:2 🔴卖出:0

🟢 买入 | 易方达蓝筹精选(005827)
📌 净值回调至20日均线支撑，近一年收益率28.5%处于稳健上升通道
💰 操作建议: 逢低买入 | 止损-8% | 目标收益+15%
✅趋势向上 ✅回调充分 ✅基金经理稳定

🟡 观望 | 兴全合润(163406)
📌 短期涨幅12.8%超过10%警戒线，严禁追高
⚠️ 等待回调至均线附近再考虑

---
生成时间: 18:00
```

### 市场复盘

![市场复盘推送效果](./sources/dapan_2026-01-13_22-14-52.png)

```
🎯 2026-01-10 市场复盘

📊 主要指数
- 上证指数: 3250.12 (🟢+0.85%)
- 深证成指: 10521.36 (🟢+1.02%)
- 创业板指: 2156.78 (🟢+1.35%)

📈 市场概况
上涨: 3920 | 下跌: 1349 | 涨停: 155 | 跌停: 3

🔥 板块表现
领涨: 互联网服务、文化传媒、小金属
领跌: 保险、航空机场、光伏设备
```

## ⚙️ 配置说明

> 📖 完整环境变量、定时任务配置请参考 [完整配置指南](docs/full-guide.md)

## 🖥️ 本地 WebUI（可选）

本地运行时，可启用 WebUI 来管理配置和触发分析。

### 启动方式

| 命令 | 说明 |
|------|------|
| `python main.py --webui` | 启动 WebUI + 执行一次完整分析 |
| `python main.py --webui-only` | 仅启动 WebUI，手动触发分析 |

- 访问地址：`http://127.0.0.1:8000`
- 详细说明请参考 [配置指南 - WebUI](docs/full-guide.md#本地-webui-管理界面)

### 功能特性

- 📝 **配置管理** - 查看/修改 `.env` 里的自选基金列表
- 🚀 **快速分析** - 页面输入基金代码，一键触发分析
- 📊 **实时进度** - 分析任务状态实时更新，支持多任务并行

### API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 配置管理页面 |
| `/health` | GET | 健康检查 |
| `/analysis?code=xxx` | GET | 触发单只基金异步分析 |
| `/tasks` | GET | 查询所有任务状态 |
| `/task?id=xxx` | GET | 查询单个任务状态 |

## 📁 项目结构

```
daily_stock_analysis/
├── main.py              # 主程序入口
├── webui.py             # WebUI 入口
├── src/                 # 核心业务代码
│   ├── analyzer.py      # AI 分析器（Gemini）
│   ├── config.py        # 配置管理
│   ├── notification.py  # 消息推送
│   ├── storage.py       # 数据存储
│   └── ...
├── bot/                 # 机器人模块
├── web/                 # WebUI 模块
├── data_provider/       # 数据源适配器
├── docker/              # Docker 配置
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/                # 项目文档
│   ├── full-guide.md    # 完整配置指南
│   └── ...
└── .github/workflows/   # GitHub Actions
```

## 🗺️ Roadmap

> 📢 以下功能将视后续情况逐步完成，如果你有好的想法或建议，欢迎 [提交 Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues) 讨论！

### 🔔 通知渠道扩展
- [x] 企业微信机器人
- [x] 飞书机器人
- [x] Telegram Bot
- [x] 邮件通知（SMTP）
- [x] 自定义 Webhook（支持钉钉、Discord、Slack、Bark 等）
- [x] iOS/Android 推送（Pushover）
- [x] 钉钉机器人 （已支持命令交互 >> [相关配置](docs/bot/dingding-bot-config.md)）
### 🤖 AI 模型支持
- [x] Google Gemini（主力，免费额度）
- [x] OpenAI 兼容 API（支持 GPT-4/DeepSeek/通义千问/Claude/文心一言 等）
- [x] 本地模型（Ollama）

### 📊 数据源扩展
- [x] AkShare（免费）
- [x] Tushare Pro
- [x] Baostock
- [x] YFinance

### 🎯 功能增强
- [x] 决策仪表盘
- [x] 市场复盘
- [x] 定时推送
- [x] GitHub Actions
- [x] 债券基金支持
- [x] Web 管理界面 (简易版)
- [x] 海外基金支持
- [ ] 历史收益回测

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

详见 [贡献指南](docs/CONTRIBUTING.md)

## 📄 License
[MIT License](LICENSE) © 2026 ZhuLinsen

如果你在项目中使用或基于本项目进行二次开发，
非常欢迎在 README 或文档中注明来源并附上本仓库链接。
这将有助于项目的持续维护和社区发展。

## 📬 联系与合作
- GitHub Issues：[提交 Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)

## ⭐ Star History

<a href="https://star-history.com/#ZhuLinsen/daily_stock_analysis&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date" />
 </picture>
</a>

## ⚠️ 免责声明

本项目仅供学习和研究使用，不构成任何投资建议。基金投资有风险，投资需谨慎。作者不对使用本项目产生的任何损失负责。

---

**如果觉得有用，请给个 ⭐ Star 支持一下！**

<!-- 赞赏锚点 -->
<a id="sponsor"></a>
###### ☕ 请我喝杯咖啡
- 如果觉得本项目对你有帮助且行有余力，可以请我喝杯咖啡，支持项目的持续维护与迭代；不赞赏也完全不影响使用。   
<small>（赞赏时可备注联系方式，方便私信致谢与后续交流反馈）</small>
- 感谢支持, 祝您投资顺利，稳健获利。

<div align="center">
  <img src="./sources/wechatpay.jpg" alt="WeChat Pay" width="200" style="margin-right: 20px;">
  <img src="./sources/alipay.jpg" alt="Alipay" width="200">
</div>