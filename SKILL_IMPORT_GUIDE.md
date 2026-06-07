# Skills 导入与适配指南

本文记录本仓库中的 skills 如何在 Codex、Cursor、Trae 三类 coding 工具中使用。更新时间：2026-06-07。

核心判断：三者对“skill”的原生支持程度不同。Codex 支持 Agent Skills 标准；Trae 已支持 Skills、Skills & Commands、`.agents/skills` 和项目/全局 Skills；Cursor 更接近 Rules + MCP，并不等价于 Codex 的 `SKILL.md` skill。

## 通用结构

Agent Skills 的通用格式是一个目录，至少包含 `SKILL.md`，可选包含 `scripts/`、`references/`、`assets/`、`agents/` 等资源。Agent Skills 官方说明把它定义为“给 AI agents 增加能力和专业知识的轻量开放格式”，并强调 progressive disclosure：先加载 name/description，触发后再读完整 `SKILL.md`。

参考：

- [Agent Skills Overview](https://agentskills.io/home)
- [OpenAI Codex Agent Skills](https://developers.openai.com/codex/skills)
- [OpenAI Academy: Using skills](https://openai.com/academy/skills/)

本仓库约定：

```text
skills/
└── <skill-name>/
    ├── SKILL.md
    ├── agents/
    ├── references/
    ├── scripts/
    └── assets/
```

## Codex

### 原生支持情况

Codex 原生支持 Agent Skills。官方文档说明：skills 可用于 Codex CLI、IDE extension 和 Codex app；skill 是一个包含 `SKILL.md` 的目录，`SKILL.md` 至少需要 `name` 和 `description`；Codex 可以显式通过 `$skill-name` 调用，也可以根据 `description` 隐式触发。

Codex 会扫描这些位置：

- 仓库级：从当前工作目录向上查找 `.agents/skills`
- 用户级：`$HOME/.agents/skills`
- 管理员级：`/etc/codex/skills`
- 系统级：Codex 自带 skills

### 导入公开 skills 市场或官方 curated skills

Codex 官方文档建议用 `$skill-installer` 安装 curated skills，也可以让 installer 从其他仓库下载 skills。

示例：

```text
$skill-installer linear
```

如果是公开 GitHub skills 仓库，优先使用 Codex 内置的 installer；如果 installer 不支持该仓库格式，再手动复制到本地 skills 目录。

### 导入本仓库 skills

用户级安装：

```bash
git clone git@github.com:cccbbbaaaa/agent_skills.git
mkdir -p ~/.agents/skills
cp -R agent_skills/skills/llm-batch-prompting ~/.agents/skills/
```

项目级安装：

```bash
mkdir -p .agents/skills
cp -R /path/to/agent_skills/skills/llm-batch-prompting .agents/skills/
```

使用：

```text
使用 $llm-batch-prompting，帮我为批量用户反馈分类设计一个中文 XML prompt。
```

如果 skill 更新后没有出现，重启 Codex。

## Cursor

### 原生支持情况

Cursor 官方文档当前主要提供 Rules，而不是 Codex/Agent Skills 标准的 `SKILL.md` 原生目录机制。Cursor Rules 用于给 Agent 和 Cmd-K 提供持久化上下文，Project Rules 存放在 `.cursor/rules`，文件格式是 `.mdc`；User Rules 在 Cursor Settings > Rules 中配置；旧版 `.cursorrules` 仍支持但官方建议迁移到 Project Rules。

Cursor 也提供 MCP Servers 页面，用于安装外部工具能力，例如 GitHub、Playwright、Sentry、Vercel 等。MCP 是工具接入，Rules 是行为/流程指导；两者可以配合，但不等同于 Agent Skills。

参考：

- [Cursor Rules](https://docs.cursor.com/context/rules)
- [Cursor MCP Servers](https://docs.cursor.com/en/tools/mcp)

### 导入公开 skills 市场或规则市场

Cursor 没有官方同名“Agent Skills 市场”。可选路径：

- 使用官方 MCP Servers 页面安装工具类能力。
- 从公开 Cursor Rules 仓库学习 `.mdc` 写法，再复制为项目规则。
- 将 Agent Skills 的 `SKILL.md` 改写成 Cursor Project Rule。

### 适配本仓库 skills

建议把一个 skill 转成一个 Agent Requested Project Rule：

```text
.cursor/rules/llm-batch-prompting.mdc
```

示例 `.mdc`：

```mdc
---
description: Use when designing stable Chinese XML prompt contracts for batch LLM tasks.
globs:
  - "**/*.md"
alwaysApply: false
---

# LLM Batch Prompting

When the user asks for batch LLM prompt design, follow:

@skills/llm-batch-prompting/SKILL.md
@skills/llm-batch-prompting/references/xml-prompt-template.md
@skills/llm-batch-prompting/references/prompt-writing-checks.md
```

如果不希望复制完整 skill，也可以把本仓库作为子模块或普通目录放入项目，然后在 `.mdc` 规则里用 `@` 引用具体文件。

## Trae

### 原生支持情况

Trae 当前已经比 Cursor 更接近“skills”概念。Trae changelog 记录了这些能力：

- Settings 已整理出 “Skills & Commands” 和 “Rules” 分组。
- 支持从 `.agents/skills` 目录加载 Skill plugins。
- 支持 global Skills 和 project-level Skills。
- Skills 可用于 IDE mode 和 custom agents。
- SOLO mode 支持上传/添加 Skills，也支持在对话中直接创建 Skills。

Trae 官方站点还说明可创建自定义 agents，并定义它们的 tools、skills 和 logic；通过 MCP 访问外部资源。Rules 方面，Trae 官方文章说明 Rules 可通过 AI Management > Rules 创建，常见文件是 `user_rules.md` 和 `project_rules.md`。

参考：

- [TRAE Changelog](https://www.trae.ai/changelog)
- [TRAE Official Website](https://www.trae.ai/)
- [Best Practices for TRAE Rules](https://www.trae.ai/blog/trae_tutorial_0825?v=1)
- [Trae IDE v1.3.0 supports MCP and .rules](https://traeide.com/zh-tw/news/6)

### 导入公开 skills 市场

优先使用 Trae 内置的 Skills & Commands / Skills 管理入口。工具类能力优先走 MCP Marketplace；流程类能力优先走 Skills；长期行为规范走 Rules。

建议区分：

- Skills：可复用 SOP、流程、检查表、prompt contract。
- Commands：常用操作入口。
- Rules：长期项目规范、编码约束、团队偏好。
- MCP：外部工具和数据源。

### 导入本仓库 skills

项目级方式：

```bash
mkdir -p .agents/skills
cp -R /path/to/agent_skills/skills/llm-batch-prompting .agents/skills/
```

全局方式：在 Trae Skills 管理界面中导入，或按当前 Trae 版本支持的 global Skills 目录导入。

如果 Trae 当前版本没有自动识别某个 skill，可退化为 Rules：

```text
.trae/project_rules.md
```

写法建议：

```md
# 可用 Skills 索引

当用户要求批量大模型 prompt、XML prompt contract、输出 schema、示例和评测清单时，参考：

- `skills/llm-batch-prompting/SKILL.md`
- `skills/llm-batch-prompting/references/xml-prompt-template.md`
- `skills/llm-batch-prompting/references/prompt-writing-checks.md`
```

## 维护建议

- Codex：保持标准 Agent Skill 结构，优先用 `skills/<name>/SKILL.md`。
- Cursor：为每个重要 skill 增加一个 `.cursor/rules/<name>.mdc` 适配层。
- Trae：优先复制到 `.agents/skills`；如果版本支持不稳定，用 `.trae/project_rules.md` 建索引。
- 公共仓库：`public_skills_learn/` 只放学习和规划文档；真正可执行的 skill 放 `skills/`。
