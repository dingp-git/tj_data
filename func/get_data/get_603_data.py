# Standard library imports
import datetime
import time
import json
import urllib
# Third party imports
from loguru import logger
import pymysql
import requests
import paramiko
# Local application imports
from func.save_data import save_603_data
from func.get_data.zabbix_conf import api_url, header, data1, zabbix_key
from utils import send_to_axxnr



d_time = time.strftime("%Y%m%d")

# cdr数据
def get_center_data():
    """
        获取中心CDR数据  查询当天，当前前一个小时至当前小时 只取最新一条数据
    """
    db = pymysql.connect(host='10.239.249.5', port=3306, user='chanct', password='chanct123', 
                        database='zhiliangtongji', charset='utf8')
    # db = pymysql.connect(host='172.27.1.12', port=3306, user='root', password='root', database='tianjin',
    #                     charset='utf8mb4')
    cursor = db.cursor()
    sql1 = """SELECT
                    days,
                    hours,
                    cdr_f_yd_prop_imsi,
                    cdr_f_lt_prop_imsi,
                    cdr_f_dx_prop_imsi,
                    cdr_f_yd_prop_msisdn,
                    cdr_f_lt_prop_msisdn,
                    cdr_f_dx_prop_msisdn,
                    cdr_f_yd_prop_imei,
                    cdr_f_lt_prop_imei,
                    cdr_f_dx_prop_imei 
                FROM
                    tj_sanma_fenjia 
                WHERE
                    
                    days = DAY (NOW())
                    AND hours != '24_zl' """
    if datetime.datetime.now().hour != 0:
        sql1 += """AND hours BETWEEN HOUR(DATE_SUB(NOW(), INTERVAL 120 MINUTE)) AND HOUR(NOW()) 
                    ORDER BY days , hours DESC LIMIT 1"""
    else:
        sql1 += """AND hours = 0 ORDER BY days, hours DESC LIMIT 1"""
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    # logger.debug(sql1)
    logger.debug(len(result1))
    sql2 = """SELECT
                days,
                hours,
                cdr_f_yd_prop_areacode,
                cdr_f_lt_prop_areacode,
                cdr_f_dx_prop_areacode,
                cdr_f_yd_prop_uli,
                cdr_f_lt_prop_uli,
                cdr_f_dx_prop_uli 
            FROM
                tj_erma 
            WHERE
                days = DAY (NOW()) 
                AND hours != '24_zl' """
    if datetime.datetime.now().hour != 0:
        sql2 += """AND hours BETWEEN HOUR(DATE_SUB(NOW(), INTERVAL 120 MINUTE)) AND HOUR(NOW())
                    ORDER BY days, hours DESC LIMIT 1"""
    else:
        sql2 += """AND hours = 0 ORDER BY days, hours DESC LIMIT 1"""
    cursor.execute(sql2)
    result2 = cursor.fetchall()
    logger.debug(len(result2))
    cursor.close()
    db.close()
    ret = date_conversion(result1,result2)
    logger.debug(len(ret))
    if ret:
        save_603_data.save_center_data(ret)


def date_conversion(data_sanma, data_erma):
    """
        时间转换
        @params:
            data_sanma :   三码数据(必填参数)    tuple
            data_erma :    二码数据(必填参数)    tuple
        @return:
            {
                datetime.datetime(2020, 11, 15, 13, 0): ['0', '0', '0', ...],
                ...
            }
    """
    new_data = {}
    sanma_zero = [0,0,0,0,0,0]
    erma_zero = [0,0,0,0,0,0,0,0,0]
    for dt_sanma in data_sanma:
        if 'zl' not in dt_sanma[1]:
            d_time = datetime.datetime.strptime(dt_sanma[0], '%Y%m%d') + datetime.timedelta(hours=int(dt_sanma[1]))
            new_data[d_time] = list(dt_sanma[2:]) + sanma_zero
    for dt_erma in data_erma:
        if 'zl' not in dt_erma[1]:
            d_time = datetime.datetime.strptime(dt_erma[0], '%Y%m%d') + datetime.timedelta(hours=int(dt_erma[1]))
            if new_data.__contains__(d_time):
                new_data[d_time][9:] = list(dt_erma[2:])
            else:
                temp = new_data.setdefault(d_time,erma_zero)
                temp.extend(list(dt_erma[2:]))
    return new_data

