# @Copyright(C), OldFive, 2020.
# @Date : 2021/3/18 0018 9:48:47
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
主入口
"""

# Standard library imports

# Third party imports
from loguru import logger
# from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
# Local application imports
from conf.sys_config import *
from utils import global_var
# from utils.aps_config import scheduler
from conf.aps_config import scheduler


def init():
    """初始化各种东西"""
    # 日志初始化
    if isFormalSystem:
        logger.add(LOG_CONF['LOG_FORM_PATH'] + '_{time:YYYY-MM-DD}.log', rotation='00:00',
                    retention=LOG_CONF['LOG_RETENTION'], level=LOG_CONF['LOG_LEVEL'], enqueue=True, encoding='utf8')
    # 全局变量管理初始化
    global_var.init()


def main():
    """定时任务启动处"""
    # 采集程序启动
    try:
        scheduler.start()
    except Exception as e:
        logger.error(e)
    # 存储程序启动

    # 判断程序启动


if __name__ == '__main__':
    main()
