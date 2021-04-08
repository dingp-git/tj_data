# Standard library imports
import datetime, time
# Third party imports
from loguru import logger
# Local application imports
from utils.mysql_conn_pool.mysql_helper import MySqLHelper
from utils.global_var import get_gloabls_var
from utils import send_to_axxnr


def save_loading_rate_data(data):
    """
        保存加载率数据
        @params:
            data :   保存数据(必填参数)    list
    """
    # return 'save_loading_rate_data success!'
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_509_loading_rate (device, ip_port, d_time, data)
                VALUES (%s,%s,%s,%s)"""
    try:
        result = db.insertmany(sql, data)
        logger.debug('save_loading_rate_data:{}'.format(result))
    except Exception as e:
        logger.error(e)
        # send_to_axxnr.send_message('save_loading_rate_data:{}'.format(e))

def save_hive_db_data(data):
    """
        保存hive db数据
        @params:
            data :   保存数据(必填参数)    list
    """
    # return 'save_hive_db_data success!'
    db = MySqLHelper()
    data_list = [list(i) for i in data]
    for j in data_list:
        j[0] = get_gloabls_var(j[0])
    data_tuple = [tuple(k) for k in data_list]
    sql = """INSERT IGNORE INTO t_509_hive_db (db_id, data, d_time)
                VALUES (%s,%s,%s)"""
    try:
        result = db.insertmany(sql, data_tuple)
        logger.debug('save_hive_db_data:{}'.format(result))
    except Exception as e:
        logger.error(e)
        # send_to_axxnr.send_message('save_hive_db_data:{}'.format(e))

def save_hive_db_increment(data):
    """
        保存hive db数据增量
        @params:
            data :   保存数据(必填参数)    list
    """
    # return 'save_hive_db_increment success!'
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_509_hive_db_increment (db_id, increment, d_time)
                VALUES (%s,%s,%s)"""
    try:
        result = db.insertmany(sql, data)
        logger.debug('save_hive_db_increment:{}'.format(result))
    except Exception as e:
        logger.error(e)
        # send_to_axxnr.send_message('save_hive_db_increment:{}'.format(e))

def save_loading_rate_increment(data):
    """
        保存加载率数据增量
        @params:
            data :   保存数据(必填参数)    list
    """
    # return 'save_loading_rate_increment success!'
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_509_loading_rate_increment (device, ip_port, d_time, increment)
                VALUES (%s,%s,%s,%s)"""
    try:
        result = db.insertmany(sql, data)
        logger.debug('save_loading_rate_increment:{}'.format(result))
    except Exception as e:
        logger.error(e)
        # send_to_axxnr.send_message('save_loading_rate_increment:{}'.format(e))