def get_chanct_data():
    """
        获取长安CDR数据 查询当天，当前前10分钟至当前 只取最新一条组数据
    """
    d_time = time.strftime("%Y%m%d")
    db = pymysql.connect(host='10.238.72.19', port=3306, user='root', password='root', 
                        database='signalling', charset='utf8')
    # db = pymysql.connect(host='172.27.1.12', port=3306, user='root', password='root', database='tianjin',
    #                     charset='utf8mb4')
    cursor = db.cursor()
    sql = """SELECT
                cdr_type,
                net_type,
                cdr_count,
                imsi_count,
                user_num_count,
                imei_count,
                areacode_count,
                uli_count,
                isp,
                server_ip,
                stat_time 
            FROM
                cdr_qua_stat_{}
            WHERE
                stat_time BETWEEN DATE_SUB(now(), INTERVAL 20 MINUTE) AND NOW()""".format(d_time)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    result = list(result)
    logger.debug(len(result))
    if result:
        save_603_data.save_chanct_data(result)

def get_match_data():
    """
        获取上下行数据 查询当天，当前前15分钟至当前 只取最新一条组数据
    """
    d_time = time.strftime("%Y%m%d")
    db = pymysql.connect(host='10.238.72.19', port=3306, user='root', password='root', 
                        database='signalling', charset='utf8')
    # db = pymysql.connect(host='172.27.1.12', port=3306, user='root', password='root', database='tianjin',
    #     charset='utf8mb4')
    cursor = db.cursor()
    sql = """SELECT
                isp,
                protocol,
                stat_time,
                sum( req_count ),
                sum( rsp_count ),
                sum( match_count ),
                sum( match_count )/ sum( req_count ),
                sum( match_count )/ sum( rsp_count ) 
            FROM
                msg_stat_{}
            WHERE 
                stat_time BETWEEN DATE_SUB(now(), INTERVAL 30 MINUTE) AND NOW()
            GROUP BY
                isp,
                protocol,
                stat_time""".format(d_time)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    result = list(result)
    logger.debug(len(result))
    if result:
        save_603_data.save_match_data(result)


# 短彩信数据
def get_dx_sjjs_data(host_name):
    """
        获取短信接收数据
        @params:
            host_name :   主机名称(必填参数)    str
        @return:
            [
                ('10.238.33.129', '2021-03-01 14:44:00', '10.68.179.92', '41'),
                ...
            ]
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name, port=22, username='smmc2', password='tigg603')
    temp_list = []
    cmd = "cat /home/smmc2/smmc2/exe/proxy/log/cur/*nm* | grep SMSC_1M | tail -n 10 | awk -F'[][]' '{print $1,$4,$10}'|awk -F'[<: ]' '{print datenow,$2\":\"$3\":\"$4,$8,$9}' datenow=`date +%Y-%m-%d`"
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    with open(host_name, 'w') as f1:
        f1.write(result)
    with open(host_name, 'r') as f2:
        for line in f2:
            line = host_name + ' ' + line.strip()
            data = line.split()
            data = (data[0], data[1] + ' ' + data[2], data[3], data[4])
            temp_list.append(data)
    client.close()
    return temp_list

def get_sms_sjjs_data():
    """
        获取所有主机 短信接收数据
    """
    hostlist = ['10.238.33.129', '10.238.33.130', '10.238.33.131', '10.238.33.132', '10.238.40.129', '10.238.40.130',
                '10.238.48.129', '10.238.48.130']
    for host in hostlist:
        result = get_dx_sjjs_data(host)
        logger.debug(len(result))
        if result:
            save_603_data.save_sms_sjjs_data(result)


def get_dx_load_data(host_name):
    """
        获取短信加载数据
        @params:
            host_name :   主机名称(必填参数)    str
        @return:
            [
                ('10.238.76.11', '2021-03-01 14:47:00', '10.238.69.14', '8000'),
                ...
            ]
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name, port=22, username='smmc2', password='tigg603')
    temp_list = []
    cmd = "cat /home/smmc2/smmc2/exe/load/log/cur/*nm* |grep UPLOAD_1M | tail -n 10 | grep -v 10.238.69.25 | grep -v 10.238.69.26 | awk -F'[][]' '{print $1,$4,$6}' |awk -F'<' '{print $2}'|awk -F':' '{print $1\":\"$2\":\"$3,$5,$6}' |awk '{print datenow,$1,$2,$4}' datenow=\"`date +%Y-%m-%d`\""
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    with open(host_name, 'w') as f1:
        f1.write(result)
    with open(host_name, 'r') as f2:
        for line in f2:
            line = host_name + ' ' + line.strip()
            data = line.split(" ")
            temp_list.append(tuple(data))
    client.close()
    ret_list = []
    for tu in temp_list:
        data = tu[0],tu[1]+' '+tu[2],tu[3],tu[4]
        ret_list.append(data)
    return ret_list

