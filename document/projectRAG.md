# 项目索引 - PatentMS 专利管理系统

## 日期: 2026年3月26日
任务内容: 阅读代码并初次编写项目索引
修改文件: 
1. app/utils/prompts.py (新建)

---

## 一、分层架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      表现层 (Routes)                         │
├─────────────────────────────────────────────────────────────┤
│  loginRoutes.py  │  registerRoutes.py  │  aiRoutes.py      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      服务层 (Service)                       │
├─────────────────────────────────────────────────────────────┤
│  UserService  │  PatentService  │  RAGService              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      模型层 (Models)                        │
├─────────────────────────────────────────────────────────────┤
│  UserModel  │  PatentModel  │  DocumentModel               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      基础设施                               │
├─────────────────────────────────────────────────────────────┤
│  Flask-SQLAlchemy  │  ChromaDB向量库  │  通义千问API        │
└─────────────────────────────────────────────────────────────┘
```

**调用链路**:
1. 用户请求 → Routes 路由处理
2. Routes 调用 Service 层业务逻辑
3. Service 操作 Model / 外部API / 向量数据库
4. Model 映射数据库表
5. 响应通过 ResponseForm 统一格式返回

---

## 二、核心数据结构定义

### 1. UserModel (用户表)
```python
class UserModel(db.Model):
    id: int                      # 主键
    username: str(50)            # 用户名(唯一)
    email: str(100)             # 邮箱(唯一)
    password_hash: str(200)     # 密码哈希
    role: str(20)               # 角色: student/admin
    created_at: datetime        # 创建时间
```

### 2. PatentModel (专利/软著表)
```python
class PatentModel(db.Model):
    id: int                      # 主键
    name: str(200)               # 名称
    type: str(20)                # 类型: invention/utility/software
    application_no: str(50)     # 申请号
    registration_no: str(50)    # 登记号
    applicant: str(100)         # 申请人
    inventor: str(100)          # 发明人
    status: str(20)             # 状态: applied/published/examining/granted/rejected/withdrawn
    application_date: Date      # 申请日
    publish_date: Date          # 公开日
    grant_date: Date            # 授权日
    description: Text            # 摘要描述
    created_by: int              # 外键→users.id
    created_at: datetime         # 创建时间
    updated_at: datetime         # 更新时间
```

### 3. DocumentModel (知识库文档表)
```python
class DocumentModel(db.Model):
    id: int                      # 主键
    title: str(200)              # 文档标题
    category: str(50)            # 分类标签
    file_path: str(500)          # 文件路径
    file_type: str(20)           # 文件类型: pdf/mp4/txt/doc/docx
    content_text: Text           # 文本内容(用于检索)
    description: Text            # 描述
    tags: str(200)               # 标签(逗号分隔)
    is_vectorized: bool          # 是否已向量化
    created_by: int              # 外键→users.id
    created_at: datetime         # 创建时间
    updated_at: datetime         # 更新时间
```

### 4. ResponseForm (统一响应格式)
```python
{
    'code': int,           # 200成功/400失败
    'success': bool,
    'message': str,
    'data': dict|None,
    'timestamp': str      # 时间戳
}
```

---

## 三、核心函数/方法清单

### 3.1 app/__init__.py

| 函数签名 | 输入参数 | 返回值 | 核心逻辑 |
|---------|---------|-------|---------|
| `create_app(config_name)` | config_name: str | Flask app | 创建Flask应用，初始化扩展、注册蓝图、创建数据库表 |

### 3.2 appRoutes

| 模块 | 路由 | 方法 | 功能 |
|-----|-----|------|------|
| loginRoutes | `/api/login` | POST | 用户登录 |
| registerRoutes | `/api/register` | POST | 用户注册 |
| aiRoutes | `/api/ai/ask` | POST | AI问答 |
| aiRoutes | `/api/ai/status` | GET | 获取AI状态 |
| aiRoutes | `/api/ai/init-db` | POST | 初始化向量数据库 |
| aiRoutes | `/api/ai/search` | POST | 知识库搜索 |

### 3.3 UserService

| 函数签名 | 输入参数 | 返回值 | 核心逻辑 |
|---------|---------|-------|---------|
| `login_user(username, password)` | str, str | dict | 查询用户，验证密码hash，返回user_id和role |
| `register_user(username, email, password)` | str, str, str | dict | 检查用户名/邮箱唯一性，密码长度≥6，创建用户 |

### 3.4 PatentService

| 函数签名 | 输入参数 | 返回值 | 核心逻辑 |
|---------|---------|-------|---------|
| `get_all_patents(page, per_page, keyword, status, patent_type)` | 分页+筛选参数 | dict | 多条件模糊查询，分页返回专利列表 |
| `get_patent_by_id(patent_id)` | int | dict | 根据ID查询专利 |
| `create_patent(data)` | dict | dict | 创建专利记录 |
| `update_patent(patent_id, data)` | int, dict | dict | 更新专利记录 |
| `delete_patent(patent_id)` | int | dict | 删除专利记录 |
| `get_statistics()` | - | dict | 统计专利总数、按类型/状态分组计数 |

### 3.5 RAGService

| 函数签名 | 输入参数 | 返回值 | 核心逻辑 |
|---------|---------|-------|---------|
| `initialize()` | - | dict | 初始化ChromaDB向量数据库 |
| `add_documents(documents, metadatas, ids)` | list | dict | 添加文档到向量库 |
| `similarity_search(query, top_k)` | str, int | dict | 向量相似度搜索 |
| `get_collection_info()` | - | dict | 获取集合信息(文档数) |
| `build_knowledge_base()` | - | dict | 构建示例专利知识库 |
| `generate_answer(query)` | str | dict | RAG+LLM生成回答 |

---

## 四、外部依赖与环境

### 4.1 Python依赖
- **Flask** - Web框架
- **Flask-SQLAlchemy** - ORM
- **Flask-CORS** - 跨域支持
- **SQLite** - 关系型数据库
- **Chromadb** - 向量数据库
- **OpenAI** - 通义千问API客户端
- **Werkzeug** - 密码哈希

### 4.2 第三方API
- **阿里云通义千问** (`https://dashscope.aliyuncs.com`)
  - 模型: `qwen-plus`
  - 环境变量: `DASHSCOPE_API_KEY`

