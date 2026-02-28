# TravelNote 数据库查看指南

## 📊 数据库概览

### 数据库配置
- **数据库类型**：MySQL
- **数据库名**：`travelnote`
- **用户名**：`travelnote`
- **密码**：`123321`
- **主机**：`localhost`

### 数据库表结构

| 表名 | 说明 | 当前记录数 |
|------|------|-----------|
| `user` | 用户表 | 7 |
| `route` | 路书表 | 12 |
| `conversation` | AI对话记录表 | 149 |
| `travel` | 旅行表 | 38 |
| `bill` | 账单表 | 26 |
| `friend_list` | 好友关系表 | 5 |
| `places` | 地点表 | 0 |
| `photo` | 照片表 | 174 |
| `photo_column` | 照片栏表 | 52 |
| `terminal` | 终端信息表 | 12 |
| `trace` | 轨迹表 | 33 |
| `user_bill` | 用户账单关系表 | 30 |
| `user_travel_list` | 用户旅行关系表 | 57 |
| `agent_scheme` | Agent方案表 | 7 |
| `agent_user` | Agent用户表 | 1 |

---

## 🛠️ 查看数据库的方法

### 方法1：使用 Shell 脚本（最简单）

```bash
# 运行数据库查看脚本
./view_database.sh
```

这会显示：
- 所有数据库表
- 各表的记录数统计
- 常用查询命令列表

### 方法2：使用 Python 脚本（功能最强大）

#### 安装依赖
```bash
pip install pymysql prettytable
```

#### 交互模式
```bash
python query_database.py
```

交互菜单提供以下选项：
1. 显示所有表
2. 显示各表记录数
3. 查询用户列表
4. 查询路书列表
5. 查询AI对话记录
6. 查询旅行列表
7. 自定义SQL查询
8. 显示所有信息
0. 退出

#### 命令行模式
```bash
# 显示所有信息
python query_database.py --all

# 执行自定义SQL查询
python query_database.py --sql "SELECT * FROM user WHERE online_state = 1"
```

### 方法3：使用 MySQL 命令行

#### 进入 MySQL 交互模式
```bash
mysql -u travelnote -p123321 travelnote
```

进入后可以执行各种SQL命令：
```sql
-- 查看所有表
SHOW TABLES;

-- 查看用户
SELECT * FROM user;

-- 查看路书
SELECT * FROM route;

-- 查看最新的AI对话
SELECT * FROM conversation ORDER BY timestamp DESC LIMIT 10;

-- 查看在线用户
SELECT username, email FROM user WHERE online_state = 1;

-- 退出
EXIT;
```

#### 直接执行单条查询
```bash
# 查看所有用户
mysql -u travelnote -p123321 -e "SELECT * FROM travelnote.user;"

# 查看路书统计
mysql -u travelnote -p123321 -e "SELECT user_id, COUNT(*) as count FROM travelnote.route GROUP BY user_id;"

# 查看最新对话
mysql -u travelnote -p123321 -e "SELECT * FROM travelnote.conversation ORDER BY timestamp DESC LIMIT 5;"
```

---

## 📝 常用查询示例

### 1. 查看用户信息
```sql
SELECT id, username, email, signature, online_state 
FROM user;
```

### 2. 查看路书详情
```sql
SELECT 
    r.route_id,
    r.route_name,
    u.username as creator,
    r.create_time,
    r.is_adopted,
    r.belong_travel
FROM route r
LEFT JOIN user u ON r.user_id = u.id
ORDER BY r.create_time DESC;
```

### 3. 查看AI对话记录
```sql
SELECT 
    c.id,
    u.username,
    c.sender,
    LEFT(c.message, 100) as message_preview,
    c.timestamp
FROM conversation c
LEFT JOIN user u ON c.user_id = u.id
ORDER BY c.timestamp DESC
LIMIT 20;
```

### 4. 查看旅行参与情况
```sql
SELECT 
    t.travelName,
    t.travelDestination,
    COUNT(ut.userId) as participant_count,
    t.status
FROM travel t
LEFT JOIN user_travel_list ut ON t.mainTravelId = ut.mainTravelId
GROUP BY t.mainTravelId
ORDER BY t.travelId DESC;
```

### 5. 查看好友关系
```sql
SELECT 
    u1.username as user1,
    u2.username as user2,
    f.status,
    f.nickname_send,
    f.nickname_accept
FROM friend_list f
LEFT JOIN user u1 ON f.id_send = u1.id
LEFT JOIN user u2 ON f.id_accept = u2.id;
```

### 6. 查看账单信息
```sql
SELECT 
    b.bill_id,
    u.username as payer,
    b.amount,
    b.reason,
    b.real_time,
    t.travelName
FROM bill b
LEFT JOIN user u ON b.payer = u.id
LEFT JOIN travel t ON b.travelId = t.travelId
ORDER BY b.real_time DESC
LIMIT 10;
```

### 7. 查看路书采纳情况
```sql
SELECT 
    is_adopted,
    COUNT(*) as count
FROM route
GROUP BY is_adopted;
```

### 8. 查看用户创建的路书数量
```sql
SELECT 
    u.username,
    COUNT(r.id) as route_count
FROM user u
LEFT JOIN route r ON u.id = r.user_id
GROUP BY u.id, u.username
ORDER BY route_count DESC;
```

---

## 🔧 使用 GUI 工具（推荐）

### 1. MySQL Workbench（官方工具）
- 下载地址：https://dev.mysql.com/downloads/workbench/
- 功能：可视化查询、表设计、数据导入导出

连接信息：
- Hostname: localhost
- Port: 3306
- Username: travelnote
- Password: 123321
- Database: travelnote

### 2. DBeaver（跨平台）
- 下载地址：https://dbeaver.io/
- 功能：支持多种数据库、强大的查询工具

### 3. phpMyAdmin（Web界面）
```bash
# 如果已安装phpMyAdmin，可以通过浏览器访问
# 通常地址为：http://localhost/phpmyadmin
```

---

## 📈 数据库监控

### 查看表大小
```sql
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)"
FROM information_schema.TABLES
WHERE table_schema = 'travelnote'
ORDER BY (data_length + index_length) DESC;
```

### 查看数据库总大小
```sql
SELECT 
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Database Size (MB)"
FROM information_schema.TABLES
WHERE table_schema = 'travelnote';
```

---

## ⚠️ 注意事项

1. **备份数据库**：在进行任何修改操作前，建议先备份
   ```bash
   mysqldump -u travelnote -p123321 travelnote > backup_$(date +%Y%m%d).sql
   ```

2. **只读查询**：建议使用 SELECT 语句查看数据，避免误操作

3. **性能考虑**：查询大表时使用 LIMIT 限制返回记录数

4. **字符编码**：数据库使用 utf8mb4 编码，支持完整的 Unicode 字符

---

## 🚀 快速开始

最简单的方式：
```bash
# 1. 查看数据库概览
./view_database.sh

# 2. 使用Python工具进行深入查询
python query_database.py

# 3. 或者直接进入MySQL
mysql -u travelnote -p123321 travelnote
```

---

## 📞 相关文档

- [通讯协议文档](./document/CommunicationDocument.md)
- [数据模型定义](./app/appModels/)
- [API路由说明](./app/appRoutes/)


