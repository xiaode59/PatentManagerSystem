# TravelNote

#### 介绍
旅游助手软件后端
Python 3.10.12

主要库：
Flask                  3.1.0
Flask-JWT-Extended     4.7.1
Flask-SocketIO         5.5.1
Flask-SQLAlchemy       3.1.1


#### 后端架构
采用类似jave-springboot的结构。主要使用flask，SQLAlchemy，token和websocket。
##### 配置文件

  * **config.py** ：配置文件，主要配置数据库连接路径，开发 / 生产 / 默认环境修改。
  * **TravelNoteMain.py** ：启动入口，可以配置开放端口号。

##### app 文件夹

  * **__init__.py** ：初始化文件。
    * **Token 配置** ：使用 flask_jwt_extended ，在 app.config 修改。
    * **日志配置** ：使用 python 原生 logging ，在 setup_logging() 函数内修改。
    * **socketio** ：使用 flask_socketio ，用 SocketIO 集成 Flask 。
    * **create_app()** ：flask 初始化配置。
      * **@app.before_request** ：在每个 HTTP 请求处理之前执行，用于请求日志记录。需要在此处设置不用检查token的节点（如登录注册，网页资源获取等）和不输出日志的节点（如本地节点）
      * **@app.errorhandler(Exception)** ：捕获 Exception 及其子类的异常，便于数据异常时输出日志。
      * **@app.after_request** ：在每个 HTTP 请求处理之后执行，用于格式化返回值，同时可以通过 debug 选项和ResponseForm的debug值联合判断是否输出日志。
      * **注册路由** ：使用 flask 蓝图管理 HTTP 节点，添加新节点需在此处注册。

  * **HTML 文件夹**
    * **CSS 文件夹**
      * **login.css** ：登录页面样式表文件。
      * **styles.css** ：主页页面样式表文件。
    * **modules 文件夹**
      * **database.js**：数据库处理相关js代码
      * **logger.js**：日志获取相关js代码
      * **login.js**：登录处理相关js代码
      * **sidebar.js**：侧边栏相关js代码
    * **app.js**: 集中初始化index页面js。
    * **login.html**：登录页面文件。
    * **index.html** ：主页文件。
    
    * **favicon.ico** ：网站图标文件。

  * **appMode 文件夹**：SQLAlchemy的模型定义，可以将数据库的表作为对象操作。
    * **BillModel** ：对应bill表。
    * **PhotoModel** ：对应photo表，以用户id，旅游id为外键，为保障数据一致性，照片处理需在这里进行。
    * **TerminalModel** ：对应terminal表。
    * **TraceModel** ：对应trace表。
    * **TravelModel** ：对应travel表。
    * **UserModel** ：对应user表，由于获取申请列表的行为与用户挂钩，因此相关查询逻辑写在user表中。

    * **FriendModel** ：好友关系表，属于多对多关系，以两者id为外键，同时需要记录nickname和申请信息。用status表示用户间的状态，目前有申请中/好友两种状态，未找到关系即为陌生人。
    * **UserBillModel** ：用户-账单关系表，以两者id为外键，记录代付人和账单的关系，付款人由于是一对多关系直接存在BillModel中。
    * **UserTravelModel** ：用户-旅游关系表，以两者id为外键，记录用户和旅游的关系，用status表示与旅游的状态，目前有结束/进行中/主动申请/被邀请四种状态。
    * **__init__.py** ：添加新的库需在此处 import ，会按照顺序初始化。

  * **appRoutes 文件夹** ：基于 flask 的蓝图文件，负责收发请求，事务逻辑调用和图片保存。
      * **billRoutes.py** ：账单管理节点，包含账单的增删改查功能。其中增改在同一节点，通过传入id判断调用不同的ServiceImpl。
      * **friendRoutes.py** ：朋友关系处理节点，包括好友搜索，添加，删除，更改昵称，获取好友列表/申请列表，以及申请相关处理。
      * **imgGetRoutes.py** ：图片获取节点，仅处理获取头像和旅游封面的请求。
      * **infoModifyRoutes.py** ：个人信息编辑节点，处理修改头像，签名，用户名。还有比较特殊的修改密码，逻辑类似注册节点。
      * **localRoutes.py** ：本地处理节点，仅处理本地发出的请求，目前用于更新旅游，防止flask框架的上下文问题。
      * **loginRoutes.py** ：登录节点，仅负责登录，会返回大量数据。
      * **mainRoutes.py** ：后台管理系统节点，用于处理后台管理系统的请求（网页）。
      * **photoGraphRoutes.py** ：照片节点，处理上传的照片和发送对应的照片，需要在节点处就保存，节省服务器资源。
      * **registerRoutes.py** ：注册节点，包括上传注册信息和验证两个节点，接受到注册信息后会发送邮箱验证码。
      * **TerminalRoutes.py** ：设备信息节点，存储前端api的映射信息，加快访问速度。
      * **TraceRoutes.py** ：轨迹记录节点，记录和获取轨迹信息。
      * **travelRoutes.py** ：旅游节点，包含旅游列表和单个旅游信息的获取，主动加入申请和被动邀请申请的获取，申请的处理，以及新建，搜索，退出，结束旅游处理节点。
  * **appService 文件夹**：服务层代码，事务逻辑实现，作为 Route 和 Dao 之间的中间层，负责接受Route的信息，清理数据后调用 Dao 中的逻辑，并返回Route需要的信息。
    * **BillService.py** ：账单处理接口。
    * **FriendService.py** ：好友处理接口。
    * **LocationShareService.py** ：位置共享接口。
    * **StaticResourceService.py** ：静态资源接口。
    * **TerminalService.py** ：设备信息接口。
    * **TraceService.py** ：轨迹信息接口。
    * **TravelService.py** ：旅游处理接口。
    * **UserService.py** ：用户服务接口。
    * **ServiceImpl 文件夹**：实现接口文件定义的方法。
      * **BillServiceImpl.py** ：与账单节点对应，处理账单相关逻辑。
      * **FriendServiceImpl.py** ：与好友节点对应，处理好友相关逻辑。
      * **LocationShareServiceImpl.py** ：websocket服务层实现，包含位置信息存储和共享，由于更新频繁不存入数据库。
      * **StaticResourceServiceImpl.py** ：静态资源服务，是所有和图片有关的节点的共用服务层。
      * **TerminalServiceImpl.py** ：与设备信息节点对应，处理设备信息相关逻辑。
      * **TraceServiceImpl.py** ：与轨迹记录节点对应，处理轨迹记录相关逻辑。
      * **TravelServiceImpl.py** ：旅游处理相关服务，处理旅游节点中除列表获取外的服务。
      * **UserServiceImpl.py** ：用户相关服务，是个人信息编辑节点，登录节点，注册节点多个节点的共用服务层。由于列表获取与用户相关性强，还包含了所有列表获取的服务。

    * **ServiceDTO** ：事务逻辑与 Route 之间传输用参数类，当节点需要返回一个字典时，需要用一个DTO承载节点和服务之间的数据传输。需要一个个体类和一个列表类，并都要有json()方法用于返回字典。
      * **FriendApplicationDTO.py** ：获取好友申请列表节点的数据，需要申请信息和申请人信息。
      * **LocationShareDTO.py** ：位置信息共享的数据，用于websocket服务，需要返回用户，经纬度，以及一个不显示的时间戳用于判断有效性。
      * **LoginDTO.py** ：登录节点的数据，需要大量信息。
      * **TerminalInTravelDTO.py** ：获取旅游设备节点的数据，需要email和设备id的对应信息。
      * **TravelListDTO.py** ：大旅游信息，main_travel_id相同的所有旅游组成的列表。
      * **TravelPhotoDTO.py** ：获取旅游照片列表节点的数据，需要照片id，时间戳，上传者的信息。

  * **entity 文件夹** ：常用实体类。需要定义一个类和该类的获取函数。
    * **BillEntity.py** ：账单实体类，包含BillModel大部分信息，以及需要用PersonEntity表示的付款人和代付人列表。
    * **PersonEntity.py** ：最基本的实体，表达的是用户和获取对象的相对关系，主要体现在nickname和relationStatus两个值上。所以获取需要两个参数，BillEntity和TravelEntity因为包含PersonEntity也都需要两个参数。
    * **TravelEntity.py** ：旅游实体类，包含TravelModel大部分信息，以及用PersonEntity表示的参与人和用BillEntity表示的账单列表。
  * **utils 文件夹** ：工具类，包括验证码处理，本地 Route 访问，HTTP 响应传输用类，照片处理。
    * **PhotoProcessTools.py**：照片处理工具，包含两种压缩函数，两个预处理函数和失败后的处理函数，zip压缩通过等比缩放能大幅减小照片大小，preview压缩通过循环逐步减少图片质量压缩，能在尽量维持原图状态的情况下压缩到1Mb以内。两个预处理函数主要是为了限制格式和对不同格式的差异处理。照片处理使用PIL库实现，PIL库是python原生库，在对比多种库的压缩质量，压缩种类，是否付费等要素后选择该库实现功能。
    * **ResponseForm.py**：Route返回值统一格式，便于统一管理，默认debug值为false，在需要debug的节点设置为true，即可看到返回值内容。同时包含三个函数用于在不同地方json化。
    * **routeTools.py**：节点工具，包含给本地节点发送请求的函数，和一些信息处理函数。
    * **VerifyTools.py**：验证码生成和发送工具。
  * **webSocket 文件夹**
    * **connectController.py** ：websocket 连接控制（连接，断开）。
    * **ReciveMessage.py** ：接收 websocket 信息（接受客户端消息并调用ServiceImpl 处理）。
    * **websocketTools.py** ：websocket 工具（向客户端发送消息），is_online 函数（是否在线）。

##### 日志文件

  * **TravelNoteMain.err.log** ：错误日志会输出到这里。
  * **TravelNoteMain.log** ：INFO 信息会输出到这里。

##### document 文件夹

  * **CommunicationDocument.md** ：前后端通信协议。
  * **updateLog.md** ：更新日志。

##### static 文件夹

  * 静态文件（图片/旅游封面/头像）存放于此。

#### 使用说明
1. 运行TravelNoteMain.py即可，注意配置端口号
2. Linux系统可以配置/etc/systemd/system/travelnote.service文件作为服务启动

#### debug流程
主要依靠python内置库logger的信息
1. 检查TravelNoteMain.log中是否有访问节点的信息
2. 检查访问值是否符合协议
3. 查看TravelNoteMain.err.log中有无报错信息
4. 如果是逻辑问题，在对应节点添加responseForm.debug = True，使TravelNoteMain.log输出返回值
5. 按照route - serviceImpl - model的层级排查
