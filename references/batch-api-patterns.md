# 批量 API 调用 Prompt 规范

## 请求组织

每条请求必须能独立运行，不能依赖上一条请求、历史对话或外部临时状态。源数据中的唯一 ID 要进入 `custom_id`，并在模型输出中原样返回，便于回填、排查和重试。

建议每条结果落盘时保存这些字段：

- `custom_id`
- `prompt_version`
- `model`
- `request_body`
- `response_body`
- `status`
- `error`
- `usage`
- `created_at`

## 参数建议

分类、抽取、评分、质检任务：

- `temperature`: `0` 或接近 `0`
- `top_p`: 默认即可，除非已有评测证明需要调整
- `max_output_tokens`: 按输出 schema 估算上限，留少量余量
- `response_format` 或 structured output: 能用 schema 约束时优先使用

摘要、改写、生成任务：

- `temperature`: 通常 `0.2-0.7`，按稳定性和多样性要求调整
- 明确长度、风格、必须保留信息和禁止扩写内容
- 对批处理结果进入生产链路的场景，仍然优先低随机性

## JSONL 请求样例

```jsonl
{"custom_id":"row-0001","method":"POST","url":"/v1/responses","body":{"model":"gpt-4.1-2025-04-14","temperature":0,"max_output_tokens":400,"input":[{"role":"developer","content":"<prompt_contract version=\"v1.0\">...固定 XML Prompt...</prompt_contract>"},{"role":"user","content":"<current_input>{\"id\":\"row-0001\",\"text\":\"用户反馈内容\"}</current_input>"}]}}
```

## Prompt 版本管理

每次修改 prompt 后都要提升版本号。小改输出措辞用 patch 版本，改判断规则用 minor 版本，改输出 schema 用 major 版本。

示例：

- `feedback-classifier-v1.0.0`
- `feedback-classifier-v1.1.0`
- `feedback-classifier-v2.0.0`

## 重试策略

只对可恢复错误重试：

- API 超时
- 429 / 限流
- 5xx
- JSON 解析失败
- schema 校验失败

不要盲目重试业务判断错误。业务判断错误要进入 prompt 修订或人工标注流程。

## 常见风险

- 没有 `custom_id`，导致结果无法回填。
- prompt 中混合多条输入，模型输出漏项或错位。
- 示例和真实输入分布差异太大。
- 输出要求写在自然语言里，但没有 schema 或校验。
- 使用过高 temperature 做分类/抽取。
- 只评测成功样本，没有覆盖空值、乱码、超长、冲突和越界样本。
