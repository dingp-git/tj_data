# Standard library imports
import json
# Third party imports

# Local application imports


api_url = "http://10.213.76.89/api_jsonrpc.php"
header = {"Content-Type": "application/json"}
zabbix_key = "0dd8a003d067278153eaecf1a4f204f9"


# 获取单个组天津下监控的每台主机
data1 = json.dumps(
    {
        "jsonrpc": "2.0",                       # API使用的JSON-RPC协议的版本; Zabbix API实现的JSON-RPC版本是2.0;
            "method": "host.get",               # 被调用的API方法名;
            "params": {                         # 将被传递给API方法的参数;
                "output": ["hostid", "name"],   # 使用host.get方法检索所有已配置主机的id,主机名
                "groupids": "43",
            },
            "auth": zabbix_key,                 # 用户认证令牌; 
            "id": 1,                            # 请求的任意标识符;
    }
)