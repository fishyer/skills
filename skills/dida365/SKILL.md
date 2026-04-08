---
name: dida365
description: "Manage tasks and projects in Dida365 (滴答清单/TickTick) via Open API. Use when the user wants to create, read, update, complete, delete, or query tasks/projects in Dida365."
---

# Dida365 (滴答清单) Skill

通过 Dida365 Open API 管理滴答清单的任务和项目。

## 认证

Access Token 存储在环境变量 `DIDA365_ACCESS_TOKEN` 中。

所有请求需携带 Header: `Authorization: Bearer $DIDA365_ACCESS_TOKEN`

## API Base URL

```
https://api.dida365.com/open/v1
```

## 概念模型

- **Project**: 项目/清单，任务的容器。字段: `id`, `name`, `color`, `viewMode`(list/kanban/timeline), `kind`(TASK), `groupId`, `closed`, `permission`, `sortOrder`
- **Task**: 任务，隶属于 Project。字段: `id`, `projectId`, `title`, `content`, `desc`, `tags`, `priority`(0-5, 0=无, 5=最高), `status`(0=未完成, 2=已完成), `startDate`, `dueDate`, `timeZone`, `isAllDay`, `reminders`, `repeatFlag`, `items`(子任务), `sortOrder`, `kind`(TEXT), `etag`, `modifiedTime`
- **ChecklistItem**: 子任务/清单项。字段: `id`, `title`, `status`(0/2), `startDate`, `completedTime`, `sortOrder`

## API 端点

### 项目 (Project)

| 操作 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 列出所有项目 | GET | `/project` | 返回所有项目列表 |
| 获取项目详情 | GET | `/project/{projectId}/data` | 返回项目+未完成任务+列信息 |
| 创建项目 | POST | `/project` | Body: `{name, color?, sortOrder?, viewMode?, kind?}` |
| 更新项目 | POST | `/project/{projectId}` | Body: 同创建，需包含 `id` |
| 删除项目 | DELETE | `/project/{projectId}` | 危险操作，需确认 |

### 任务 (Task)

| 操作 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 创建任务 | POST | `/task` | Body: `{title, projectId, content?, priority?, dueDate?, startDate?, isAllDay?, reminders?, tags?, items?}` |
| 获取任务 | GET | `/project/{projectId}/task/{taskId}` | 获取单个任务详情 |
| 更新任务 | POST | `/project/{projectId}/task/{taskId}` | Body: 需包含 `id`, `etag` |
| 完成任务 | POST | `/project/{projectId}/task/{taskId}/complete` | Body: 需包含 `id`, `etag` |
| 删除任务 | DELETE | `/project/{projectId}/task/{taskId}` | 危险操作，需确认 |
| 已完成任务 | GET | `/project/{projectId}/task/completed?limit=50&offset=0` | 分页查询已完成任务 |

### 日期格式

- 日期时间: `2026-04-08T09:00:00.000+0800` (RFC 3339 带时区)
- 全天任务: `isAllDay: true`, 日期格式 `2026-04-08T00:00:00.000+0800`

### 优先级

- 0: 无优先级
- 1: 低
- 3: 中
- 5: 高

### 重复规则 (repeatFlag)

- `RRULE:FREQ=DAILY` 每天重复
- `RRULE:FREQ=WEEKLY` 每周重复
- `RRULE:FREQ=MONTHLY` 每月重复
- `RRULE:FREQ=YEARLY` 每年重复

## 使用方式

所有 API 调用通过 `curl` 命令执行。示例：

```bash
# 列出所有项目
curl -s "https://api.dida365.com/open/v1/project" \
  -H "Authorization: Bearer $DIDA365_ACCESS_TOKEN"

# 获取项目数据（含任务）
curl -s "https://api.dida365.com/open/v1/project/{projectId}/data" \
  -H "Authorization: Bearer $DIDA365_ACCESS_TOKEN"

# 创建任务
curl -s -X POST "https://api.dida365.com/open/v1/task" \
  -H "Authorization: Bearer $DIDA365_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"任务标题","projectId":"xxx","priority":0}'

# 完成任务（需要 id 和 etag）
curl -s -X POST "https://api.dida365.com/open/v1/project/{projectId}/task/{taskId}/complete" \
  -H "Authorization: Bearer $DIDA365_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id":"taskId","etag":"xxx"}'

# 删除任务
curl -s -X DELETE "https://api.dida365.com/open/v1/project/{projectId}/task/{taskId}" \
  -H "Authorization: Bearer $DIDA365_ACCESS_TOKEN"
```

## 注意事项

- 删除操作（项目/任务）需先向用户确认
- 更新和完成任务需要 `etag` 字段（乐观锁），先 GET 获取最新 etag
- `projectId` 必须是有效的项目 ID，可通过 GET `/project` 获取
- Token 有效期约 180 天（15551999 秒），过期后需重新 OAuth 授权
- OAuth 凭证: Client ID 和 Secret 存储在环境变量 `DIDA365_CLIENT_ID` 和 `DIDA365_CLIENT_SECRET` 中
- OAuth redirect URI: `DIDA365_REDIRECT_URI`
