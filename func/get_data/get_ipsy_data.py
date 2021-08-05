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
# Local application imports
from func.save_data import save_ipsy_data
from utils import send_to_axxnr

app = FastAPI()

class log_nums_item(BaseModel):
    proxy_ip_addr: List[str]
    storage_ip_addr: List[str]
    proxy_total: List[int]
    storage_total: List[int]
    d_time: List[datetime.datetime]

class log_increment_item(BaseModel):
    db_name: List[str]
    ip_addr: List[str]
    data_num: List[str]
    d_time: List[datetime.datetime]

@app.post('/tj_data/ipsy/log_nums')
async def get_log_nums(request_data: log_nums_item):
    """ 
        接收 每家运营商上报日志条数（包括固网、移动网）数据
         ## **param**:
            proxy_ip_addr:      代理服务器IP(必传参数)                List[str]
            storage_ip_addr:    存储服务器IP(必传参数)                List[str]
            proxy_total:        代理服务器入库数据量(必传参数)         List[int]
            storage_total:      存储服务器入库数据量(必传参数)         List[int]
            d_time:             采集时间（每30min采集一次）(必传参数)  List[datetime]
        ## **return**:
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
        save_ipsy_data.save_get_log_data(result)

@app.post('/tj_data/ipsy/log_increment')
async def get_log_increment(request_data: log_increment_item):
    """
        接收 每家运营商上报日志条数的增量（包括固网、移动网） 数据
         ## **param**:
            db_name:      数据库/表名称(必传参数)               List[str]
            ip_addr:      服务器ip(必传参数)                   List[str]
            data_num:     数据库/表数据增量(必传参数)           List[str]
            d_time:       采集时间（每30min采集一次）(必传参数)  List[datetime]
        ## **return**:
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
        save_ipsy_data.save_get_log_increment(result)

def read_file(file_dir):
    """
        通过读取文件获取 日志量数据
        @params:
            file_dir :   文件路径(必填参数)    str
    """
    ret_list = []
    if Path(file_dir + '.ok').is_file():
        with open(Path(file_dir), 'r', encoding='utf-8') as f:
            ret = f.read()
            temp_list = ret.split(',')[0:-1]
            result = tuple([int(item) for item in temp_list])
            ret_list.append(result)
    else:
        return 1
    if ret_list:
        logger.debug(ret_list)
        save_ipsy_data.save_log_data(ret_list)

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

# def get_system_info():