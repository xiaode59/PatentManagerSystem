# 旅游攻略API配置说明

## 概述

本项目已从Coze SDK迁移至使用外部旅游攻略API。新的API提供更简洁的接口和标准化的响应格式。

## 环境变量配置

需要在环境变量或`.env`文件中配置以下参数：

### 必需配置

1. **TRAVEL_API_BASE_URL** - API基础地址
   ```bash
   export TRAVEL_API_BASE_URL="http://your-domain.com"
   ```
   > 默认值：`http://your-domain.com`（请修改为实际的API地址）

2. **TRAVEL_API_KEY** - API访问密钥
   ```bash
   export TRAVEL_API_KEY="sk-travelnote-7f8a2b9c4e1d6f3a8b5c9e2d7f4a1b6c"
   ```
   > 默认值：`sk-travelnote-7f8a2b9c4e1d6f3a8b5c9e2d7f4a1b6c`（请使用你的实际API Key）

## 使用模拟数据进行测试

在`RouteServiceImpl.py`中，有一个开关可以启用模拟数据模式，用于测试：

```python
class RouteServiceImpl(RouteService):
    # 是否启用模拟模式（用于测试）
    USE_MOCK_DATA = True  # 设置为True启用模拟数据，False使用真实API
```

- **True**: 使用内置的模拟数据，不调用实际API（适合开发测试）
- **False**: 调用真实的旅游攻略API

## API接口说明

### 请求格式

```http
POST /api/travel-guide
Content-Type: application/json
X-API-Key: sk-travelnote-7f8a2b9c4e1d6f3a8b5c9e2d7f4a1b6c

{
  "query": "九寨沟旅游攻略",
  "enable_extended_thinking": false
}
```

### 响应格式

```json
{
  "success": true,
  "guide": "**📍 一、目的地概况**\n...",
  "location": [
    {
      "location": "九寨沟风景区",
      "latitude": 33.18523,
      "longitude": 103.9267,
      "placedesc": "九寨沟国家级自然保护区...",
      "placechara": 4
    }
  ]
}
```

### location字段说明

- `location`: 地点名称
- `latitude`: 纬度
- `longitude`: 经度  
- `placedesc`: 地点描述
- `placechara`: 地点类型
  - 0: 娱乐
  - 1: 餐饮
  - 2: 酒店
  - 3: 交通
  - 4: 景区

## 主要改动

### 1. 移除的依赖

- ❌ `cozepy` SDK及相关导入
- ❌ Coze客户端配置
- ❌ 消息提取和清理相关方法

### 2. 新增的功能

- ✅ `_get_api_config()`: 获取API配置
- ✅ `_call_travel_guide_api()`: 调用旅游攻略API
- ✅ 标准HTTP请求（使用`requests`库）
- ✅ 自动转换location格式以匹配数据库结构

### 3. 修改的方法

- `generate_route_from_api()`: 改用新API生成路书
- `talk_to_ai()`: 改用新API处理AI对话
- `handle_talkToAI()` (ReciveMessage.py): 移除cookie处理

## 数据流程

### 用户发起对话

```
用户消息 → WebSocket → handle_talkToAI() 
         ↓
调用 RouteServiceImpl.talk_to_ai()
         ↓
调用 _call_travel_guide_api() 
         ↓
POST /api/travel-guide (带API Key)
         ↓
接收响应 {success, guide, location}
         ↓
保存路书到数据库（如果有location）
         ↓
返回guide文本 + 路书数据
```

### 生成路书

```
生成路书请求 → RouteServiceImpl.generate_route_from_api()
              ↓
调用 _call_travel_guide_api()
              ↓
接收响应并转换location格式
              ↓
保存到数据库
              ↓
返回RouteDTO对象
```

## 错误处理

API调用失败时会抛出异常：

```python
raise Exception(f"调用旅游攻略API失败: {str(e)}")
```

常见错误：
- **连接超时**: 检查`TRAVEL_API_BASE_URL`是否正确
- **401 Unauthorized**: 检查`TRAVEL_API_KEY`是否有效
- **500 Server Error**: API服务端错误，查看详细错误信息

## 测试建议

1. **先使用模拟数据测试**
   ```python
   USE_MOCK_DATA = True
   ```

2. **验证API配置**
   ```bash
   curl -X POST http://your-domain.com/api/travel-guide \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-api-key" \
     -d '{"query": "测试查询"}'
   ```

3. **切换到真实API**
   ```python
   USE_MOCK_DATA = False
   ```

## 注意事项

1. ⚠️ 确保API服务可访问
2. ⚠️ API Key需要保密，不要提交到版本控制
3. ⚠️ 超时时间设置为120秒，长时间查询可能需要调整
4. ⚠️ `metadata`字段已被忽略，只使用`guide`和`location`

