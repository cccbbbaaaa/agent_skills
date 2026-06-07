# Agent Skills

用于沉淀对 AI coding 和 agent 工作流有帮助的 skills。这里既可以放自己创建的 skills，也可以放从其他优秀实践中学习、整理、改写后的 skills。

当前包含一个中文优先的 skill：`llm-batch-prompting`，用于为批量大模型调用场景生成稳定、可复用、可校验的 XML Prompt Contract。

另有 `public_skills_learn/` 用于记录热门 skill 方向和学习笔记；`SKILL_IMPORT_GUIDE.md` 记录 Codex、Cursor、Trae 的导入和适配方式。

## 仓库结构

```text
.
├── README.md
├── SKILL_IMPORT_GUIDE.md
├── public_skills_learn/
│   ├── README.md
│   ├── fullstack-feature-planner.md
│   ├── llm-eval-designer.md
│   └── rag-system-review.md
└── skills/
    └── llm-batch-prompting/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── references/
        │   ├── evaluation-checklist.md
        │   ├── prompt-writing-checks.md
        │   └── xml-prompt-template.md
        └── scripts/
            └── validate_prompt_contract.py
```

新增 skill 时，统一放在 `skills/<skill-name>/` 下。仓库根目录尽量只保留仓库级说明和 `skills/` 目录，避免把单个 skill 的实现文件散落在根目录。

候选 skill 或外部学习笔记先放 `public_skills_learn/`；只有真正可触发、可安装的 skill 才进入 `skills/`。

## Skills

| Skill | 说明 | 路径 |
| --- | --- | --- |
| `llm-batch-prompting` | 批量大模型调用场景下的中文 XML Prompt Contract 设计与检查 | `skills/llm-batch-prompting/` |

## 学习文档

| 文档 | 说明 |
| --- | --- |
| `SKILL_IMPORT_GUIDE.md` | Codex、Cursor、Trae 三类 coding 工具的导入和适配方式 |
| `public_skills_learn/llm-eval-designer.md` | LLM eval 设计候选 skill 学习文档 |
| `public_skills_learn/fullstack-feature-planner.md` | 全栈功能规划候选 skill 学习文档 |
| `public_skills_learn/rag-system-review.md` | RAG 系统审查候选 skill 学习文档 |

## Skill: llm-batch-prompting

用于把批量处理任务转成稳定的 XML prompt 模板，适合分类、抽取、打标、评分、摘要、改写、实体标准化和质检等场景。

它重点解决：

- 如何用 `<background>`、`<role>`、`<task>`、`<requirements>`、`<examples>` 等 XML 标签组织 prompt。
- 如何定义输出 schema、兜底策略、边界样本和人工复核规则。
- 如何检查 prompt 是否适合批量复用，而不是只在单条样本上表现正常。
- 如何用小样本评测验证 JSON 可解析率、schema 通过率和业务规则一致性。

## 使用方式

在支持 skills 的 Codex 环境中安装或引用本仓库后，可以直接要求模型使用对应 skill：

```text
使用 llm-batch-prompting，帮我为一批用户反馈分类任务设计一个中文 XML prompt，要求输出 JSON schema，并给出 5 条示例和上线前检查清单。
```

也可以直接阅读：

- `skills/llm-batch-prompting/SKILL.md`：主工作流。
- `skills/llm-batch-prompting/references/xml-prompt-template.md`：XML Prompt Contract 模板。
- `skills/llm-batch-prompting/references/prompt-writing-checks.md`：Prompt 写作与自查规范。
- `skills/llm-batch-prompting/references/evaluation-checklist.md`：上线前评测清单。

## 本地校验

校验 skill 结构：

```bash
python3 /path/to/quick_validate.py skills/llm-batch-prompting
```

校验某个 prompt 文件是否包含核心 XML 标签：

```bash
python3 skills/llm-batch-prompting/scripts/validate_prompt_contract.py path/to/prompt.md
```

## 设计原则

- 可扩展：每个 skill 独立成目录，便于后续继续添加、迁移和维护。
- 可学习：可以吸收外部优秀实践，但要整理成适合本仓库使用的结构和说明。
- 中文优先：主文档、模板和检查清单默认面向中文业务场景。
- Prompt 优先：只关注 prompt 写法和检查，不绑定具体 API 请求格式。
- 批量稳定：每条输入自包含上下文，输出结构固定，异常和边界情况有明确处理规则。
- 可评测：prompt 上线前必须通过小样本评测和格式检查。
