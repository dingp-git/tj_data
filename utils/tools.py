# @Copyright(C), OldFive, 2020.
# @Date : 2021/3/11 10:04:21
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
各种小工具集合
"""

# Standard library imports
import decimal
# Third party imports
from loguru import logger


# Local application imports


def round_up_x(val, x=2):
    """数值取有效小数位(使用 round 函数) [解决部分小数遇 5 不进的情况]
    @params:
        val : 需要取精确值的数据
        x   : 需要保留的有效的小数位个数, 默认 2 位
    @return:
        返回 float 类型数据
    """
    return round(val * (10 ** x)) / (10.0 ** x)


def decimal_up_x(val, x=2):
    """数值取有效小数位(使用 decimal 模块, 速度慢) [解决部分小数遇 5 不进的情况]
    @params:
        val : 需要取精确值的数据 decimal.Decimal
        x   : 需要保留的有效的小数位个数, 默认 2 位
    @return:
        返回 decimal.Decimal 类型数据
    """
    #                     注意此处使用 str
    #                     decimal.Decimal(float) 与 decimal.Decimal(str) 有差异
    return decimal.Decimal(str(val)).quantize(decimal.Decimal(('0.' + "0" * x)),
                                                rounding=decimal.ROUND_HALF_UP)


def print_logo():
    """打印logo"""
    logger.info(' ▒█████   ██▓    ▓█████▄   █████▒██▓ ██▒   █▓▓█████')
    logger.info('▒██▒  ██▒▓██▒    ▒██▀ ██▌▓██   ▒▓██▒▓██░   █▒▓█   ▀')
    logger.info('▒██░  ██▒▒██░    ░██   █▌▒████ ░▒██▒ ▓██  █▒░▒███')
    logger.info('▒██   ██░▒██░    ░▓█▄   ▌░▓█▒  ░░██░  ▒██ █░░▒▓█  ▄')
    logger.info('░ ████▓▒░░██████▒░▒████▓ ░▒█░   ░██░   ▒▀█░  ░▒████▒')
    logger.info('░ ▒░▒░▒░ ░ ▒░▓  ░ ▒▒▓  ▒  ▒ ░   ░▓     ░ ▐░  ░░ ▒░ ░')
    logger.info('  ░ ▒ ▒░ ░ ░ ▒  ░ ░ ▒  ▒  ░      ▒ ░   ░ ░░   ░ ░  ░')
    logger.info('░ ░ ░ ▒    ░ ░    ░ ░  ░  ░ ░    ▒ ░     ░░     ░')
    logger.info('    ░ ░      ░  ░   ░            ░        ░     ░  ░')
    logger.info('                  ░                      ░')
