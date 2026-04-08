# Skills

My personal agent skills collection.

## Included Skills

| Skill | Description |
|-------|-------------|
| [dida365](dida365/) | 滴答清单 (TickTick) 任务/项目管理 |
| [cubox](cubox/) | Cubox 稍后读/书签收藏 |
| [workflowy](workflowy/) | Workflowy 大纲笔记管理 |

## Install

```bash
npx skills add https://github.com/fishyer/skills --skill <skill-name>
```

## 环境变量配置

使用前需在 `~/.bashrc` 或对应环境配置中设置以下变量：

### dida365（滴答清单）

| 变量 | 必填 | 说明 |
|------|------|------|
| `DIDA365_ACCESS_TOKEN` | ✅ | OAuth Access Token（有效期 ~180 天） |
| `DIDA365_CLIENT_ID` | ✅ | OAuth Client ID |
| `DIDA365_CLIENT_SECRET` | ✅ | OAuth Client Secret |
| `DIDA365_REDIRECT_URI` | ✅ | OAuth 回调地址 |

获取方式：前往 [Dida365 开发者后台](https://developer.dida365.com/manage) 创建应用，完成 OAuth 授权流程。

### cubox

| 变量 | 必填 | 说明 |
|------|------|------|
| `CUBOX_API_KEY` | ✅ | 完整的 API URL，如 `https://cubox.pro/c/api/save/xxxxxxxxxxxxx` |

获取方式：前往 [Cubox 设置](https://cubox.cc) → 扩展 & 自动化 → API → 启用并复制 API 链接。

### workflowy

| 变量 | 必填 | 说明 |
|------|------|------|
| `WORKFLOWY_API_KEY` | ✅ | API Key |

获取方式：前往 [Workflowy 设置](https://workflowy.com/#/settings) → API → 生成 API Key。
