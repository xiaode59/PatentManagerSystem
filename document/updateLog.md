2025.2.21
 1.0.0
- 开始采用更新日志
- 修复了register部分函数书写错误
- 修复了payer显示问题
- 调整了Bill获取函数
- 完善newMassage返回值,现在支持travel通知
- 打开自动更新

2025.2.22
 1.0.1
 - 修复了register部分函数书写错误
 - 增加了修改头像节点(/modifyAvatar)
 - 修改了自动更新节点(/autoCreateTravelRoute)的返回值显示
 - 将自动更新节点调整为北京时间
 - 增加修改旅游封面节点(/modifyTravelCover)(暂定)
 - 修复了旅游结束但用户与旅游关系未结束的bug
 - 修复了获取节点的部分bug
 ~~TODO: 修复不能确定添加好友发起方的bug~~

2025.2.23
 1.0.2
 - 修复不能确定添加好友发起方的bug
 - 优化了添加头像节点的逻辑
 - 优化了TravelRoutes部分代码命名
~~TODO: 继续优化TravelRoutes~~
~~TODO: 优化BillRoutes事务逻辑~~

2025.2.24
 1.0.3
 - 修复了部分没改名的地方
TODO: 优化testTools

2025.3.7
 1.1.0
 - 增加了websocket连接模式
 - 为billRoutes添加了websocket通知
 - 为loginRoutes添加了token验证
 - 给Bill类型添加一个travel_id字段

2025.3.9
 1.1.1
 - 为travelRoutes添加了websocket通知
 - 为friendRoutes添加了websocket通知
 - 修复了websocket断开后字典不删除的bug
 - 修复了websocket广播所有人的bug
 - 修复了travelRoutes中函数名错误的bug
~~TODO: 将全局字典改为hash表~~

2025.3.18
 1.1.2
 - 为billModel新增两列：pay_method和merchant
 - 解决nohup文件过大的问题
    1. 新增脚本文件truncate_nohup.sh
    2. 使用crontab -e    0 * * * * /root/TravelNote-Backend/truncate_nohup.sh添加定时任务，每小时发动一次
    3. 使用crontab -l查看定时任务
 - 添加退出旅游节点(/exitTravel)
 - 修复了自动更新失败的bug

2025.3.19
 1.1.3
 - 修复了退出的人还会再旅游中显示的bug
 - 为Bill增加两个值
 - 修复了账单发起人会给自己发通知的bug
 - 将token换成flask扩展版flask_jwt_extended
 - 为搜索好友节点添加了token验证（测试用）
 - 将全局字典改为hash表
 - 优化BillRoutes事务逻辑
 - token换成flask扩展版本
 - 把websocket启动文件名称改正式了一点
 - 将websocket通知写成函数形式（暂未实装）
 - 用户只能加入一个旅游（暂未实装）

2025.3.20
 1.1.4
 - 将需要的节点加上了token验证

2025.3.21
 1.1.5
 - 修复了websocket通知的bug
 - 修复了获取不到结束旅游的bug
 - 大幅调整了get_single_travel的逻辑，以适应退出旅游的功能
 - 修改了websocket保存现有连接的方式

2025.3.23
 1.1.6
 - 为UserBill添加isRead字段
 - 添加websocket接收客户端消息的节点，用于更新已读信息
 - 为Travel增加main_travel_id

2025.4.14
 1.2.0
 - 数据库换为mysql
 - 时间戳改为Long防止精度丢失
 - 增加了将空旅游自动清除的功能

2025.4.15
 1.2.1
 - 大幅调整自动更新逻辑：
    1. 为Travel增加了travel_timezone
    2. 在更新节点会根据travel_timezone判断是否需要更新
    3. travel_timezone的取值为1-24,12: UTC+0
    4. 创建旅游时需要格外的值travel_timezone

2025.4.16
 1.2.2
 - 为Travel添加timeZone返回值
 - 修复了添加好友失败的bug
 - 将打印的返回值的timestamp改为正常时间
 - 添加photoGraphRoutes及其3个节点
 - 增加Photo表
 - 增加了start.sh脚本，方便启动

