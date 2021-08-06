# Standard library imports
import datetime, time
# Third party imports
from loguru import logger
# Local application imports
from utils.mysql_conn_pool.mysql_helper import MySqLHelper
from utils.global_var import get_gloabls_var
from utils import send_to_axxnr


def save_log_data(data):
    """
        入库 日志量数据 相关数据
        @params:
            data :   保存数据(必填参数)    list
    """
    # return 'save_log_data success!'
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_ipsy_log_nums (province, lt_yw, yd_yw, dx_yw, 
        lt_gw, yd_gw, dx_gw, d_time ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        result = db.insertmany(sql, data)
        logger.debug('save_log_data:{}'.format(result))
    except Exception as e:
        logger.error(e)
        # send_to_axxnr.send_message('save_log_data:{}'.format(e))

def save_log_increment(data):
    """
        入库 日志量数据增量 相关数据
        @params:
            data :   保存数据(必填参数)    list
    """
    # return 'save_log_increment success!'
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_ipsy_log_increment (province, lt_yw_diff, yd_yw_diff, dx_yw_diff, 
        lt_gw_diff, yd_gw_diff, dx_gw_diff, d_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        result = db.insertmany(sql, data)
        logger.debug('save_log_increment:{}'.format(result))
    except Exception as e:
        logger.error(e)
        # send_to_axxnr.send_message('save_log_increment:{}'.format(e))

def save_proxy_ip_data(data):
    """
        入库 代理服务器数据是否正常入库 相关数据
        @params:
            data :   保存数据(必填参数)    list
    """
    # return 'save_proxy_ip_data success!'
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_ipsy_proxy_ip_data (proxy_ip_addr, storage_ip_addr, proxy_total, storage_total, d_time )
                VALUES (%s,%s,%s,%s,%s)"""
    try:
        result = db.insertmany(sql, data)
        logger.debug('save_log_data:{}'.format(result))
    except Exception as e:
        logger.error(e)
        # send_to_axxnr.send_message('save_proxy_ip_data:{}'.format(e))

def save_database_produce_data(data):
    """
        入库 当天库表产生情况 相关数据
        @params:
            data :   保存数据(必填参数)    list
    """
    # return 'save_database_produce_data success!'
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_ipsy_database_produce_data (db_name, ip_addr, data_num, d_time) VALUES (%s,%s,%s,%s)"""
    try:
        result = db.insertmany(sql, data)
        logger.debug('save_database_produce_data:{}'.format(result))
    except Exception as e:
        logger.error(e)
        # send_to_axxnr.send_message('save_database_produce_data:{}'.format(e))
