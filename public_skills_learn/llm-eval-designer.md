# llm-eval-designer 学习文档

## 定位

`llm-eval-designer` 是一个候选 skill，用于把 LLM 应用、prompt、RAG、agent workflow 或模型变更转成可重复运行的评测方案。

它应该解决的问题：不要只凭主观感受判断“模型效果变好了”，而是沉淀 dataset、rubric、grader、trace review、回归测试和上线门槛。

## 为什么值得做

最近 skill 生态很强调 eval，因为 skills 本身也需要被测试、评分和回归验证。OpenAI 的 Agent eval 文档明确建议用 traces、graders、datasets 和 eval runs 改善 agent 质量；先用 trace grading 找 workflow 级问题，再用 datasets/eval runs 做可重复评测。

参考：

- [OpenAI Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)
- [OpenAI Codex Skills](https://developers.openai.com/codex/skills)
- [Agent Skills: Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)

## 适合触发的场景

- “帮我设计一个 prompt eval”
- “这个 RAG 改动怎么评估”
- “怎么做 LLM-as-judge”
- “我想给 agent workflow 加回归测试”
- “帮我设计一批测试集和评分 rubric”
- “上线前怎么判断这个模型版本能不能替换旧版本”

## 应该包含的工作流

1. 明确评测对象：prompt、RAG、agent、tool call、分类器、摘要器、抽取器、模型版本。
2. 定义成功标准：准确率、召回率、格式通过率、事实一致性、引用正确率、人工复核率、成本、延迟。
3. 构造数据集：正常样本、边界样本、失败样本、真实线上样本、对抗样本。
4. 设计 rubric：可观察、可评分、避免含糊描述。
5. 选择 grader：规则评分、人工评分、LLM-as-judge、混合评分。
6. 设计实验：baseline、candidate、ablation、回归门槛。
7. 输出结论：是否上线、风险点、下一轮改进建议。

## 最小产物

- `eval_plan.md`：评测目标、指标、样本分层、通过标准。
- `dataset_schema.json`：测试集字段定义。
- `rubric.md`：评分细则。
- `judge_prompt.md`：LLM-as-judge prompt。
- `failure_taxonomy.md`：失败类型分类。
- `release_gate.md`：上线门槛和回滚条件。

## 下载方式

当前状态：学习文档，暂不可直接安装。

未来实现为正式 skill 后，下载方式：

```bash
git clone git@github.com:cccbbbaaaa/agent_skills.git
mkdir -p ~/.agents/skills
cp -R agent_skills/skills/llm-eval-designer ~/.agents/skills/
```

Cursor 适配：

```text
将 skills/llm-eval-designer/SKILL.md 改写或引用到 .cursor/rules/llm-eval-designer.mdc
```

Trae 适配：

```text
复制到项目 .agents/skills/llm-eval-designer/
```

## 后续实现建议

第一版先做 instruction-only skill，不写脚本。等你有固定 eval 数据格式后，再增加 `scripts/validate_eval_dataset.py` 或 `scripts/sample_eval_cases.py`。
