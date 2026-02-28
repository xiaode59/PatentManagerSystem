# API迁移总结

## 迁移概述

本项目已成功从 **Coze SDK** 迁移至使用 **外部旅游攻略API**（基于API文档）。

迁移日期: 2025-10-21

---

## 主要改动文件

### 1. ✅ `app/appService/ServiceImpl/RouteServiceImpl.py`

#### 移除的内容
- ❌ Coze SDK导入 (`from cozepy import ...`)
- ❌ `_get_coze_client()` 方法
- ❌ `_get_bot_id()` 方法
- ❌ `_extract_text_from_coze_messages()` 方法
- ❌ `_clean_ai_response()` 方法
- ❌ `_is_json_line()` 方法
- ❌ `_is_status_line()` 方法

#### 新增的内容
- ✅ `requests` 库导入（用于HTTP请求）
- ✅ `_get_api_config()` 方法 - 获取API配置
- ✅ `_call_travel_guide_api()` 方法 - 调用旅游攻略API

#### 修改的方法
- **`generate_route_from_api()`**
  - 原：使用Coze SDK的`create_and_poll()`方法
  - 新：使用`_call_travel_guide_api()`发送HTTP POST请求
  - 响应处理：直接从API响应的`guide`和`location`字段提取数据
  
- **`talk_to_ai()`**
  - 原：使用Coze SDK获取聊天回复
  - 新：使用`_call_travel_guide_api()`获取旅游攻略
  - 模拟数据模式：保留原有的模拟数据逻辑
  - 返回值：返回`guide`文本和可选的`route_data`

### 2. ✅ `app/webSocket/ReciveMessage.py`

#### 修改的内容
- **`handle_talkToAI()` 函数**
  - ❌ 移除：硬编码的cookie字符串
  - ❌ 移除：将cookie拼接到消息的逻辑
  - ✅ 简化：直接使用`extra`作为消息内容
  - ✅ 更新：日志消息从"调用AI服务"改为"调用旅游攻略API"
  - ✅ 更新：提示消息从"智能体正在生成答案中"改为"智能体正在生成旅游攻略中"

### 3. ✅ `requirements.txt`

#### 移除的依赖
- ❌ `cozepy>=0.7.0`

#### 保留的依赖
- ✅ `requests>=2.31.0` (已存在，用于HTTP请求)

### 4. 📄 新增文档

- ✅ `API_CONFIG.md` - API配置说明文档
- ✅ `MIGRATION_SUMMARY.md` - 本文件，迁移总结

---

## API规格对比

### 旧API (Coze SDK)

```python
# 初始化客户端
coze_client = Coze(auth=TokenAuth(token=api_key), base_url=COZE_CN_BASE_URL)

# 调用聊天API
chat_poll = coze_client.chat.create_and_poll(
    bot_id=bot_id,
    user_id=str(user_id),
    additional_messages=[Message.build_user_question_text(prompt)]
)

# 提取回复（需要复杂的过滤逻辑）
text = self._extract_text_from_coze_messages(chat_poll.messages)
```

### 新API (HTTP请求)

```python
# 配置
config = {
    'base_url': os.getenv('TRAVEL_API_BASE_URL'),
    'api_key': os.getenv('TRAVEL_API_KEY'),
    'endpoint': '/api/travel-guide'
}

# 请求
response = requests.post(
    url=f"{config['base_url']}{config['endpoint']}",
    headers={
        'Content-Type': 'application/json',
        'X-API-Key': config['api_key']
    },
    json={
        'query': query,
        'enable_extended_thinking': False
    },
    timeout=120
)

# 响应
data = response.json()
# {
#   "success": true,
#   "guide": "markdown攻略内容",
#   "location": [{location, latitude, longitude, placedesc, placechara}]
# }
```

---

## 环境变量配置

### 必需配置

1. **TRAVEL_API_BASE_URL**
   - 说明：旅游攻略API的基础地址
   - 示例：`http://your-domain.com`
   - 默认值：`http://your-domain.com`

2. **TRAVEL_API_KEY**
   - 说明：API访问密钥（使用`X-API-Key`请求头）
   - 示例：`sk-travelnote-7f8a2b9c4e1d6f3a8b5c9e2d7f4a1b6c`
   - 默认值：`sk-travelnote-7f8a2b9c4e1d6f3a8b5c9e2d7f4a1b6c`

### 配置方法

**方法1：系统环境变量**
```bash
export TRAVEL_API_BASE_URL="http://your-domain.com"
export TRAVEL_API_KEY="sk-travelnote-your-actual-key"
```

**方法2：在启动脚本中设置**
```bash
TRAVEL_API_BASE_URL=http://your-domain.com \
TRAVEL_API_KEY=sk-travelnote-your-key \
python TravelNoteMain.py
```

**方法3：使用.env文件**（如果项目支持）
```
TRAVEL_API_BASE_URL=http://your-domain.com
TRAVEL_API_KEY=sk-travelnote-your-key
```

---

## 数据格式变化

### Location数据格式

API返回的`location`字段格式与数据库需求完全匹配：

