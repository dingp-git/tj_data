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
    ret_list = ['ip', 'config', 'crcity', 'crlacpoint', 'crprovince_name', 'dfcoding', 
                'dmodel_name', 'dname', 'dstatus_name', 'maindept_name', 'mperson_name', 'rname']
    result = []
    for ip in ip_list:
        url = 'http://jczy.aiops.pub:8083/jczy/device' + "?ip={}".format(ip)
        res = requests.get(url)
        ret = json.loads(res.content)
        temp_dict = {}
        for key in ret[0]:
            if key in ret_list:
                temp_dict[key] = ret[0][key]
        result.append(temp_dict)
    ret_list = []
    for i in result:
        ret_list.append(tuple(i.values()))
    if ret_list:
        logger.debug(ret_list)
        save_public_data.save_topo_data(ret_list)

def get_topo_ip():
    db = MySqLHelper()
    sql = """
        SELECT
            ip,
            config,
            crcity,
            crlacpoint,
            crprovince_name,
            dfcoding,
            dmodel_name,
            dname,
            dstatus_name,
            maindept_name,
            mperson_name,
            rname,
            d_time 
        FROM
            t_public_topo 
        WHERE
            ip IS NOT NULL 
            AND d_time IS NULL
    """
    rows = db.selectall(sql=sql)
    temp_list = [list(row) for row in rows]
    result = []
    for item in temp_list:
        result.append(item[0])
    get_topo_data(result)

