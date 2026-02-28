	


<h1>TravelNote通讯协议v4.0</h1>

<h2>基础返回值</h2>

```json
BasicValue = {
  "flag": Boolean,
  "timeStamp":Int,
  "extra" : 额外附加信息
}
```
其中extra根据具体的请求改变

```json
Person = {
  "nickname" : String,
  "username" : String,
  "email" : String,
  "signature" : String,
  "onlineStatus" : Int[0: 不在线, 1: 在线],
  "relationStatus": Int[-1: self, 0: stranger, 1: inviting, 2: friend]
}
```

```json
Bill = {
  "billId" : Int,
  "payer" : Person , 
  "amount" : Double , 
  "reason" : String ,
  "realTime" : Long,
  "payfors" : List[Person], 
  "isTransfer" : Boolean,
  "merchant": String,
  "paymethod": String,
  "isRead": Boolean
}
```

```json
Travel = {
  "travelName":String,
  "mainTravelId": Int,
  "travelDestination" : String,
  "travelId" : Int,
  "travelStartTimeStamp" : Long,
  "promoterEmail" : String,
  "bills" : List[Bill] ,
  "participants" : List[Person],
  "status" : Int[0: 结束, 1: 申请中, 2: 进行中], 
  "timeZone": Int,
  "budget": Double
}
```

```json
Route = {
  "routeID": Long,
  "routeName": String,
  "routeDesc": String,
  "routeCreator": Person,
  "createTime": Int (时间戳),
  "routePlaces": List[Place],
  "routeImg": String,
  "belongingTravel": Long,
  "markdownContent": String,
  "isAdopted": Boolean,
  "adoptedBy": Int
}
```

```json
Place = {
  "lat": Double,
  "lng": Double,
  "placeDesc" : String,
  "placeName" : String,
  "placeChara" : Int[0: 娱乐, 1: 餐饮, 2: 酒店, 3: 交通, 4: 景区]
}
```

***

<h2>主要协议表格</h2>

