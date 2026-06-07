---
name: llm-batch-prompting
description: This skill should be used when the user asks in Chinese or English to design stable prompts for batch LLM calls, create XML prompt templates, write Prompt 101 guidance, improve prompt stability, define output schemas, add examples, or build prompt review and evaluation checks for large-scale model invocation.
---

# 批量大模型 Prompt 设计

## 概览

用于为批量调用大模型的任务设计稳定、可复用、可校验的 Prompt Contract。默认用中文写作，默认 prompt 结构使用 XML 标签，适用于分类、抽取、打标、评分、摘要、改写、实体标准化、质检等批处理场景。

核心目标不是写一个“看起来聪明”的 prompt，而是让几百到几万条输入在同一套规则下稳定输出、容易解析、容易回放、容易评测。

## 设计原则

把 prompt 当成接口契约处理：

1. 每条输入必须自包含上下文，不依赖历史对话。
2. 先定义输出 schema，再写任务说明和示例。
3. 用 XML 标签隔离背景、角色、任务、要求、输入、输出格式、示例和异常处理。
4. 批量任务默认固定 prompt 版本、字段顺序、标签定义和兜底策略。
5. 上全量前必须先抽样评测，覆盖正常样本、边界样本、缺字段样本和脏数据样本。

## 工作流

### 1. 明确批处理任务

先识别任务类型和输出消费方：

- 分类：输出有限标签集合，必须明确标签定义、优先级和兜底标签。
- 抽取：输出字段必须有类型、是否必填、为空策略和证据要求。
- 评分：输出分数区间、评分维度、权重、校准样例。
- 改写：输出风格、长度、禁用词、保留信息、不可改动信息。
- 摘要：输出粒度、受众、长度限制、必须保留和必须忽略的信息。
- 质检：输出问题类型、严重级别、判定依据和是否通过。

### 2. 收集 Prompt Contract 输入

生成 prompt 前，确认这些信息是否存在；缺关键项时先向用户补问，不要直接臆造：

- 业务背景：为什么做这个批处理，结果会被谁使用。
- 输入字段：字段名、类型、含义、是否可能为空。
- 任务目标：每条输入需要模型做什么判断或生成什么。
- 输出 schema：字段名、类型、枚举值、是否必填。
- 业务规则：优先级、边界条件、拒答/跳过条件。
- 示例样本：至少 3 条，最好包含正例、反例、边界例。
- 验收标准：JSON 可解析率、字段完整率、人工抽检准确率、失败重试策略。

### 3. 生成 XML Prompt

默认使用 `references/xml-prompt-template.md` 的结构。核心标签建议保持稳定：

- `<background>`：业务背景和使用场景。
- `<role>`：模型扮演的专业角色。
- `<task>`：单条样本要完成的任务。
- `<input_schema>`：输入字段说明。
- `<requirements>`：硬性规则、判断逻辑、禁止事项。
- `<output_schema>`：输出 JSON schema 或字段契约。
- `<examples>`：3-5 个高质量 few-shot 示例。
- `<edge_cases>`：缺失、冲突、低置信度、无法判断时如何处理。
- `<current_input>`：当前这一条批处理输入变量。

不要把 XML 当成真正要被解析的 XML 文件；它是给模型分隔上下文的结构化标记。标签名要稳定、描述性强，并且在同一项目内保持一致。

### 4. 检查 Prompt 可批量复用性

生成 prompt 后，检查它是否适合批量稳定运行：

- 是否只处理一条 `<current_input>`，避免一次塞入多条导致错位。
- 是否要求输出中返回输入 ID，方便结果回填和人工排查。
- 是否有明确的 `<output_schema>`，并禁止额外解释、Markdown 或代码块。
- 是否有稳定的 `<requirements>` 和 `<decision_rules>`，而不是依赖隐含常识。
- 是否覆盖空值、冲突、越界、低置信度等 `<edge_cases>`。
- 是否提供 3-5 个和真实分布接近的 `<examples>`。
- 是否标注 `prompt_contract version`，方便改版对比。

更多 prompt 写作与自查规则见 `references/prompt-writing-checks.md`。

### 5. 评测与上线前检查

在生成全量批处理前，先要求用户提供或自动构造 20-50 条代表性样本。使用 `references/evaluation-checklist.md` 检查：

- 输出是否始终为目标格式。
- JSON 是否能解析并通过 schema。
- 标签/字段是否符合业务定义。
- 低置信度和缺字段是否按规则兜底。
- prompt 改版后是否保留对比结果。

如用户已有 prompt 文件，可运行 `scripts/validate_prompt_contract.py` 检查关键 XML 标签是否齐全。

## 输出要求

给用户交付时，优先输出以下内容：

1. 一份可直接复用的 XML prompt 模板。
2. 一份输出 schema。
3. 3-5 个示例，包括边界样本。
4. Prompt 自查清单。
5. 小样本评测计划。
6. 可选：XML Prompt Contract 标签校验脚本使用方式。

## 资源

- `references/xml-prompt-template.md`：中文 XML Prompt Contract 模板。
- `references/prompt-writing-checks.md`：Prompt 写作、自查、版本和常见风险规范。
- `references/evaluation-checklist.md`：上线前抽样评测和稳定性检查清单。
- `scripts/validate_prompt_contract.py`：检查 XML Prompt Contract 是否包含关键标签。
