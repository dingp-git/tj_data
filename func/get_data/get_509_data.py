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

def get_hive_db_increment():
    """
        获取hive_db增量
    """
    # 当前时间
    NOW_DATE_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 当前时间减去2小时
    HOUR_DATE_TIME = (datetime.datetime.now()+datetime.timedelta(minutes=-120)).strftime("%Y-%m-%d %H:%M:%S")
    db = pymysql.connect(host='10.213.70.120', port=3306, user='root', password='chanct603', 
                        database='TIANJIN', charset='utf8')
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
    ret = save_509_data.save_hive_db_increment(result)
    logger.debug(len(result))
    send_to_axxnr.send_message('get_hive_db_increment : {}'.format(ret))

def get_loading_rate_increment():
    """获取记载率数据增量"""
    NOW_DATE_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 当前时间减10分钟
    MIN_DATE_TIME = (datetime.datetime.now()+datetime.timedelta(minutes=-10)).strftime("%Y-%m-%d %H:%M:%S")
    db = pymysql.connect(host='10.213.70.120', port=3306, user='root', password='chanct603', 
                        database='TIANJIN', charset='utf8')
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
            d_time DESC;""".format(MIN_DATE_TIME,NOW_DATE_TIME)
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
    ret = save_509_data.save_loading_rate_increment(result)
    logger.debug(len(result))
    send_to_axxnr.send_message('get_loading_rate_increment : {}'.format(ret))