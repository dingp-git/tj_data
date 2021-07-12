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
告警判断
"""

# Standard library imports

# Third party imports

# Local application imports
from func.judge import alarm
from utils.global_var import *


def judge_data(data_flag, new_data):
    """判断当前数据是否存在异常
    data_flag = 系统名-location
    """
    if new_data == 0:
        alarm.find_alarm(data_flag + '-' + '出现0值')
    # 获取之前数据并计算3sigma
    old_data = get_gloabls_var(data_flag)
    if old_data != 'Not Found':
        # 当历史数据不足5个时不进行分析
        if len(old_data) < 6:
            old_data.append(new_data)
            set_gloabls_var(data_flag, old_data)
            return
        # 计算当前历史值的3sigma并与当前值进行比对
        else:
            sigma = operation_3sigma(old_data)
            avg = sum(old_data) / len(old_data)
            max_num = avg + sigma
            min_num = avg - sigma
            if new_data > max_num :
                alarm.find_alarm(data_flag + '-' + '数据突增')
            elif new_data < min_num:
                alarm.find_alarm(data_flag + '-' + '数据突降')
            old_data.pop(0)
            old_data.append(new_data)
            set_gloabls_var(data_flag, old_data)
            return
    else:
        set_gloabls_var(data_flag, [new_data])



def operation_3sigma(num_list):
    """3sigma计算"""
    total_numerator = 0
    total_denominator = 0
    for i, coefficient in enumerate(num_list):
        total_numerator += 2**(-i) * coefficient
        total_denominator += 2**(-i)
    return (total_numerator / total_denominator)