### 4.3 环境变量
| 变量名 | 说明 | 示例 |
|--------|------|------|
| `DASHSCOPE_API_KEY` | 通义千问API密钥 | `sk-xxxx` |
| `DASHSCOPE_BASE_URL` | API地址 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `DASHSCOPE_MODEL` | 模型名称 | `qwen-plus` |

### 4.4 配置文件 (config.py)
- `SECRET_KEY` - Flask会话密钥
- `SQLALCHEMY_DATABASE_URI` - SQLite数据库路径
- `JWT_SECRET_KEY` / `JWT_ACCESS_TOKEN_EXPIRES` - JWT配置(预留)

---

## 五、隐式逻辑与"坑"

### 5.1 认证相关
- **密码存储**: 使用Werkzeug的`generate_password_hash`/`check_password_hash`，不要自己写hash
- **登录方式**: 支持用户名或邮箱登录 (UserService.login_user先查username，再查email)
- **会话管理**: 使用Flask session，role存储在session中

### 5.2 数据库相关
- **日期字段处理**: PatentModel中使用Date类型，创建/更新时需用`datetime.strptime(value, '%Y-%m-%d').date()`转换
- **软删除**: 当前未实现物理删除，使用`delete_patent`会直接删除记录(无软删除)

### 5.3 RAG服务相关
- **环境变量依赖**: RAGService初始化时从环境变量读取API Key，为空会调用失败
- **调试日志**: generate_answer()会将回复保存至`logs/rag_debug/rag_response_{timestamp}.json`
- **fallback机制**: LLM调用失败时返回`_mock_answer()`模拟回答(关键词匹配)

### 5.4 前端相关
- **静态文件**: Flask的static_folder指向`HTML`目录
- **模板**: template_folder指向`HTML`目录
- **API响应**: 统一使用ResponseForm包装，支持前端统一处理

### 5.5 其他
- **运行日志**: `logs/PatentMain.log`，Flask自动reload时会检测代码变化
- **向量数据库**: 使用ChromaDB持久化存储在`instance/vector_db`目录

---

## 六、项目目录结构

```
/home/ubuntu/graduation/BACKUP/
├── PatentMS.py              # 启动入口
├── config.py                # 配置文件
├── venv/                    # Python虚拟环境
├── logs/                    # 日志目录
│   ├── PatentMain.log      # 主日志
│   └── rag_debug/          # RAG调试日志
├── instance/                # Flask实例数据
│   └── vector_db/           # ChromaDB向量库
├── HTML/                    # 前端静态文件
├── app/
│   ├── __init__.py         # Flask应用创建
│   ├── appRoutes/          # 路由层
│   │   ├── aiRoutes.py
│   │   ├── loginRoutes.py
│   │   └── registerRoutes.py
│   ├── appService/         # 服务层
│   │   ├── RAGService.py
│   │   ├── PatentService.py
│   │   └── UserService.py
│   ├── appModels/          # 模型层
│   │   ├── UserModel.py
│   │   ├── PatentModel.py
│   │   └── DocumentModel.py
│   └── utils/              # 工具模块
│       ├── ResponseForm.py
│       └── prompts.py      # RAG提示词配置
└── document/               # 文档目录
    ├── AI_log.md           # 工作日志
    └── projectRAG.md       # 项目索引(本文档)
```
