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


def save_disk_usage(data):
    """
        入库 磁盘使用情况和关键程序监测 相关数据
        @params:
            data :   保存数据(必填参数)    list
    """
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_ipsy_used_disk (ip, usedDisk, usedDisk_data1, usedDisk_data2, usedDisk_data3,
            usedDisk_data4, usedDisk_data5, usedDisk_data6, usedDisk_data7, usedDisk_data8, usedDisk_data9,
            usedDisk_data10, usedDisk_data11, usedDisk_data12, check_df, check_jps, check_recv, d_time) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        result = db.insertmany(sql, data)
        logger.debug('save_disk_usage:{}'.format(result))
    except Exception as e:
        logger.error(e)
        # send_to_axxnr.send_message('save_disk_usage:{}'.format(e))

def save_bc_data(data):
    """
        入库 拨测 相关数据
        @params:
            data :   保存数据(必填参数)    list
    """
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_ipsy_bc (province, isp, online_report_rate, offline_report_rate, access_report_rate,
            log_standard_rate, log_loading_rate, log_query_rate, extranet_report_rate, ip_report_rate, ip_accurate_rate,
            imei_correct_rate, imsi_correct_rate, lac_correct_rate, ci_correct_rate, total_nums, d_time) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        result = db.insertmany(sql, data)
        logger.debug('save_bc_data:{}'.format(result))
    except Exception as e:
        logger.error(e)
        # send_to_axxnr.send_message('save_bc_data:{}'.format(e))