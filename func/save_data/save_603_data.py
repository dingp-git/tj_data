# Standard library imports
import datetime, time
# Third party imports
from loguru import logger
# Local application imports
from utils.mysql_conn_pool.mysql_helper import MySqLHelper
from utils import send_to_axxnr


def save_center_data(data):
    """
        保存中心CDR数据
        @params:
            data :   保存数据(必填参数)    list
    """
    # print(111)
    return 'save center data success!'
    db = MySqLHelper()
    sql = """INSERT INTO t_603_cdr_center (imsi_cmcc_rates, imsi_cucc_rates, imsi_ctcc_rates, msisdn_cmcc_rates, 
            msisdn_cucc_rates, msisdn_ctcc_rates, imei_cmcc_rates, imei_cucc_rates, imei_ctcc_rates, areacode_cmcc_rates,
            areacode_cucc_rates, areacode_ctcc_rates, uli_cmcc_rates, uli_cucc_rates, uli_ctcc_rates, d_time)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    new_data = []
    for k,v in data.items():
        v.append(k)
        new_data.append(tuple(v))
    try:
        db.insertmany(sql,new_data)
    except Exception as e:
        logger.error(e)
        send_to_axxnr.send_message('save_center_data:{}'.format(e))


def save_chanct_data(data):
    """
        保存长安CDR数据
        @params:
            data :   保存数据(必填参数)    list
    """
    return 'save chanct data success!'
    db = MySqLHelper()
    sql = """INSERT INTO t_603_cdr_chanct 
            (cdr_type, net_type, cdr_count, imsi_count, user_num_count, imei_count, areacode_count, 
            uli_count, isp, ip_addr, d_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        db.insertmany(sql, data)
    except Exception as e:
        logger.error(e)
        send_to_axxnr.send_message('save_chanct_data:{}'.format(e))

def save_match_data(data):
    """
        保存上下行数据
        @params:
            data :   保存数据(必填参数)    list
    """
    return 'save metch data success!'
    db = MySqLHelper()
    sql = """INSERT INTO t_603_req_rsp_match 
            (isp, protocol, d_time, req_count_sum, rsp_count_sum, match_count_sum, req_match_rate, rsp_match_rate)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        db.insertmany(sql, data)
    except Exception as e:
        logger.error(e)
        send_to_axxnr.send_message('save_match_data:{}'.format(e))

def save_sms_sjjs_data(data):
    """
        保存短信接收数据
        @params:
            data :   保存数据(必填参数)    list
    """
    return 'save_sms_sjjs_data success!'
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_603_sms_sjjs (ip_addr, d_time, isp_ip, sjjs_1m)
                VALUES (%s,%s,%s,%s)"""
    try:
        db.insertmany(sql, data)
    except Exception as e:
        logger.error(e)
        send_to_axxnr.send_message('save_sms_sjjs_data:{}'.format(e))

def save_sms_load_data(data):
    """
        保存短信加载数据
        @params:
            data :   保存数据(必填参数)    list
    """
    return 'save_sms_load_data success!'
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_603_sms_load (ip_addr, d_time, isp_ip, load_1m)
                VALUES (%s,%s,%s,%s)"""
    try:
        db.insertmany(sql, data)
    except Exception as e:
        logger.error(e)
        send_to_axxnr.send_message('save_sms_load_data:{}'.format(e))

def save_mms_sjjs_data(data):
    """
        保存彩信接收数据
        @params:
            data :   保存数据(必填参数)    list
    """
    return 'save_mms_sjjs_data success!'
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_603_mms_sjjs (ip_addr, d_time, isp_ip, sjjs_1m)
                VALUES (%s,%s,%s,%s)"""
    try:
        db.insertmany(sql, data)
    except Exception as e:
        logger.error(e)
        send_to_axxnr.send_message('save_mms_sjjs_data:{}'.format(e))

def save_mms_load_data(data):
    """
        保存彩信加载数据
        @params:
            data :   保存数据(必填参数)    list
    """
    return 'save_mms_load_data success!'
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_603_mms_load (ip_addr, d_time, load_1m)
                VALUES (%s,%s,%s,%s)"""
    try:
        db.insertmany(sql, data)
    except Exception as e:
        logger.error(e)
        send_to_axxnr.send_message('save_mms_load_data:{}'.format(e))

def save_relate_rate_data(data):
    """
        保存关联率数据
        @params:
            data :   保存数据(必填参数)    list
    """
    return 'save_relate_rate_data success!'
    db = MySqLHelper()
    sql = """INSERT IGNORE INTO t_603_relate_rate (d_time, ip_addr, relate_rate)
                VALUES (%s,%s,%s)"""
    try:
        db.insertmany(sql, data)
    except Exception as e:
        logger.error(e)
        send_to_axxnr.send_message('save_relate_rate_data:{}'.format(e))



