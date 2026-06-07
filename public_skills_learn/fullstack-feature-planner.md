# fullstack-feature-planner 学习文档

## 定位

`fullstack-feature-planner` 是一个候选 skill，用于把一个产品需求或技术想法拆成可执行的全栈交付计划。

它应该覆盖前端、后端、数据库、API contract、鉴权、状态管理、测试、部署、监控和回滚，而不是只生成一个笼统 TODO list。

## 为什么值得做

你的目标是做全栈，这类 skill 可以成为主干工作流。OpenAI Academy 的 skills 示例中，工程方向包括把 design doc 转成执行计划、把 sprint notes 转成故事和验收标准、标准化 PR description 和 changelog；这些都说明工程类 skills 适合沉淀“需求到交付”的稳定流程。

参考：

- [OpenAI Academy: Using skills](https://openai.com/academy/skills/)
- [OpenAI Codex use cases](https://developers.openai.com/codex/use-cases)
- [OpenAI Codex Skills](https://developers.openai.com/codex/skills)

## 适合触发的场景

- “帮我把这个功能拆成全栈开发计划”
- “这个需求前后端怎么分工”
- “帮我设计 API、DB schema 和页面状态”
- “这个 feature 怎么测试和上线”
- “帮我从 PRD 生成技术实现计划”

## 应该包含的工作流

1. 需求澄清：目标用户、核心路径、非目标、约束、上线时间。
2. 领域建模：实体、关系、状态机、权限边界。
3. API contract：endpoint、request、response、错误码、幂等、分页、鉴权。
4. DB 设计：表结构、索引、迁移、数据回填、兼容策略。
5. 前端设计：页面结构、组件边界、状态管理、加载态、错误态、空态。
6. 后端设计：服务边界、业务逻辑、事务、任务队列、缓存。
7. 测试计划：单测、集成测试、端到端测试、回归样例。
8. 上线计划：feature flag、灰度、监控、日志、回滚。

## 最小产物

- `feature_plan.md`：完整开发计划。
- `api_contract.md`：接口契约。
- `data_model.md`：数据模型和迁移策略。
- `frontend_plan.md`：页面和组件拆解。
- `test_plan.md`：测试和验收清单。
- `release_plan.md`：上线、监控、回滚。

## 下载方式

当前状态：学习文档，暂不可直接安装。

未来实现为正式 skill 后，下载方式：

```bash
git clone git@github.com:cccbbbaaaa/agent_skills.git
mkdir -p ~/.agents/skills
cp -R agent_skills/skills/fullstack-feature-planner ~/.agents/skills/
```

Cursor 适配：

```text
将 skills/fullstack-feature-planner/SKILL.md 改写或引用到 .cursor/rules/fullstack-feature-planner.mdc
```

Trae 适配：

```text
复制到项目 .agents/skills/fullstack-feature-planner/
```

## 后续实现建议

第一版可以只做规划文档生成。第二版再增加模板：

- `references/api-contract-template.md`
- `references/release-checklist.md`
- `references/frontend-state-checklist.md`
- `references/db-migration-checklist.md`