def get_sms_load_data():
    """
        获取所有主机 短信加载数据
    """
    hostlist = ['10.238.76.11', '10.238.76.12']
    for host in hostlist:
        result = get_dx_load_data(host)
        logger.debug(len(result))
        if result:
            save_603_data.save_sms_load_data(result)


def get_cx_yd_sjjs_data(host_name):
    """
        获取彩信 移动接收数据
        @params:
            host_name :   主机名称(必填参数)    str
        @return:
            [
                ('10.238.16.1', '2021-03-01 14:43:00', '10.10.5.7', '118'),
                ...
            ]
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name, port=22, username='mmmc', password='mmmc')
    temp_list = []
    cmd = "cat /home/mmmc/cx_sjjs/log/cx_sjjs.log |grep MMS:|grep 10.10.5.7 |tail -n 5|awk '{print $1,$2,$6}'|awk -F'[][]' '{print $1,$4}'| awk -F'#report:' '{print $1,\"10.10.5.7\",$2}';cat /home/mmmc/cx_sjjs/log/cx_sjjs.log |grep MMS:|grep 10.10.5.8 |tail -n 5|awk '{print $1,$2,$6}'|awk -F'[][]' '{print $1,$4}'| awk -F'#report:' '{print $1,\"10.10.5.8\",$2}'"
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    with open(host_name, 'w') as f1:
        f1.write(result)
    with open(host_name, 'r') as f2:
        for line in f2:
            line = host_name + ' ' + line.strip()
            data = line.split(" ")
            data = [i for i in data if i != '']
            temp_list.append(tuple(data))
    client.close()
    ret_list = []
    for li in temp_list:
        data = (li[0], li[1] + ' ' + li[2], li[3], li[4])
        ret_list.append(data)
    return ret_list

def get_cx_lt_sjjs_data(host_name):
    """
        获取彩信 联通接收数据
        @params:
            host_name :   主机名称(必填参数)    str
        @return:
            [
                ('10.238.16.1', '2021-03-01 14:43:00', '10.10.5.7', '118'),
                ...
            ]
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name, port=22, username='mmmc', password='mmmc')
    temp_list = []
    cmd = "cat /home/mmmc/cx_sjjs/log/cx_sjjs.log |grep MMS:|grep 10.10.4.219 |tail -n 5|awk '{print $1,$2,$6}'|awk -F'[][]' '{print $1,$4}'| awk -F'#report:' '{print $1,\"10.10.4.219\",$2}'"
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    with open(host_name, 'w') as f1:
        f1.write(result)
    with open(host_name, 'r') as f2:
        for line in f2:
            line = host_name + ' ' + line.strip()
            data = line.split(" ")
            data = [i for i in data if i != '']
            temp_list.append(tuple(data))
    client.close()
    ret_list = []
    for li in temp_list:
        data = (li[0], li[1] + ' ' + li[2], li[3], li[4])
        ret_list.append(data)
    return ret_list

