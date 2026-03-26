# 工作日志 - AI开发记录

## 日期: 2026年3月26日
任务内容: 阅读代码并初次编写项目索引
修改文件: 
1. app/utils/prompts.py (新建) - RAG服务提示词和知识库配置
2. document/projectRAG.md (更新) - 项目索引

工作要点:
- 完成git提交: refactor: RAGService敏感信息改环境变量
- 梳理项目为4层架构: Routes → Service → Model → 基础设施
- 编写核心数据结构定义(UserModel, PatentModel, DocumentModel)
- 列出核心函数/方法清单
- 整理外部依赖(Flask, SQLAlchemy, Chromadb, 通义千问API)
- 总结隐式逻辑与"坑"(认证、数据库日期处理、RAG环境变量依赖等)

---
## 日期: 2026年3月26日
任务内容: 将AI问答分离为独立页面
修改文件: 
1. app/HTML/ai-chat.html (新建) - 全新AI问答页面
2. app/HTML/index.html (修改) - 移除内嵌问答，改为入口按钮
3. app/__init__.py (修改) - 添加 /ai-chat 路由

工作要点:
- 创建独立AI问答页面，支持聊天式交互
- 保留快捷问题按钮
- 显示AI状态指示器
- 首页AI卡片改为"进入问答"按钮
- 提交代码
