# PatentManagerSystem

面向实验室场景的专利与软著管理知识库后端 Demo，当前代码以“用户登录/注册 + 首页展示”为主，采用 Flask + SQLAlchemy 的分层结构，便于后续继续扩展业务模块。

## 1. 项目结构讲解（当前实际结构）

```text
PatentManagerSystem/
├── PatentMS.py                 # 启动入口
├── config.py                   # 开发/生产配置
├── app/
│   ├── __init__.py             # Flask 应用工厂、扩展初始化、蓝图注册
│   ├── appRoutes/              # 路由层（Controller）
│   │   ├── loginRoutes.py      # 登录接口
│   │   └── registerRoutes.py   # 注册接口
│   ├── appService/             # 业务层（Service）
│   │   └── UserService.py      # 登录/注册核心逻辑
│   ├── appModels/              # 数据模型层（Model）
│   │   └── UserModel.py        # 用户表定义
│   ├── utils/
│   │   └── ResponseForm.py     # 统一响应格式
│   └── HTML/                   # 前端静态页面与脚本
│       ├── index.html          # 首页
│       ├── login.html          # 登录/注册页面
│       ├── css/login.css
│       └── modules/login.js    # 登录注册交互逻辑
├── instance/patent_knowledge.db# SQLite 数据库文件（运行后生成/使用）
├── logs/PatentMain.log         # 运行日志
└── document/                   # 历史文档与迁移说明（部分内容来自旧项目）
```

### 分层说明

- **Route 层（`app/appRoutes`）**：只负责接收请求、做基础参数检查、调用 Service、返回统一格式。
- **Service 层（`app/appService`）**：封装业务规则（如账号唯一性、密码长度、登录校验）。
- **Model 层（`app/appModels`）**：维护数据结构与 ORM 映射。
- **Utils 层（`app/utils`）**：放与业务无关但可复用的工具（统一响应体）。

> 这种分层很适合后续继续加“专利管理/文档管理/问答”模块：接口层不堆逻辑，复杂规则下沉到 Service，模型清晰可迁移。

---

## 2. 功能概述（便于后续添加功能）

### 当前已有功能

1. **应用启动与初始化**
   - `PatentMS.py` 调用应用工厂创建实例并启动服务。
   - 应用启动后会自动创建数据库表（`db.create_all()`）。

2. **用户注册**（`POST /api/register`）
   - 必填字段校验：`username`、`email`、`password`、`confirm_password`
   - 密码一致性校验
   - 用户名/邮箱唯一性校验
   - 密码长度基础校验（至少 6 位）

3. **用户登录**（`POST /api/login`）
   - 支持“用户名或邮箱 + 密码”登录
   - 密码哈希校验（Werkzeug）
   - 登录成功后写入会话（`session`）

4. **前端页面**
   - `/login`：登录/注册页面
   - `/`：系统首页
   - `login.js` 已封装登录与注册的 fetch 调用流程

### 推荐扩展路径（按优先级）

- **第一阶段（快速可见）**
  - 用户信息接口：`GET /api/user/profile`
  - 登录态校验中间件（统一处理未登录）
  - 统一错误码枚举（替代目前硬编码 code=400）

- **第二阶段（核心业务）**
  - 新增 `PatentModel`、`SoftCopyrightModel`
  - 新增 `appRoutes/patentRoutes.py` + `appService/PatentService.py`
  - 功能：专利条目录入、检索、更新、状态流转

- **第三阶段（管理能力）**
  - RBAC（角色权限）：学生/导师/管理员
  - 审核流（提交-审核-退回）
  - 操作日志与审计字段（创建人、修改人、时间戳）

### 建议新增模块模板

```text
app/
├── appRoutes/
│   └── patentRoutes.py
├── appService/
│   └── PatentService.py
└── appModels/
    └── PatentModel.py
```

保持“Route 只转发 + Service 放业务规则 + Model 管数据结构”的原则，后期维护成本最低。

---

## 3. 使用技术（便于后续限定技术范围）

### 后端

- **Python 3.x**（建议 3.10+）
- **Flask**：Web 框架与路由
- **Flask-SQLAlchemy**：ORM 与数据库访问
- **Flask-CORS**：跨域支持
- **Werkzeug Security**：密码哈希与校验

### 数据与运行

- **SQLite**（当前默认）
  - 连接配置：`sqlite:///patent_knowledge.db`
- **日志系统**：Python `logging`
  - 输出到 `logs/PatentMain.log` + 控制台
- **Session**：Flask 内置会话机制

### 前端（当前页面）

- **HTML + CSS + 原生 JavaScript**
- **Bootstrap 5**（CDN）
- 通过 `fetch` 调用后端 `/api/*` 接口

### 推荐技术边界（后续开发建议）

为保证项目一致性，建议优先使用：

- 后端继续使用 Flask 生态（不混入 Django/FastAPI）
- ORM 统一走 SQLAlchemy（不混写原生 SQL 到各处）
- 鉴权优先从 Session 过渡到 JWT（项目里已有 JWT 配置占位）
- 新接口统一走 `ResponseForm`，避免返回格式不一致

---

## 快速运行

```bash
# 1) 安装依赖（按项目实际环境准备）
pip install flask flask-sqlalchemy flask-cors werkzeug

# 2) 启动
python PatentMS.py
```

启动后访问：

- `http://localhost:5000/login`（登录/注册）
- `http://localhost:5000/`（首页）

---

## 说明

`document/` 目录下存在历史文档（部分仍保留旧项目命名/结构），建议以当前 `app/` 实际代码为准进行后续开发。
