# Prompt Skill

面向批量大模型调用场景的 Prompt 设计 skill 仓库。当前包含一个中文优先的 skill：`llm-batch-prompting`，用于生成稳定、可复用、可校验的 XML Prompt Contract。

## 仓库结构

```text
.
├── README.md
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

## Skill: llm-batch-prompting

用于把批量处理任务转成稳定的 XML prompt 模板，适合分类、抽取、打标、评分、摘要、改写、实体标准化和质检等场景。

它重点解决：

- 如何用 `<background>`、`<role>`、`<task>`、`<requirements>`、`<examples>` 等 XML 标签组织 prompt。
- 如何定义输出 schema、兜底策略、边界样本和人工复核规则。
- 如何检查 prompt 是否适合批量复用，而不是只在单条样本上表现正常。
- 如何用小样本评测验证 JSON 可解析率、schema 通过率和业务规则一致性。

## 使用方式

在支持 skills 的 Codex 环境中安装或引用本仓库后，可以直接要求模型使用该 skill：

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

- 中文优先：主文档、模板和检查清单默认面向中文业务场景。
- Prompt 优先：只关注 prompt 写法和检查，不绑定具体 API 请求格式。
- 批量稳定：每条输入自包含上下文，输出结构固定，异常和边界情况有明确处理规则。
- 可评测：prompt 上线前必须通过小样本评测和格式检查。
