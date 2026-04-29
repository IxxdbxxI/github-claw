# .agents/skills/

项目级技能目录。每个技能独占一个子目录，遵循统一的约定。

---

## 目录结构约定

```
.agents/skills/
├── README.md          ← 本文件（总索引 + 约定说明）
├── _template/         ← 新技能参考模板（不可直接调用）
│   ├── skill.yml      ← 技能清单（必须）
│   └── README.md      ← 技能说明（必须）
└── <skill-name>/      ← 具体技能目录
    ├── skill.yml
    └── README.md
```

---

## skill.yml 字段说明

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `name` | string | ✓ | 技能唯一标识符，与目录名一致 |
| `version` | string | ✓ | 语义化版本号，如 `1.0.0` |
| `description` | string | ✓ | 一句话描述技能用途 |
| `usage` | string | ✓ | 如何在对话或工作流中触发该技能 |
| `tags` | list | - | 分类标签，用于发现 |
| `requires` | list | - | 依赖的其他技能或外部工具 |

---

## 技能生命周期

### 发现（Discovery）
Claw 在每次会话开始时读取 `AGENTS.md`，其中包含对本目录的引用。
需要了解可用技能时，直接列举 `.agents/skills/` 下的子目录并读取各自的 `skill.yml`。

### 安装（Installation）
在 `.agents/skills/` 下创建新的子目录，至少包含 `skill.yml` 和 `README.md`，然后提交到仓库。
安装即提交 — 技能存在于仓库中即视为已安装。

### 使用（Usage）
在对话或任务中，通过技能的 `usage` 字段描述的方式触发。
Claw 读取对应技能目录的文件后按说明执行。

---

## 已注册技能

| 技能目录 | 版本 | 简介 |
|---|---|---|
| `_template` | — | 参考模板，不可直接调用 |

> 每次新增技能后，请更新上表。