登录协议
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
[登录](#login)|login|GET|username,password|
注册|register|POST|username,password,email|
注册验证|registerVerify|POST|verifyCode|
忘记密码-接收邮箱|lostPassword_getEmail|GET|email|
忘记密码-验证并重置密码|lostPassword_resetPassword|GET|verifyCode,newPassword|

媒体文件与更新节点
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
头像图片获取|getAvatar|GET|token, email|
旅行封面图片获取|getCoverage|GET|travelId, token|
应用更新包|upgradePackage|GET|NULL|

邮箱模块
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
[获取好友申请列表](#getFriendsApplication)|getFriendsApplication|GET|token|
[获取旅游申请列表](#getTravelsApplication)|getTravelsApplication|GET|token|
好友申请处理|processFriendApplication|POST|targetEmail , permitted ,token|
旅游申请处理|processTravelApplication|POST|targetTravel, permitted ,token, targetEmail
[获取主动加入旅游申请列表](#getTravelApplicants)|getTravelApplicants|GET|token|

好友模块
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
删除好友节点|deleteFriend|POST|deletedEmail , token
[搜索好友节点](#getNewFriends)|getNewFriends|GET|token,string|
申请好友节点|applyNewFriend|POST|token,targetEmail,message|
更改好友昵称|changeFriendNickname|POST|token,targetEmail,nickname|

路书模块
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
[获取用户所有路书](#getAllRoute)|getAllRoute|GET|token|
[采纳路书](#adoptRoute)|adoptRoute|POST|token, routeID|
[获取历史对话记录](#getHistoryConversation)|getHistoryConversation|GET|token|

个人主页b
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
修改用户名|modifyUsername|POST|token , newUsername
修改签名|modifySignature|POST|token , newSignature
修改头像|modifyAvatar|POST|file,token

主题旅游
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
[开始旅游](#startTravel)|startTravel|POST|token , travelName , travelDestination, travelTimezone
结束旅游|endTravel|POST|token , travelId
邀请好友加入旅游|applyNewTravelParticipants|POST|travelId, targetEmail , token
退出旅游|exitTravel|POST|token , travelId
[搜索旅游](#searchTravel)|searchTravel|GET|token , string
修改预算|modifyBudget|POST|token, travelId, budget


旅游相关——记账本
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
[账单上传](#uploadBill)|uploadBill|POST|token , billId(id>0: change, id<0: new), travelId , reason , amount, payfors : [email1,email2,...] , isTransfer, payMethod, merchant, timeStamp
~~账单修改|modifyBill|POST|billId , newAmount , newReason , newPayfors, token~~
账单删除|deleteBill|POST|billId, token

旅游相关——照片
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
[旅行图片上传](#uploadPhotoGraph)|uploadPhotoGraph|POST|token , travelId , timestamp , photograph
旅行图片删除-一栏|deletePhotoColumn|POST|token , travelId, timestamp
[旅行图片获取](#getTravelPhotoGraph)|getTravelPhotoGraph|GET|token , travelId
修改照片栏评论|modifyColumnComment|POST|token, travelId, timestamp, newComment
单个照片获取|getSignalPhotoGraph|GET|token , photoGraphId
单个照片获取-压缩|getSignalPhotoGraphZip|GET|token , photoGraphId
单个照片获取-预览|getSignalPhotoGraphPreview|GET|token , photoGraphId

路径相关
|NodeName|UrlSuffix|Method|Params
|:---:|:---:|:---:|:---:|
上传/更新trace|uploadTrace|POST|token, tracelId, stepCounts
[获取trace](#getTrace)|getTrace|GET|token , emailList, traceIdList

单独数据结构获取
|NodeName|UrlSuffix|Method|Params
|:---:|:---:|:---:|:---:|
[旅行](#getTravel)|getTravelByTravelId|GET|travelId , token
[账单](#getBill)|getBillByBillId|GET|billId , token
[旅行列表](#getTravelList)|getTravelList|GET|token
[好友列表](#refreshFriendList)|refreshFriendList|GET|token

自动更新项
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
[更新检查](#checkUpdate)|checkUpdate|GET|

terminal信息
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
[获取小旅游所有terminalId](#getTerminalIdInTravel)|getTerminalIdInTravel|GET|token, travelId

<!-- 里程信息
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
上传里程信息|uploadTrace|POST|token, travelId, startTime, endTime, distance -->

coze
|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
[获取token](#requestCozeToken)|requestCozeToken|GET|token

***

<h2>SocketIO</h2>
客户端->服务端
基本格式:
{
  "task" : String,
  "extra" : 额外附加信息
}

账单已读通知
```json
'bill' -> [billId]
```

上传terminal信息
```json
'updateTerminal' -> {"mainTravelId": Long, "terminalId": Long, "email": str}
```

上传位置信息
```json
'updateLocation' -> {"longitude": double, "latitude": double}
```

与AI对话
```json
'talkToAI' -> String (用户消息)
```

生成路书
```json
'generateRoute' -> String (用户消息)
```


服务端->客户端

账单添加通知
```json
billAdded -> Bill
```

好友申请添加通知
```json
friendAdded ->   
  {
    "person" : Person,
    "message" : String
  }
```

好友同意添加通知
```json
addFriend ->   
  Person
```

好友删除通知
```json
deleteFriend ->   
  Person
```

好友状态更新
```json
updateFriendStatus -> 
  Person
```

旅游添加通知
```json
travelAdded -> Travel
```

某人突然退出旅游通知
```json
exitTravel -> Travel
```

旅游结束通知
```json
endTravel -> Travel
```

某人突然加入旅行通知
```json
someoneJoinedTravel -> Travel
```

广播位置信息
```json
broadcastLocation -> 
[
  {
    "email" : str, 
    "longitude" : Double, 
    "latitude" ：Double
  }
]
```

更新好友在线状态
```json
updateOnlineStatus -> 
{
  "email" : str, 
  "status" ：int
}
```

AI对话响应
```json
talkToAI -> 
{
 "message" : str
}


```

路书生成响应
```json
routeGenerate -> Route
```

错误响应
```json
error -> 
{
  "status": "error",
  "message": String
}
```

***

<h2>返回值</h2>
<span id="getTrace">获取trace</span>
```json
[
  {
    email: String,
    traceInformation: [
      {
        traceId: Long,
        stepCounts: Long
      }
    ]
  }
]
```

<span id="getTravelApplicants">获取主动加入旅游申请列表</span>
```json
[
  Person
]
```

<span id="searchTravel">搜索旅游节点返回值</span>
```json
[
  Travel
]
```

<span id="getTerminalIdInTravel">获取小旅游所有terminalId</span>
```json
  [
    {
      "email" : email , 
      "terminalId" : Long
    }
  ]
```


<span id="uploadPhotoGraph">上传账单</span>
```json
  Long
```

<span id="getTravelPhotoGraph">照片获取</span>
```json
  [
    {
      "travelId" : Long,
      "comment" : String (default = "")
      "timeStamp" : Long,
      "photoGraph" : [{
        "photoId" : Long,
        "lat" : Double,
        "lng" : Double
      },...],
      "person": Person
    }
  ]
```

<span id="getBill">账单获取</span>
```json
  Bill
```


<span id="getTravel">单次旅行详细信息获取</span>
```json
  Travel
```

<span id="getTravelList">获取旅游列表</span>
```json
[
  {
    "length" : Int,
    "travels" : List[Travel]
  }
]
```

<span id="startTravel">发起旅游节点(TravelId)</span>:
```json
  Travel
```

<span id="refreshFriendList">刷新好友列表</span>
```json
  List[ Person ]
```

<span id="checkUpdate">检查更新节点</span>
```json
{
  "versionCode" : Int,
  "Description" : String,
  "Size" : String
}
```

<span id="getNewFriends">搜索好友节点返回值</span>
```json
[
  Person
]
```

<span id="getFriendsApplication">邮箱-获取好友申请列表返回值</span>
```json
[
  {
    "person" : Person,
    "message" : String
  }
]
```

<span id="uploadBill">账单上传返回值</span>
```json
  Int
```

<span id="getTravelsApplication">邮箱-获取旅游申请列表返回值</span>
```json
  List[Travel]
```

<span id="login">登录</span>
```json
{
  "username":String,
  "signature":String,
  "email":String,
  "newMessage" : Boolean,
  "travels":[
    {
      "length" : Int,
      "travels" : List[Travel]
    }
  ],
  "friends": List[ Person ]
}
```

<span id="requestCozeToken">获取Coze token</span>
```json
  string
```

<span id="getAllRoute">获取用户所有路书</span>
```json
[
  Route
]
```

<span id="adoptRoute">采纳路书</span>
```json
{
  "flag": Boolean,
  "message": String
}
```

<span id="getHistoryConversation">获取历史对话记录</span>
```json
[
  {
    "conversationId": Long,
    "userId": Int,
    "sender": String ("user" | "ai"),
    "message": String,
    "timestamp": Int
  }
]
```
