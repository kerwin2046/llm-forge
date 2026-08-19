# LLM-Forge 项目介绍

LLM-Forge 是一个学习型项目，目标是从零搭建一个完整的 LLM 应用开发栈。

## 技术栈

- Python 3.12
- OpenAI SDK（兼容 DeepSeek）
- 向量存储（JSON + 余弦相似度）
- 模型：Agnes-2.0-flash

## 已完成功能

1. 基础调用（SDK + 原生 HTTP）
2. 流式输出（SSE 解析）
3. 多轮会话（ChatSession + 历史管理）
4. 鲁棒性（错误分类 + 指数退避重试 + 上下文截断）
5. Tool Calling（函数定义 + 执行 + 二次调用）
6. RAG（文档切片 + 向量化 + 检索 + 生成）

## 学习路线

项目按 Phase 0-8 推进：
- Phase 0：理解整体生态
- Phase 1-3：基础调用到多轮会话
- Phase 4：生产级鲁棒性
- Phase 5：Tool Calling
- Phase 6：RAG
- Phase 7：Agent（计划中）
- Phase 8：异步并发（可选）

## 运行方式

需要环境变量 DEEPSEEK_API_KEY，然后：
- python main.py （单轮）
- python main_stream.py （流式）
- python main_chat.py （多轮）
- python main_tools.py （工具调用）
- python main_rag.py index docs/example.md （索引）
- python main_rag.py ask "问题" （提问）

## 作者

chenyibw2026，2026 年 8 月开始。
