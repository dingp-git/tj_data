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
from func.save_data import save_509_data
from utils import send_to_axxnr



def get_loading_rate_data(host_name):
    """
        获取加载率数据
        @params:
            host_name :   主机名称(必填参数)    str
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name, port=22, username='root', password='chanct2018')
    cmd = "find /opt/recv/nfs/ -name 'loading_rate_*' | grep -v wrong|sort|awk 'END{print}'|xargs cat"
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    if result:
        result = json.loads(result)
        ret_list = []
        temp_time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result[0]['values'][0][0]))
        temp_time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result[1]['values'][0][0]))
        ret_list.append((result[0]['metric']['device'], result[0]['metric']['instance'], temp_time1,
                    result[0]['values'][0][1]))
        ret_list.append((result[1]['metric']['device'], result[1]['metric']['instance'], temp_time2,
                    result[1]['values'][0][1]))
        logger.debug(ret_list[0])
        logger.debug(len(ret_list))
        save_509_data.save_loading_rate_data(ret_list)

def del_loading_rate_data(host_name):
    """
        删除加载率数据
        @params:
            host_name :   主机名称(必填参数)    str
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name, port=22, username='root', password='chanct2018')
    cmd = "find /opt/recv/nfs/ -name 'loading_rate_*' | xargs rm -rf"
    stdin, stdout, stderr = client.exec_command(cmd)

def get_hive_db_data(host_name):
    """
        获取hive db数据
        @params:
            host_name :   主机名称(必填参数)    str
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name, port=22, username='root', password='chanct2018')
    cmd = "find /opt/recv/nfs/ -name '509hive_db_*' | grep -v wrong|sort|awk 'END{print}'|xargs cat"
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    if result:
        result = json.loads(result)
        data1 = [tuple(i) for i in result["table_storage"]]
        data2 = [tuple(i) for i in result["db_storage"]]
        ret_list = data1.extend(data2)
        logger.debug(len(ret_list))
        save_509_data.save_hive_db_data(ret_list)

def del_hive_db_data(host_name):
    """
        删除hive_db数据
        @params:
            host_name :   主机名称(必填参数)    str
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name, port=22, username='root', password='chanct2018')
    cmd = "find /opt/recv/nfs/ -name '509hive_db_*' | xargs rm -rf"
    stdin, stdout, stderr = client.exec_command(cmd)

def get_hive_db_increment():
    """
        获取hive_db增量
    """
    # 当前时间
    NOW_DATE_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 当前时间减去2小时
    HOUR_DATE_TIME = (datetime.datetime.now()+datetime.timedelta(minutes=-120)).strftime("%Y-%m-%d %H:%M:%S")
    db = pymysql.connect(host='10.238.249.33', port=3306, user='root', password='root',
                        database='tianjin', charset='utf8')
    # db = pymysql.connect(host='172.27.1.12', port=3306, user='root', password='root', database='tianjin',
    #                     charset='utf8mb4')
    cursor = db.cursor()
    sql = """
        SELECT
            db_id,
            data,
            d_time 
        FROM
            t_509_hive_db 
        WHERE
            d_time > "{}" AND d_time <= "{}"
        ORDER BY
            d_time DESC;""".format(HOUR_DATE_TIME,NOW_DATE_TIME)
    cursor.execute(sql)
    rows = cursor.fetchall()
    data_list = [list(row) for row in rows]
    increment = []
    new_list = copy.copy(data_list)
    for item in new_list:
        data_list.remove(item)
        for item2 in data_list:
            if item2[0] == item[0]:
                temp = []
                temp.append(item[0])
                detla = item[1]-item2[1]
                temp.append(detla)
                temp.append(item[2])
                new_list.remove(item2)
                increment.append(temp)
    result = [tuple(i) for i in increment]
    cursor.close()
    db.close()
    logger.debug(len(result))
    if result:
        save_509_data.save_hive_db_increment(result)


def get_loading_rate_increment():
    """获取记载率数据增量"""
    NOW_DATE_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 当前时间减10分钟
    MIN_DATE_TIME = (datetime.datetime.now()+datetime.timedelta(minutes=-10)).strftime("%Y-%m-%d %H:%M:%S")
    db = pymysql.connect(host='10.238.249.33', port=3306, user='root', password='root',
                        database='tianjin', charset='utf8mb4')
    # db = pymysql.connect(host='172.27.1.12', port=3306, user='root', password='root', database='tianjin',
    #                     charset='utf8mb4')
    cursor = db.cursor()
    sql = """
        SELECT
            device,
            ip_port,
            d_time,
            data 
        FROM
            t_509_loading_rate 
        WHERE
            d_time > '{}' 
            AND d_time <= '{}' 
        ORDER BY
            d_time DESC;""".format(MIN_DATE_TIME, NOW_DATE_TIME)
    cursor.execute(sql)
    rows = cursor.fetchall()
    data_list = [list(row) for row in rows]
    increment = []
    for i in range(int(len(data_list)/2)):
        temp = data_list[i]
        for j in data_list:
            if j[0] == data_list[i][0] and j[1] == data_list[i][1] and j[2] != data_list[i][2]:
                delta = data_list[i][3] - j[3]
                temp[3] = delta
        increment.append(temp)
    result = [tuple(k) for k in increment]
    cursor.close()
    db.close()
    logger.debug(len(result))
    if result:
        save_509_data.save_loading_rate_increment(result)


def get_row_flow():
    """获取原始流量"""
    """
    [{"obps": 429941888.0, "discards": 0.0, "iMpps": 0.0, "ibps": 0.0, "ip": "10.148.255.7", "iUpps": 0.0, "epps": 0.0, "state": 1, 
    "oMpps": 0.0, "timestamp": "2020-12-04 09:23:44", "speed": 10000, "port": "xgei-0/1/0/3", "oUpps": 253642.7, 
    "desc": "To:TJ-V-QDJC-SK-SEV2-TGE1"}, ]
    """
    # 查询接口
    url = "http://northstar.pub:8080/northstar/port/?net=v&ip=10.148.255.7"
    try:
        res = requests.get(url, timeout=30)
        if res.status_code == 200:
            d = res.json()
        else:
            print("=========== get api code err ===========")
            print(res)
            return

    except Exception as e:
        print("============ 请求接口异常 ============")
        traceback.print_exc()
    else:
        if not d:
            print("=========== api data is empty ===========")
            return
        insert_data = []  # 入库数据
        for data in d:
            desc = data.get("desc", "")
            if desc == "":  # 从中获取运营商信息
                continue
            if "-LT-" in desc:
                operators = "联通"
                #operators = "LT"
            elif "-YD-" in desc:
                operators = "移动"
                #operators = "YD"
            elif "-DX-" in desc:
                operators = "电信"
                #operators = "DX"
            else:
                print("========= desc ==========")
                print(desc)
                continue
            ip = data.get("ip", "")
            obps = data.get("obps", "")
            ibps = data.get("ibps", "")
            timestamp = data.get("timestamp", "")
            if timestamp == "":
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            port = data.get("port", "")

            insert_data.append((ip, obps, ibps, operators, desc, port, timestamp))

        # print(insert_data)
        # 入库
        save_509_data.save_row_flow(insert_data)
