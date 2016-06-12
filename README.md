# 873_Pi
Group 873's project in Embedded System Course of ZJU

### 1. 协议说明
树莓派使用HTTP协议，定时向两个服务器发送实时浴室人数信息。
具体如下：
### POST /api/report

树莓派汇报数据用的接口

Body 格式

```javascript
{
  "auth_id": 23,                        // Integer，发送这个数据包的设备（网关或直连网络的传感器）在网页上获得的设备码
  "auth_key": "f94d3aa2dcf5b8ee2db0a0d4bdf2a200",     // String，发送这个数据包的设备（网关或直连网络的传感器）在网页上获得的密钥
  "device_id": 23,                      // Integer，数据源的设备码，本次数据会显示在这个设备的网页上
  "payload": {                         // 要传输的数据
    "number": 4,               // 人数4人，将会显示在23号设备的网页中
    "time": 1465718478.127675  // Unix时间戳，将会显示在23号设备的网页中
  }
}
```

### GET /api/data?device_id=2&limit=10

APP获取传感器提交过的所有数据历史的接口

`device_id` 即这个设备的序列号，`limit` 指需要获得最新的多少条数据。默认为 200 条，有点多哦。

返回的数据格式

```javascript
{
  "code": 0, // 请求成功
  "data": [
    { "id": 23, "number": 4, "time": 1465718478.127675, "created_at": "2016-06-12 13:28:12" } // 直接返回了数据库中的内容
  ]
}
```

### 2. 使用说明
直接放在浴室门口开机即可。树莓派会自动运行登录ZJUWLAN的脚本以及检测实时人数的脚本。
