# Standard library imports
import json
import time
# Third party imports
import requests



def send_message(message):
    """
        发送信息到axxnr
        :param 
            message: 输出信息
    """
    data = {"chatname": "测试","msgtype": "text","msg" : time.strftime('%Y-%m-%d %H:%M:%S') + '\n' + message }
    r = requests.post('http://10.52.140.158:8080/axxnr/message',data = json.dumps(data))
    if 'send ok' in r.text :
        pass
    r.close()