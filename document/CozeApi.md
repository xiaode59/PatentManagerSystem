<h1>Coze接口</h1>

<h2>主要接口</h2>

|NodeName|UrlSuffix|Method|Params|
|:---:|:---:|:---:|:---:|
用户推导完毕后的位置信息|uploadTravelScheme|POST|email, [latlng, addressname, note, flag]|
单个坐标值的转发与存储|uploadSingleSightseeingPoint|POST|email,latlng, addressname, note, flag|

<h2>websocket</h2>
<h3>服务端->客户端</h3>

uploadSingleSightseeingPoint
```json
{
    "lat" : Float,
    "lng":Float,
    "addressname": string, 
    "note": string, 
    "flag": int
}
```

uploadTravelScheme
```json
[
    {
        "lat" : Float,
        "lng":Float,
        "addressname": string, 
        "note": string, 
        "flag": int
    }
]
```

