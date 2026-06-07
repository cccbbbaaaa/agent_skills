# XML Prompt Contract 模板

这个模板用于批量 API 调用。默认每条请求只处理一条输入，保证上下文自包含、输出稳定、容易解析。

## 标准模板

```xml
<prompt_contract version="v1.0">
  <background>
    说明业务背景、使用场景、结果消费方，以及为什么这个判断/生成任务重要。
    示例：该任务用于对用户反馈进行批量分类，结果会进入工单分发系统。
  </background>

  <role>
    你是{领域}专家，擅长{核心能力}。你的判断必须稳定、保守，并严格依据输入内容。
  </role>

  <task>
    对<current_input>中的单条数据执行以下任务：
    1. {任务步骤一}
    2. {任务步骤二}
    3. 按<output_schema>输出结果
  </task>

  <input_schema>
    <field name="id" type="string" required="true">源数据唯一标识。</field>
    <field name="text" type="string" required="true">需要处理的原始文本。</field>
    <field name="metadata" type="object" required="false">可选业务上下文。</field>
  </input_schema>

  <requirements>
    <requirement priority="p0">只依据<current_input>和本 prompt 中提供的信息判断，不要引入外部事实。</requirement>
    <requirement priority="p0">输出必须是合法 JSON，不要输出 Markdown、解释、代码块或额外文本。</requirement>
    <requirement priority="p0">如果信息不足，按<edge_cases>中的规则返回兜底值。</requirement>
    <requirement priority="p1">优先保证一致性和可解析性，而不是文采。</requirement>
  </requirements>

  <label_definitions>
    <label name="{标签A}">定义、适用条件、排除条件。</label>
    <label name="{标签B}">定义、适用条件、排除条件。</label>
    <label name="unknown">无法根据输入可靠判断时使用。</label>
  </label_definitions>

  <decision_rules>
    <rule id="1">如果多个标签都可能成立，按{优先级规则}选择。</rule>
    <rule id="2">如果文本为空、乱码或缺少关键信息，返回 unknown。</rule>
    <rule id="3">不要因为关键词命中就直接分类，必须结合语义。</rule>
  </decision_rules>

  <output_schema>
    {
      "id": "string，与输入 id 一致",
      "label": "string，枚举值之一",
      "confidence": "number，0 到 1",
      "reason": "string，20-60 字，说明关键依据",
      "needs_review": "boolean，低置信度或边界样本为 true"
    }
  </output_schema>

  <examples>
    <example id="normal_case">
      <input>{"id":"ex1","text":"{示例输入}"}</input>
      <output>{"id":"ex1","label":"{标签A}","confidence":0.92,"reason":"{简短依据}","needs_review":false}</output>
    </example>
    <example id="edge_case">
      <input>{"id":"ex2","text":"{边界或冲突输入}"}</input>
      <output>{"id":"ex2","label":"unknown","confidence":0.35,"reason":"信息不足，无法可靠判断","needs_review":true}</output>
    </example>
  </examples>

  <edge_cases>
    <case name="empty_input">文本为空时，label 返回 unknown，confidence 不高于 0.2。</case>
    <case name="conflicting_signals">多个标签冲突且无法按规则判定时，needs_review 返回 true。</case>
    <case name="out_of_scope">输入不属于任务范围时，label 返回 unknown。</case>
  </edge_cases>

  <current_input>
    {{CURRENT_INPUT_JSON}}
  </current_input>
</prompt_contract>
```

## 标签选择规则

- 用 `<background>` 解释业务背景，不放具体任务步骤。
- 用 `<role>` 约束专业视角和语气，不塞业务规则。
- 用 `<task>` 写单条输入的处理动作，避免写成整批任务。
- 用 `<requirements>` 写硬约束，尤其是输出格式、禁止额外文本、缺失信息策略。
- 用 `<examples>` 放 3-5 个 few-shot 示例，至少包含一个边界样本。
- 用 `<current_input>` 放变量输入，批处理时每条请求替换这一块。

## 常见变体

分类任务增加 `<label_definitions>` 和 `<decision_rules>`。

抽取任务增加 `<extraction_fields>`，每个字段写清类型、来源、为空策略。

评分任务增加 `<rubric>`，写清分数区间、维度权重和校准样例。

改写任务增加 `<style_guide>`，写清目标读者、语气、长度和禁用表达。
