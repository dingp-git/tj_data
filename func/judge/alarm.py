# @Copyright(C), OldFive, 2020.
# @Date : 2021/3/24 0024 13:56:30
# @Author : OldFive
# @Version : 0.1
# @Description : 
# @History :
# @Other:
#  ▒█████   ██▓    ▓█████▄   █████▒██▓ ██▒   █▓▓█████
# ▒██▒  ██▒▓██▒    ▒██▀ ██▌▓██   ▒▓██▒▓██░   █▒▓█   ▀
# ▒██░  ██▒▒██░    ░██   █▌▒████ ░▒██▒ ▓██  █▒░▒███
# ▒██   ██░▒██░    ░▓█▄   ▌░▓█▒  ░░██░  ▒██ █░░▒▓█  ▄
# ░ ████▓▒░░██████▒░▒████▓ ░▒█░   ░██░   ▒▀█░  ░▒████▒
# ░ ▒░▒░▒░ ░ ▒░▓  ░ ▒▒▓  ▒  ▒ ░   ░▓     ░ ▐░  ░░ ▒░ ░
#   ░ ▒ ▒░ ░ ░ ▒  ░ ░ ▒  ▒  ░      ▒ ░   ░ ░░   ░ ░  ░
# ░ ░ ░ ▒    ░ ░    ░ ░  ░  ░ ░    ▒ ░     ░░     ░
#     ░ ░      ░  ░   ░            ░        ░     ░  ░
#                   ░                      ░
#
"""
检查告警信息并存入数据库
"""


# Standard library imports
import uuid
import datetime
# Third party imports
from loguru import logger
# Local application imports
from utils.mysql_conn_pool.mysql_helper import MySqLHelper
from utils.global_var import *

def find_alarm(data_flag, judge_flag):
    """查询缓存中是否含有当前告警"""
    alarm_flag = 'alarm-' + data_flag
    # 当前数据存在告警
    if judge_flag:
        alarm_data = get_gloabls_var(alarm_flag)
        # 当前缓存存在告警 更新缓存及数据库
        if alarm_data != 'Not Found':
            alarm_data = get_gloabls_var(alarm_flag)
            alarm_data['alarm_times'] = alarm_data['alarm_times'] + 1
            set_gloabls_var(alarm_flag, alarm_data)
            add_alarm_times(alarm_data['alarm_id'])
        # 当前缓存不存在告警 在缓存新建告警数据并存入数据库
        else:
            alarm_id = ''.join(str(uuid.uuid4()).split('-'))
            alarm_data = {
                'alarm_id': alarm_id,
                'alarm_times': 1,
                'alarm_heppen_d_time': datetime.datetime.now()
            }
            set_gloabls_var(alarm_flag, alarm_data)
            add_alarm(alarm_flag, alarm_data)
    # 当前数据不存在告警
    else:
        alarm_data = get_gloabls_var(alarm_flag)
        # 当前缓存存在告警 更新缓存及数据库 将当前告警移入历史告警
        if alarm_data != 'Not Found':
            del_gloabls_var(alarm_flag)
            del_alarm(get_gloabls_var(alarm_flag)['alarm_id'])
        # 当前缓存不存在告警
        else:
            return




def del_alarm(alarm_id):
    """告警结束后将告警转移到历史告警表"""
    db = MySqLHelper()
    # 将告警表中的数据插入到历史告警表
    sql = """INSERT INTO t_alarm_history(alarm_id, alarm_location, alarm_system, 
    alarm_level, alarm_type, alarm_text, happen_times, happen_d_time, end_d_time) 
    SELECT alarm_id, alarm_location, alarm_system, alarm_level, alarm_type, 
    alarm_text, happen_times, happen_d_time, NOW() FROM t_alarm WHERE alarm_id = '%s'""" % alarm_id
    try:
        result = db.insertone(sql)
        logger.debug('del_alarm:{}'.format(result))
    except Exception as e:
        logger.error(e)

    # 删除告警表中数据
    sql = """DELETE FROM t_alarm WHERE alarm_id = '%s'""" % alarm_id
    try:
        result = db.delete(sql)
        logger.debug('del_alarm:{}'.format(result))
    except Exception as e:
        logger.error(e)


def add_alarm_times(alarm_id, alarm_times):
    """增加数据库中告警次数"""
    db = MySqLHelper()
    sql = """UPDATE t_alarm SET happen_times = '%s' WHERE alarm_id =  '%s'""" % (alarm_times, alarm_id)
    try:
        result = db.update(sql)
        logger.debug('del_alarm:{}'.format(result))
    except Exception as e:
        logger.error(e)

def add_alarm(alarm_flag, alarm_data):
    """增加新告警"""
    alarm_data = alarm_data.split('-')
    alarm_location = alarm_flag[2]
    alarm_system = alarm_flag[1]
    alarm_text = alarm_flag[3]
    alarm_id = alarm_data['alarm_id']
    db = MySqLHelper()
    # 将告警表中的数据插入到历史告警表
    sql = """INSERT INTO t_alarm(alarm_id, alarm_location, alarm_system, 
    alarm_text, happen_times, happen_d_time) 
    VALUES (%s, %s, %s, %s, 1, NOW())""" % (alarm_id, alarm_location, alarm_system, alarm_text)
    try:
        result = db.insertone(sql)
        logger.debug('del_alarm:{}'.format(result))
    except Exception as e:
        logger.error(e)
