# Standard library imports
import datetime
import time
import json
import copy
from pathlib import Path
# Third party imports
import traceback
import requests
from loguru import logger
import pymysql
import paramiko
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import subprocess
import cx_Oracle as cx
# Local application imports
from func.save_data import save_ipsy_data
from utils import send_to_axxnr
from conf.ipsy_config import ip_list, get_ip_cmd,get_now_date_time

app = FastAPI()

# 库表  数据(接收信工所传入数据)
class proxy_ip_data(BaseModel):
    proxy_ip_addr: List[str]
    storage_ip_addr: List[str]
    proxy_total: List[int]
    storage_total: List[int]
    d_time: List[datetime.datetime]

class database_produce_data(BaseModel):
    db_name: List[str]
    ip_addr: List[str]
    data_num: List[int]
    d_time: List[datetime.datetime]

@app.post('/tj_data/ipsy/proxy_ip_data')
async def get_proxy_ip_data(request_data: proxy_ip_data):
    """ 
        接收 代理服务器数据是否正常入库 数据
         ## **param**:
            proxy_ip_addr:      代理服务器IP(必传参数)                List[str]
            storage_ip_addr:    存储服务器IP(必传参数)                List[str]
            proxy_total:        代理服务器入库数据量(必传参数)         List[int]
            storage_total:      存储服务器入库数据量(必传参数)         List[int]
            d_time:             采集时间（每30min采集一次）(必传参数)  List[datetime]
        ## **return**: 数据处理结果
            [
                (
                    "1.1.1.1",
                    "1.1.1.1",
                    12523,
                    4511,
                    "2021-07-30T02:07:23.867000+00:00"
                ),
                ...
            ]
    """
    ret_list = [] 
    for item in request_data:
        ret_list.append(item[1])
    result = []
    for i in range(len(ret_list[0])):
        temp_list = [x[i] for x in ret_list]
        result.append(temp_list)
    if result:
        result = [tuple(j) for j in result]
        logger.debug(result)
        save_ipsy_data.save_proxy_ip_data(result)

@app.post('/tj_data/ipsy/database_produce_data')
async def get_database_produce_data(request_data: database_produce_data):
    """
        接收 当天库表产生情况 数据
         ## **param**:
            db_name:      数据库/表名称(必传参数)               List[str]
            ip_addr:      服务器ip(必传参数)                   List[str]
            data_num:     数据库/表数据增量(必传参数)           List[str]
            d_time:       采集时间（每30min采集一次）(必传参数)  List[datetime]
        ## **return**: 数据处理结果
            [
                (
                    "dbms",
                    "1.1.1.1",
                    "12523",
                    "2021-07-30T02:07:23.867000+00:00"
                ),
                ...
            ]
    """
    ret_list = []
    for item in request_data:
        ret_list.append(item[1])
    result = []
    for i in range(len(ret_list[0])):
        temp_list = [x[i] for x in ret_list]
        result.append(temp_list)
    if result:
        result = [tuple(j) for j in result]
        logger.debug(result)
        save_ipsy_data.save_database_produce_data(result)

# 日志数据 (读取本机日志文件)
def read_file(file_dir):
    """
        通过读取文件获取 日志量数据
        @params:
            file_dir :   文件路径(必填参数)    str
    """
    if Path(file_dir + '.ok').is_file():
        with open(Path(file_dir), 'r', encoding='utf-8') as f:
            ret = f.read()
            temp_list = ret.split(',')[0:-1]
            result = [tuple([int(item) for item in temp_list])]
            logger.debug(ret_list)
            save_ipsy_data.save_log_data(ret_list)
    else:
        return 1

def get_log_data(file_path):
    """
        获取日志量数据
        @params:
            file_path :   文件路径(必填参数)    str
    """
    flag = True
    f_date = datetime.date.today().strftime("%Y%m%d")
    f_file = file_path + 'tj_' + f_date + '.log'
    while flag:
        ret = read_file(f_file)
        if ret == 1:
            time.sleep(3600)
            ret = read_file(f_file)
        else:
            flag = False

def str_to_date(str_date):
    """
        将 字符串 装换成 日期
        @params: '2021-01-01'
        @return: 2021-01-01
    """
    year, month, day = [int(i) for i in str_date.split('-')]
    d_date = datetime.date(year, month, day)
    return d_date

def get_history_log_data(start_date, end_date, file_path):
    """
        获取日志量历史数据
        @params:
            start_date:      开始日期(必填参数)   str     '2021-01-01'
            end_date:        结束日期(必填参数)   str     '2021-03-01'
            file_path:       文件路径(必填参数)   str     '/opt/rzx_ipsy_data'
    """
    ret_list = []
    start_date = str_to_date(start_date)
    end_date = str_to_date(end_date)
    for i in range((end_date-start_date).days + 1):
        day = start_date + datetime.timedelta(days=i)
        f_day = day.strftime("%Y%m%d")
        f_file = file_path + 'tj' + f_day + '.log'
        read_file(f_file)

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


# TODO 工信通 zabbix-get
def write_file(str2):
    """
        将字符串写入文件
        @param:       str2   类型   str
    """
    with open('zabbix_data.txt', 'r', encoding='utf-8') as f:
        f.write(str2)

def run_cmd(command):
    """
        将zabbix_get执行命令后的结果写入文件
        @param: command  zabbix_get执行命令   类型  list
    """
    for cmd in command:
        ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding='utf-8',timeout=30)
        if ret.returncode == 0:
            if ret.stdout is None:
                write_file('-')
            elif ret.stdout == '':
                write_file('0')
            else:
                write_file(ret.stdout.strip() + ',')

def get_disk_usage():
    """
        获取 磁盘使用情况
        ## **return**：数据处理结果
    """
    d_time = get_now_date_time()
    for ip in ip_list:
        write_file(ip + ',')
        cmd_list = get_ip_cmd(ip)
        run_cmd(cmd_list)
        write_file(str(d_time))
        write_file('\n')
    get_disk_data()

def get_disk_data():
    with open('zabbix_data.txt', 'r', encoding='utf-8') as f:
        rows = f.readlines()
        ret_data = [row.strip() for row in rows]
        result = []
        for i in ret_data:
            temp_list = i.split(',')
            result.append(tuple(temp_list))
        if result:
            save_ipsy_data.save_disk_usage(result)


# TODO 拨测数据 oracle
def get_bc_data():
    conn = cx.connect('tjca', 'tjca123456', '10.238.183.2/jk1')
    cursor = conn.cursor()
    ret = cursor.execute('select * from tryfzx.tjca limit 100')
    data = ret.fetchall()
    with open('oracle_data.txt', 'a',encoding='utf-8') as f:
        f.write(data)
    cursor.close()
    conn.close()
    # if data:
    #     save_ipsy_data.save_bc_data(data)

