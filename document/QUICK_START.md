# 快速开始指南 - API迁移后

## 1️⃣ 最少配置启动（5分钟）

### 步骤1: 设置环境变量

在终端执行：
```bash
export TRAVEL_API_BASE_URL="http://your-domain.com"
export TRAVEL_API_KEY="sk-travelnote-7f8a2b9c4e1d6f3a8b5c9e2d7f4a1b6c"
```

> ⚠️ 请将`your-domain.com`替换为实际的API域名

### 步骤2: 选择运行模式

编辑 `app/appService/ServiceImpl/RouteServiceImpl.py`：

```python
# 第23行左右
USE_MOCK_DATA = True   # 测试模式：使用模拟数据
# 或
USE_MOCK_DATA = False  # 生产模式：调用真实API
```

### 步骤3: 安装依赖并启动

```bash
# 激活虚拟环境（如果有）
source venv/bin/activate

# 更新依赖
pip install -r requirements.txt

# 启动服务
python TravelNoteMain.py
```

---

## 2️⃣ 验证API连接

### 使用curl测试API

```bash
curl -X POST http://your-domain.com/api/travel-guide \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-travelnote-7f8a2b9c4e1d6f3a8b5c9e2d7f4a1b6c" \
  -d '{"query": "北京旅游攻略"}'
```

### 预期响应

```json
{
  "success": true,
  "guide": "**📍 一、目的地概况**\n北京...",
  "location": [
    {
      "location": "故宫博物院",
      "latitude": 39.9163,
      "longitude": 116.3972,
      "placedesc": "...",
      "placechara": 4
    }
  ]
}
```

---

## 3️⃣ WebSocket测试

### 连接WebSocket

```javascript
const socket = io('http://localhost:7777');

// 发送AI对话请求
socket.emit('message', JSON.stringify({
  task: 'talkToAI',
  extra: '九寨沟旅游攻略'
}));

// 监听响应
socket.on('talkToAI', (data) => {
  console.log('AI回复:', data);
});

socket.on('routeGenerate', (data) => {
  console.log('路书生成:', data);
});
```

---

## 4️⃣ 环境变量配置方式

### 方式A: 命令行临时设置

```bash
export TRAVEL_API_BASE_URL="http://your-domain.com"
export TRAVEL_API_KEY="your-api-key"
python TravelNoteMain.py
```

### 方式B: 启动脚本

创建 `start.sh`:
```bash
#!/bin/bash
export TRAVEL_API_BASE_URL="http://your-domain.com"
export TRAVEL_API_KEY="your-api-key"
python TravelNoteMain.py
```

执行：
```bash
chmod +x start.sh
./start.sh
```

### 方式C: 使用.env文件（如果项目支持）

创建 `.env`:
```
TRAVEL_API_BASE_URL=http://your-domain.com
TRAVEL_API_KEY=your-api-key
```

---

## 5️⃣ 常见问题快速修复

### ❌ "ModuleNotFoundError: No module named 'cozepy'"

**原因**: 旧依赖未清理

**解决**:
```bash
pip uninstall cozepy -y
pip install -r requirements.txt
```

### ❌ "调用旅游攻略API失败: Connection refused"

**原因**: API地址不正确或服务未启动

**解决**:
1. 检查`TRAVEL_API_BASE_URL`是否正确
2. 确认API服务正在运行
3. 测试网络连接: `ping your-domain.com`

### ❌ "API返回失败: 无效的API Key"

**原因**: API Key错误

**解决**:
1. 检查`TRAVEL_API_KEY`是否正确
2. 确认API Key有访问权限
3. 检查请求头是否正确设置

### ⚠️ 响应很慢

**原因**: 使用真实API且查询复杂

**临时解决**:
```python
# 切换到模拟数据模式测试
USE_MOCK_DATA = True
```

---

## 6️⃣ 测试路径

### 完整测试流程

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 使用模拟数据测试
# 编辑RouteServiceImpl.py: USE_MOCK_DATA = True
python TravelNoteMain.py
# 测试WebSocket或API接口

# 3. 测试真实API连接
curl -X POST http://your-domain.com/api/travel-guide \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{"query": "测试"}'

# 4. 切换到真实API
# 编辑RouteServiceImpl.py: USE_MOCK_DATA = False
python TravelNoteMain.py
# 再次测试

# 5. 检查日志
tail -f logs/app.log  # 如果有日志文件
```

---

## 7️⃣ 代码修改检查清单

- ✅ `RouteServiceImpl.py` - 已更新为使用HTTP API
- ✅ `ReciveMessage.py` - 已移除cookie处理
- ✅ `requirements.txt` - 已移除cozepy依赖
- ✅ 环境变量 - 已配置`TRAVEL_API_BASE_URL`和`TRAVEL_API_KEY`

---

## 8️⃣ 性能建议

### 开发环境
```python
USE_MOCK_DATA = True  # 快速响应，无需API调用
```

### 测试环境
```python
USE_MOCK_DATA = False  # 验证API集成
# 设置较短的超时
timeout=30  # 修改_call_travel_guide_api()中的timeout参数
```

### 生产环境
```python
USE_MOCK_DATA = False  # 使用真实API
timeout=120  # 保持默认超时
```

---

## 9️⃣ 监控要点

### 关键日志

成功日志：
```
[talk_to_ai] user_id: X, 使用真实旅游攻略API
[talk_to_ai] user_id: X, AI回复已生成，回复长度: 1234
```

失败日志：
```
[talk_to_ai] user_id: X, AI对话处理异常: ...
```

### 监控指标

- API调用成功率
- 平均响应时间
- 生成路书数量
- 错误率

---

## 🔟 获取帮助

遇到问题？按顺序检查：

1. **查看日志** - 找到错误详细信息
2. **检查配置** - 确认环境变量是否正确
3. **测试API** - 使用curl验证API连接
4. **切换模拟** - 使用`USE_MOCK_DATA=True`排除API问题
5. **查看文档** - `API_CONFIG.md`和`MIGRATION_SUMMARY.md`

---

## 📋 配置模板

### 最小配置

```bash
# 必需
export TRAVEL_API_BASE_URL="http://api.example.com"
export TRAVEL_API_KEY="sk-travelnote-xxxxx"

# 启动
python TravelNoteMain.py
```

### 完整配置

```bash
# API配置
export TRAVEL_API_BASE_URL="http://api.example.com"
export TRAVEL_API_KEY="sk-travelnote-xxxxx"

# Flask配置
export FLASK_ENV="production"
export FLASK_DEBUG="False"

# JWT配置
export JWT_SECRET_KEY="your-secret-key"

# 启动
python TravelNoteMain.py
```

---

**现在就可以启动了！** 🚀

建议第一次启动时使用`USE_MOCK_DATA = True`进行测试。

