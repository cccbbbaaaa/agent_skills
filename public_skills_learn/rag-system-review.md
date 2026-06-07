# rag-system-review 学习文档

## 定位

`rag-system-review` 是一个候选 skill，用于审查和改进 RAG 系统，包括数据摄取、chunking、embedding、检索、rerank、上下文组装、引用、生成、评测和线上监控。

它的目标不是“解释 RAG 是什么”，而是给一个可执行的审查框架，帮助快速定位 RAG 质量问题。

## 为什么值得做

如果你要专注 LLM 算法，RAG 是工程和算法结合最强的方向之一。OpenAI 的 file search 文档说明，模型可通过 file search 在生成前检索文件知识库；retrieval 文档进一步说明 vector stores、semantic search、hybrid search 和 chunk/embedding/indexing 是检索系统的基础构件。

参考：

- [OpenAI File search](https://developers.openai.com/api/docs/guides/tools-file-search)
- [OpenAI Retrieval](https://developers.openai.com/api/docs/guides/retrieval)
- [OpenAI Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)

## 适合触发的场景

- “帮我 review 这个 RAG 系统”
- “为什么检索结果不准”
- “怎么设计 RAG eval”
- “chunk size 和 embedding 怎么调”
- “rerank 有没有必要”
- “回答引用不对怎么排查”
- “RAG hallucination 怎么定位”

## 应该包含的工作流

1. 问题定义：业务场景、知识源、用户 query 类型、失败案例。
2. 数据摄取审查：格式、清洗、去重、版本、权限、增量更新。
3. Chunking 审查：chunk size、overlap、标题层级、表格/代码/列表处理。
4. Embedding 审查：模型选择、向量维度、语言覆盖、领域词、成本。
5. Retrieval 审查：top-k、filter、hybrid search、recall、query rewrite。
6. Rerank 审查：reranker 输入、候选数、排序指标、延迟成本。
7. Context assembly：去重、排序、压缩、引用保留、token budget。
8. Generation 审查：回答格式、引用策略、不知道时拒答、事实一致性。
9. Eval 审查：retrieval recall、answer faithfulness、citation accuracy、latency、cost。
10. 线上监控：低置信度、无结果率、引用缺失率、人工反馈闭环。

## 最小产物

- `rag_review_report.md`：系统审查报告。
- `failure_cases.md`：失败样例和归因。
- `retrieval_eval_plan.md`：检索评测计划。
- `answer_eval_plan.md`：生成答案评测计划。
- `improvement_backlog.md`：优先级排序后的改进项。

## 下载方式

当前状态：学习文档，暂不可直接安装。

未来实现为正式 skill 后，下载方式：

```bash
git clone git@github.com:cccbbbaaaa/agent_skills.git
mkdir -p ~/.agents/skills
cp -R agent_skills/skills/rag-system-review ~/.agents/skills/
```

Cursor 适配：

```text
将 skills/rag-system-review/SKILL.md 改写或引用到 .cursor/rules/rag-system-review.mdc
```

Trae 适配：

```text
复制到项目 .agents/skills/rag-system-review/
```

## 后续实现建议

第一版应重点做审查清单和报告模板。第二版再增加脚本，例如：

- 检查测试集字段完整性。
- 统计 retrieval eval 指标。
- 从失败样本生成 failure taxonomy。
