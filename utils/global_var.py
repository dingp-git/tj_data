# @Copyright(C), OldFive, 2020.
# @Date : 2021/3/24 0024 15:36:52
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
全局变量管理
"""

# Standard library imports

# Third party imports

# Local application imports


hive_db = [
    ('/wa/wa_dams_iie_hive.db', '1'), 
    ('/wa/wa_dams_iie_hive.db/t_dams_dnsc2f', '2'),
    ('/wa/wa_dams_iie_hive.db/t_dams_dnsc2f_v6', '3'),
    ('/wa/wa_dams_iie_hive.db/t_dams_dnsc2r', '4'),
    ('/wa/wa_dams_iie_hive.db/t_dams_dnsr2a', '5'),
    ('/wa/wa_fms_iie_hive.db', '6'),
    ('/wa/wa_fms_iie_hive.db/t_flowdata', '7'),
    ('/wa/wa_fms_iie_hive.db/t_flowdata_v6', '8'),
    ('/wa/wa_zfd_tytt_hive.db', '9'),
    ('/wa/wa_zfd_tytt_hive.db/t_urllog','10')
]

def init():
    """在主模块初始化"""
    global GLOBALS_DICT
    GLOBALS_DICT = {}
    for i in hive_db:
        set_gloabls_var(i[0], i[1])


def set_gloabls_var(key, value):
    """设置"""
    try:
        GLOBALS_DICT[key] = value
        return True
    except KeyError:
        return False


def get_gloabls_var(key):
    """取值"""
    try:
        return GLOBALS_DICT[key]
    except KeyError:
        return "Not Found"