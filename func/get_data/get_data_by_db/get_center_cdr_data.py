# @Copyright(C), OldFive, 2020.
# @Date : 2021/3/22 0022 11:47:01
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
获取中心侧CDR数据
"""

# Standard library imports

# Third party imports
import pymysql
import datetime


# Local application imports


def get_data():
    """从数据库中获取对应数据"""
    db = pymysql.connect(host='172.27.1.12', port=3306, user='root', password='root', database='tianjin',
                         charset='utf8mb4')
    cursor = db.cursor()
    sql1 = """
          SELECT days,hours,
                cdr_f_yd_prop_imsi,
                cdr_f_lt_prop_imsi,
                cdr_f_dx_prop_imsi,
                cdr_f_yd_prop_msisdn,
                cdr_f_lt_prop_msisdn,
                cdr_f_dx_prop_msisdn,
                cdr_f_yd_prop_imei,
                cdr_f_lt_prop_imei,
                cdr_f_dx_prop_imei FROM tj_sanma_fenjia
"""
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    sql2 = """
              SELECT days,hours,
                    cdr_f_yd_prop_areacode,
                    cdr_f_lt_prop_areacode,
                    cdr_f_dx_prop_areacode,
                    cdr_f_yd_prop_uli,
                    cdr_f_lt_prop_uli,
                    cdr_f_dx_prop_uli FROM tj_erma
    """
    cursor.execute(sql2)
    result2 = cursor.fetchall()
    cursor.close()
    db.close()
    date_conversion(result1, result2)


def date_conversion(data_sanma, data_erma):
    """时间转换"""
    new_data = {}
    for da_sanma in data_sanma:
        if 'zl' not in da_sanma[1]:
            d_time = datetime.datetime.strptime(da_sanma[0], '%Y%m%d') + datetime.timedelta(hours=int(da_sanma[1]))
            new_data[d_time] = list(da_sanma[2:])

    for da_erma in data_erma:
        if 'zl' not in da_erma[1]:
            d_time = datetime.datetime.strptime(da_erma[0], '%Y%m%d') + datetime.timedelta(hours=int(da_erma[1]))
            if new_data.__contains__(d_time):
                new_data[d_time].extend(list(da_erma[2:]))
            else:
                new_data[d_time] = [0,0,0,0,0,0].extend(list(da_erma[2:]))

    save_data(new_data)


def save_data(data):
    db = pymysql.connect(host='172.27.1.12', port=3306, user='root', password='root', database='tianjin',
                         charset='utf8mb4')
    cursor = db.cursor()
    sql = """
    INSERT INTO t_603_cdr_center VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    new_data = []
    for k, y in data.items():
        if '2020-12-' in str(k):
            y.append(k)
            new_data.append(tuple(y))
    cursor.executemany(sql, new_data)
    db.commit()
    cursor.close()
    db.close()


get_data()
