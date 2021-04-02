# Standard library imports
import datetime, time
import json
# Third party imports
from loguru import logger
import pymysql
# import requests
import paramiko
# Local application imports
from func.save_data import save_509_data
from utils import send_to_axxnr



# 需要传递参数 host_name=('10.41.18.69')
def get_loading_rate_data(host_name):
    """
        获取加载率数据
        @params:
            hostname :   主机名称(必填参数)    str
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username='root', password='chanct2018')
    cmd = "find /opt/recv/nfs/ -name 'loading_rate_*' | grep -v wrong|sort|awk 'END{print}'|xargs cat"
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    result = json.loads(result)
    ret_list = []
    temp_time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result[0]['values'][0][0]))
    temp_time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result[1]['values'][0][0]))
    ret_list.append((result[0]['metric']['device'], result[0]['metric']['instance'], temp_time1,
                result[0]['values'][0][1]))
    ret_list.append((result[1]['metric']['device'], result[1]['metric']['instance'], temp_time2,
                result[1]['values'][0][1]))
    ret = save_509_data.save_loading_rate_data(ret_list)
    logger.debug(ret)
    send_to_axxnr.send_message('get_loading_rate_data : {}'.format(ret))

# 需要传递参数 host_name=('10.41.18.69')
def del_loading_rate_data(host_name):
    """
        删除加载率数据
        @params:
            hostname :   主机名称(必填参数)    str
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username='root', password='chanct2018')
    cmd = "find /opt/recv/nfs/ -name 'loading_rate_*' | xargs rm -rf"
    stdin, stdout, stderr = client.exec_command(cmd)

# 需要传递参数 host_name=('10.41.18.69')
def get_hive_db_data(host_name):
    """
        获取hive db数据
        @params:
            hostname :   主机名称(必填参数)    str
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username='root', password='chanct2018')
    cmd = "find /opt/recv/nfs/ -name '509hive_db_*' | grep -v wrong|sort|awk 'END{print}'|xargs cat"
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    result = json.loads(result)
    data1 = [tuple(i) for i in result["table_storage"]]
    data2 = [tuple(i) for i in result["db_storage"]]
    ret_list = data1.extend(data2)
    ret = save_509_data.get_hive_db_data(ret_list)
    logger.debug(ret)
    send_to_axxnr.send_message('get_hive_db_data : {}'.format(ret))

# 需要传递参数 host_name=('10.41.18.69')
def del_hive_db_data(host_name):
    """
        删除hive_db数据
        @params:
            hostname :   主机名称(必填参数)    str
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username='root', password='chanct2018')
    cmd = "find /opt/recv/nfs/ -name '509hive_db_*' | xargs rm -rf"
    stdin, stdout, stderr = client.exec_command(cmd)
