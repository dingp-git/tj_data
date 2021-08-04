# Standard library imports
import datetime
import time
import json
import copy
# Third party imports
import traceback

import requests
from loguru import logger
import pymysql
# import requests
import paramiko
# Local application imports
from func.save_data import save_ipsy_data
from utils import send_to_axxnr

def get_log_data(host_name):
    """
        获取日志量数据
        @params:
            host_name :   主机名称(必填参数)    str
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host_name=host_name, port=22, username='root', password='TJcert2020!@')
    cmd = "find /opt/rzx_ipsy_data -name 'tj_2021*' | grep -v wrong|sort|awk 'END{print}'|xargs cat"
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    if result:
        result = json.loads(result)
        ret_list = [tuple(i) for i in result]
        logger.debug(len(ret_list))
        logger.debug(ret_list)
        save_ipsy_data.save_log_data(ret_list)

def del_log_data(host_name):
    """
        删除日志量数据
        @params:
            host_name :   主机名称(必填参数)    str
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name, port=22, username='root', password='TJcert2020!@')
    cmd = "find /opt/recv/nfs/ -name 'tj_2021*' | xargs rm -rf"
    stdin, stdout, stderr = client.exec_command(cmd)

def get_log_increment():
    """获取日志量增量"""
    NOW_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
    BEFORE_DATE = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    db = pymysql.connect(host='10.238.249.33', port=3306, user='root', password='root',
                        database='tianjin', charset='utf8mb4')
    # db = pymysql.connect(host='172.27.1.12', port=3306, user='root', password='root', database='tianjin',
    #                     charset='utf8mb4')
    cursor = db.cursor()
    sql = """SELECT
                province,
                lt_yw,
                yd_yw,
                dx_yw,
                lt_gw,
                yd_gw,
                dx_gw,
                d_time 
            FROM
                t_ipsy_log_nums 
            WHERE
                d_time BETWEEN '{}' 
                AND '{}' 
            ORDER BY
                d_time DESC""".format(BEFORE_DATE, NOW_DATE)
    cursor.execute(sql)
    rows = cursor.fetchall()
    data_list = [list(row) for row in rows]
    increment = []
    for i in range(len(data_list) - 1):
        x = data_list[i]
        y = data_list[i+1]
        k = []
        k.append(x[0])
        for j in range(1, len(x)-1):
            k1 = int(x[j]) - int(y[j])
            k.append(k1)
        k.append(x[7])
        increment.append(k)
    result = [tuple(item) for item in increment]
    cursor.close()
    db.close()
    logger.debug(len(result))
    if result:
        save_ipsy_data.save_log_increment(result)

def get_system_info():