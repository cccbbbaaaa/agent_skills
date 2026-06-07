# Public Skills Learn

这个目录用于记录值得学习、未来可能落地到本仓库的热门 skill 方向。它不是可直接安装的 skill 目录，而是学习笔记和设计草案。

当前优先记录 3 个方向：

| 候选 skill | 适合你的原因 | 状态 |
| --- | --- | --- |
| `llm-eval-designer` | LLM 算法方向的基础设施，用 eval 约束 prompt、RAG、agent 和模型改动 | 学习文档 |
| `fullstack-feature-planner` | 全栈路线的主干，把需求稳定拆成前端、后端、DB、API、测试、部署 | 学习文档 |
| `rag-system-review` | RAG 是 LLM 应用算法和工程结合最强的落地方向之一 | 学习文档 |

## 学习来源

- [OpenAI Codex Agent Skills](https://developers.openai.com/codex/skills)：学习标准 skill 结构、安装位置、触发方式。
- [Agent Skills Overview](https://agentskills.io/home)：学习跨工具 Agent Skills 标准。
- [OpenAI Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)：学习 traces、graders、datasets、eval runs。
- [OpenAI File search](https://developers.openai.com/api/docs/guides/tools-file-search)：学习知识库检索、vector stores、citation。
- [Cursor Rules](https://docs.cursor.com/context/rules)：学习如何把 skill 思路降级适配为 Cursor rules。
- [TRAE Changelog](https://www.trae.ai/changelog)：跟踪 Trae Skills、Commands、Rules、MCP 的支持状态。

## 下载和落地方式

当前这些文档只是学习材料。未来如果实现成正式 skill，统一放到：

```text
skills/<skill-name>/
```

Codex 安装示例：

```bash
git clone git@github.com:cccbbbaaaa/agent_skills.git
mkdir -p ~/.agents/skills
cp -R agent_skills/skills/<skill-name> ~/.agents/skills/
```

Cursor 适配示例：

```text
.cursor/rules/<skill-name>.mdc
```

Trae 适配示例：

```text
.agents/skills/<skill-name>/
```