2025.4.22
 1.2.3
 - 增加照片压缩功能，上传时自动压缩成三分（原图，预览，zip）
 - 增加格外两种照片的获取节点
 - 增加照片删除节点
 - Person结构调整，增加relationStatus值反映关系
 - 增加changeFriendNickname节点
 - 大幅调整账单部分逻辑，去除modifyBill，合并至uploadBill
 - 优化login和registe部分逻辑

2025.4.30
 2.0.0
 - 大幅更改结构
 - 大幅调整数据查询逻辑，减少数据库访问次数

 2.0.1
 - import 结构调整
 - 整理文件目录

 2.0.2
 - 修改了部分参数错误

2025.5.8
 2.0.3
 - 增加2个websocket接收节点
   1. 接收terminal信息
   2. 接受位置信息
 - 增加1个websocket发送节点
   1. 发送位置信息
 - 增加一个http节点
   1. 获取小旅游terminal
 - 调整了websocket处理接受信息的逻辑
 - 存储头像改为压缩
 - 存储旅游封面改为压缩
 - 旅游未上传封面且有照片时，改为显示照片墙第一张照片

2025.5.10
 2.0.4
 - 修复了进行旅游时还能添加的bug
 - 修复了用户修改密码参数错误的bug
 - 旅游未上传封面且有照片时，改为显示大旅游照片墙第一张照片
 - 修复了用户上传账单，代付有自己时，会给自己发通知的bug

2025.5.14
 2.1.0
 - 重构了日志输出，使用python的logging库
 - 将启动融合进linux的service中
 - 调整terminal存储格式和获取逻辑
 - 调整了存储photograph的逻辑，防止处理失败的照片仍被存入数据库
 - 修复了旅游结束后旅游申请还在的bug
 - 删除bill中的is_transfer

 TODO: SocketIO实时判断，返回好友在线状态--可测试

2025.5.17
 2.1.1
 - 重写了返回值逻辑，用一个类替换json，并添加debug供日志输出
 - 修复了travel一系列websocket返回值报错的问题
 - 添加上传里程信息功能
 - 同时给TravelEntity添加用户总里程

2025.5.18
 2.1.2
 - 将mainRoute暂时作为后台管理系统的节点
 - 修复了账单上传有参数问题的bug
 - 修改了照片压缩逻辑~~（暂未启用，待测试）~~
 TODO: ~~HTML结构优化，添加验证页面，~~增加websocket输出日志

2025.5.19
 2.1.3
 - 修复了原图不保存的bug
 - 调整了static位置
 - 增加README说明

2025.5.22
 2.1.4
 - 为后台管理系统添加了登录和token
 - 修复了修改用户名会覆盖昵称的bug
 - 修改位置共享逻辑，移动超过一定距离再发送位置信息(待测试)
 - 添加搜索旅游功能(还在加)
  1. 增加搜索节点
  2. 修改邀请好友加入旅游，email与token相同则视为主动添加
  3. 旅游申请处理添加email
- 修复了好友申请发起者能看到申请的bug

2025.5.24
 2.1.5
 - 修复了头像上传的各种问题
 - 修复了添加好友websocket的命名问题
 - 修复了处理好友申请的问题

2025.5.25
 2.1.5
 - 修复了在线状态更新失败的问题
 - 增加不能在多个设备上登录同一账号的功能

2025.7.6
 - 修改了照片存储逻辑，改为用column和photo的1对多关系表
 - 调整相关部分代码
 - 增加照片栏评论，及其修改功能
 - 修改照片栏获取的返回值

2025.7.8
 - 为bill上传增加timeStamp
 - 优化了一部分账单逻辑

2025.7.9
 - 给TravelEntity添加了budget
 - 添加了modifyBudget节点，同时修改了相关旅游逻辑
 - 添加了照片经纬度信息提取
 - 修复了上传照片导致的数据库的bug

2025.7.14
 - 修复了自动更新相关问题
 - 优化了一部分Travel数据库相关代码

2025.9.4
 - 修复了若干bug

2025.9.11
 - 添加了上传和获取Trace的节点
