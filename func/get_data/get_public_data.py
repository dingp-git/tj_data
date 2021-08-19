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
from func.save_data import save_public_data
from utils.mysql_conn_pool.mysql_helper import MySqLHelper
from utils import send_to_axxnr

def get_topo_data(ip_list):
    """
        根据 get_topo_ip或get_topo_ip_list返回的ip_list, 访问jczy，获取各ip基础信息
        [(ip,d_time),(ip,d_time)]
    """
    ret_list = ['ip', 'config', 'crcity', 'crlacpoint', 'crprovince_name', 'dfcoding', 
                'dmodel_name', 'dname', 'dstatus_name', 'maindept_name', 'mperson_name', 'rname']
    d_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result = []
    for ip in ip_list:
        url = 'http://jczy.aiops.pub:8083/jczy/device' + "?ip={}".format(ip[0])
        res = requests.get(url)
        ret = json.loads(res.content)
        temp_dict = {}
        if ip[1] == '0000-00-00 00:00:00':
            temp_dict['d_time'] = d_time
        else:
            temp_dict['d_time'] = ip[1]
        if len(ret) !=0:
            for key in ret[0]:
                if key in ret_list:
                    temp_dict[key] = ret[0][key]
        else:
            temp_dict['ip'] = ip[0]
            temp_dict['config'] = '-'
            temp_dict['crcity'] = '-'
            temp_dict['crlacpoint'] = '-'
            temp_dict['crprovince_name'] = '-'
            temp_dict['dfcoding'] = '-'
            temp_dict['dmodel_name'] = '-'
            temp_dict['dname'] = '-'
            temp_dict['dstatus_name'] = '-'
            temp_dict['maindept_name'] = '-'
            temp_dict['mperson_name'] = '-'
            temp_dict['rname'] = '-'
        result.append(temp_dict)
    ret_list = []
    for i in result:
        ret_list.append(tuple(i.values()))
    if ret_list:
        logger.debug(ret_list)
        save_public_data.save_topo_data(ret_list)

def get_topo_ip():
    """
        获取数据表tj_public_topo中 新增ip
        @params:
            无
        @return:
            [
                "1.1.1.1",
                ...
            ]
    """
    db = MySqLHelper()
    sql = """
        SELECT
            ip,
            d_time
        FROM
            t_public_topo 
        WHERE
            ip IS NOT NULL 
            AND d_time IS NULL 
    """
    rows = db.selectall(sql=sql)
    if len(rows) == 0:
        logger.debug('无新添加ip信息')
        # return 
    else: 
        result = [tuple(row) for row in rows]
        get_topo_data(result)

def get_topo_ip_list():
    """
        获取数据表tj_public_topo中 所有ip
        @params:
            无
        @return:
            [
                "1.1.1.1",
                ...
            ]
    """
    db = MySqLHelper()
    sql = """
        SELECT
            ip,
            d_time
        FROM
            t_public_topo 
    """
    rows = db.selectall(sql=sql)
    if len(rows) == 0:
        logger.debug('t_public_topo表中无ip')
        # return 
    else:
        result = [tuple(row) for row in rows]
        get_topo_data(result)