```python
# API返回格式
{
    "location": "景点名称",
    "latitude": 33.18523,
    "longitude": 103.9267,
    "placedesc": "景点描述",
    "placechara": 4
}

# 转换为数据库格式
{
    "placeName": "景点名称",  # 从location字段映射
    "lat": 33.18523,          # 从latitude字段映射
    "lng": 103.9267,          # 从longitude字段映射
    "placeDesc": "景点描述",   # 从placedesc字段映射
    "placeChara": 4           # 从placechara字段映射
}
```

### placechara类型说明

- `0`: 娱乐场所
- `1`: 餐饮
- `2`: 酒店
- `3`: 交通
- `4`: 景区

---

## 测试模式

### 模拟数据模式

在`RouteServiceImpl.py`中：

```python
class RouteServiceImpl(RouteService):
    # 是否启用模拟模式（用于测试）
    USE_MOCK_DATA = True  # True=模拟数据，False=真实API
```

- **True**: 使用内置模拟数据（北京三日游），不调用实际API
- **False**: 调用真实的旅游攻略API

### 测试流程

1. **开发测试阶段**
   ```python
   USE_MOCK_DATA = True  # 使用模拟数据
   ```

2. **API验证阶段**
   - 设置正确的环境变量
   - 使用curl测试API连通性
   ```bash
   curl -X POST http://your-domain.com/api/travel-guide \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-key" \
     -d '{"query": "测试"}'
   ```

3. **生产环境**
   ```python
   USE_MOCK_DATA = False  # 使用真实API
   ```

---

## 升级步骤

### 对于已部署的实例

1. **备份代码**
   ```bash
   git stash  # 或其他备份方式
   ```

2. **拉取更新**
   ```bash
   git pull origin main
   ```

3. **更新依赖**
   ```bash
   # 如果使用虚拟环境
   source venv/bin/activate
   
   # 卸载旧依赖
   pip uninstall cozepy -y
   
   # 安装/更新依赖
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   ```bash
   export TRAVEL_API_BASE_URL="http://your-actual-api-domain.com"
   export TRAVEL_API_KEY="sk-travelnote-your-actual-key"
   ```

5. **测试验证**
   - 先设置`USE_MOCK_DATA = True`测试基本功能
   - 再设置`USE_MOCK_DATA = False`测试API连接

6. **重启服务**
   ```bash
   # 根据你的部署方式重启服务
   systemctl restart travelnote  # 或其他启动方式
   ```

---

## 兼容性说明

### 保持兼容的功能

- ✅ WebSocket通信协议未改变
- ✅ 数据库schema未改变
- ✅ 路书存储格式未改变
- ✅ 前端接口未改变
- ✅ 历史会话查询未改变

### 行为变化

- ⚠️ AI回复内容格式可能略有不同（取决于新API的生成风格）
- ⚠️ 响应时间可能有变化（取决于新API的性能）
- ⚠️ 不再需要Coze的Bot ID和相关配置

---

## 故障排查

### 常见问题

1. **"调用旅游攻略API失败"**
   - 检查`TRAVEL_API_BASE_URL`是否正确
   - 检查网络连接
   - 检查API服务是否运行

2. **"API返回失败: 无效的API Key"**
   - 检查`TRAVEL_API_KEY`是否正确
   - 检查API Key是否有权限

3. **"Connection timeout"**
   - 检查API地址是否可访问
   - 检查防火墙设置
   - 考虑增加timeout时间（当前120秒）

4. **"ModuleNotFoundError: No module named 'cozepy'"**
   - 正常现象，已移除此依赖
   - 运行 `pip install -r requirements.txt` 确保依赖正确

### 日志检查

关键日志输出：
```
[talk_to_ai] user_id: X, 使用真实旅游攻略API
[talk_to_ai] user_id: X, 调用旅游攻略API获取回复
[talk_to_ai] user_id: X, AI回复已生成，回复长度: XXX
```

错误日志：
```
[talk_to_ai] user_id: X, AI对话处理异常: ...
```

---

## 回滚方案

如果需要回滚到Coze SDK版本：

1. **恢复代码**
   ```bash
   git revert <commit-hash>
   ```

2. **恢复依赖**
   ```bash
   pip install cozepy>=0.7.0
   ```

3. **恢复环境变量**
   ```bash
   export COZE_API_KEY="..."
   export COZE_BOT_ID="..."
   ```

---

## 性能对比

| 指标 | 旧方案(Coze SDK) | 新方案(HTTP API) |
|------|------------------|------------------|
| 依赖复杂度 | 高（SDK + 底层依赖） | 低（仅requests） |
| 请求方式 | SDK封装 | 标准HTTP |
| 响应格式 | 需要复杂提取和清理 | 标准JSON，直接使用 |
| 错误处理 | SDK特定异常 | HTTP标准异常 |
| 可维护性 | 依赖SDK版本 | 独立于SDK |
| 灵活性 | 受SDK限制 | 完全控制 |

---

## 后续优化建议

1. **缓存机制**
   - 对相同查询的结果进行缓存
   - 减少API调用次数

2. **重试机制**
   - 添加自动重试逻辑
   - 实现指数退避

3. **监控告警**
   - 监控API调用成功率
   - 监控响应时间
   - 设置告警阈值

4. **配置管理**
   - 使用配置文件统一管理
   - 支持动态配置更新

---

## 联系支持

如有问题，请查看：
- `API_CONFIG.md` - API配置详细说明
- API文档 - 外部服务接口文档
- 项目代码注释

---

**迁移完成 ✅**