def get_cx_dx_sjjs_data(host_name):
    """
        获取彩信 电信接收数据
        @params:
            host_name :   主机名称(必填参数)    str
        @return:
            [
                ('10.238.16.1', '2021-03-01 14:43:00', '10.10.5.7', '118'),
                ...
            ]
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name, port=22, username='mmmc', password='mmmc')
    temp_list = []
    cmd = "cat /home/mmmc/cx_sjjs/log/cx_sjjs.log |grep MMS:|grep 192.168.10.190 |tail -n 5|awk '{print $1,$2,$6}'|awk -F'[][]' '{print $1,$4}'| awk -F'#report:' '{print $1,\"192.168.10.190\",$2}'"
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    with open(host_name, 'w') as f1:
        f1.write(result)
    with open(host_name, 'r') as f2:
        for line in f2:
            line = host_name + ' ' + line.strip()
            data = line.split(" ")
            data = [i for i in data if i != '']
            temp_list.append(tuple(data))
    client.close()
    ret_list = []
    for li in temp_list:
        data = (li[0], li[1] + ' ' + li[2], li[3], li[4])
        ret_list.append(data)
    return ret_list

def get_mms_yd_sjjs_data():
    """
        获取彩信 移动 所有主机收数据
    """
    hostlist = ['10.238.16.1', '10.238.16.2']
    for host in hostlist:
        result = get_cx_yd_sjjs_data(host)
        logger.debug(len(result))
        if result:
            save_603_data.save_mms_sjjs_data(result)


def get_mms_lt_sjjs_data():
    """
        获取彩信 联通 所有主机接收数据
    """
    hostlist = ['10.238.21.1', '10.238.21.2']
    for host in hostlist:
        result = get_cx_lt_sjjs_data(host)
        logger.debug(len(result))
        if result:
            save_603_data.save_mms_sjjs_data(result)


def get_mms_dx_sjjs_data():
    """
        获取彩信 电信 所有主机接收数据
    """
    hostlist = ['10.238.26.1', ]
    for host in hostlist:
        result = get_cx_dx_sjjs_data(host)
        logger.debug(len(result))
        if result:
            save_603_data.save_mms_sjjs_data(result)


def get_mms_sjjs_data():
    """
        获取彩信 所有主机接收数据
    """
    get_mms_yd_sjjs_data()
    get_mms_lt_sjjs_data()
    get_mms_dx_sjjs_data()

def get_cx_load_data(host_name):
    """
        获取彩信加载数据
        @params:
            host_name :   主机名称(必填参数)    str
        @return:
            [
                ('10.238.77.5', '2021-03-01 14:42:00', '623'),
                ...
            ]
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host_name, port=22, username='mmmc', password='mmmc')
    temp_list = []
    cmd = "cat /mmmc/cx_sjjz_szx/log/cx_sjjz_szx.log | grep Trafic-Min | grep AvroCxMin |tail -n 6|awk -F'[][]' '{print $1,$6}'|awk '{print $1,$2,$5}'"
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    with open(host_name, 'w') as f1:
        f1.write(result)
    with open(host_name, 'r') as f2:
        for line in f2:
            line = host_name + ' ' + line.strip()
            data = line.split(" ")
            data = [i for i in data if i != '']
            temp_list.append(tuple(data))
    client.close()
    ret_list = []
    for li in temp_list:
        data = (li[0], li[1] + ' ' + li[2], li[3])
        ret_list.append(data)
    return ret_list

def get_mms_load_data():
    """
        获取所有主机 彩信加载数据
    """
    hostlist = ['10.238.77.5', '10.238.77.6']
    for host in hostlist:
        result = get_cx_load_data(host)
        logger.debug(len(result))
        if result:
            save_603_data.save_mms_load_data(result)



# 关联率数据
class ZabbixApi():
    """
        使用requests调用ZabbixApi
    """
    def __init__(self):
        self.url = api_url
        self.header = header

    def get_host(self,data):
        request = requests.post(url=self.url, headers=self.header, data=data)
        response = json.loads(request.text)
        request.close()
        return response['result']


def get_hosts():
    # TODO 补充return返回数据
    """
        获取主机列表hostid, hostid和服务器对应关系
        @return:
            host_list : []
            host_dict : {}
    """
    p = ZabbixApi()
    host_list = []
    host_dict = {}
    for host in p.get_host(data1):
        host_dict[host['hostid']] = host['name']
        host_list.append(host['hostid'])
    return host_list, host_dict

def get_items():
    # TODO 补充return返回数据
    """
        获取每台服务器的hostid, 服务器ip地址, 监控项id, 服务器的关联率监控项
        @return:
            items : []
    """
    hostid_list, hostid_dict = get_hosts()
    p1 = ZabbixApi()
    items = []
    for hostid in hostid_list:
        data2 = json.dumps(
            {
                "jsonrpc": "2.0",
                    "method": "item.get",
                    "params": {
                        "output": ["itemids", "key_"],
                        "hostids": hostid,
                        "search": {
                            "key_": "gll.sta.E"
                        },
                    },
                    "auth": zabbix_key,
                    "id": 1,
            }
        )
        if p1.get_host(data2):
            items.append((hostid, hostid_dict[hostid], p1.get_host(data2)))
    return items

def get_relate_rate_data():
    """
        获取每台服务器下关联率的历史数据
    """
    items = get_items()
    p2 = ZabbixApi()
    result = []
    for item in items:
        data3 = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": 5,
                    "itemids": item[2][0]['itemid'],
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "limit": 1
                },
                "auth": zabbix_key,
                "id": 1,
            }
        )
        host = p2.get_host(data3)
        for i in host:
            time_stamp = int(i['clock'])
            time_array = time.localtime(time_stamp)
            clock = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
            temp_item = (str(clock), str(item[1]), float(i['value']))
            result.append(temp_item)
    logger.debug(len(result))
    if result:
        save_603_data.save_relate_rate_data(result)




