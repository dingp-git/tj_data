"""
ipsy相关数据
"""

# 磁盘使用情况和关键指标监测   相关数据
ip_list = ['10.238.183.1', '10.238.183.2', '10.238.183.3', '10.238.183.4', '10.238.183.5',
            '10.238.183.6', '10.238.183.11', '10.238.183.31','10.238.183.32', '10.238.183.33', 
            '10.238.183.71', '10.238.183.72', '10.238.183.73', '10.238.183.81', '10.238.183.82', 
            '10.238.184.1', '10.238.184.2', '10.238.184.3', '10.238.184.4', '10.238.184.5', 
            '10.238.184.6', '10.238.184.7', '10.238.184.121', '10.238.184.122', '10.238.184.123', 
            '10.238.184.131', '10.238.184.132', '10.238.184.133', '10.238.184.134', '10.238.184.135',
            '10.238.184.136', '10.238.185.1', '10.238.185.2', '10.238.185.3', '10.238.185.4',
            '10.238.185.5', '10.238.185.6', '10.238.185.7', '10.238.185.8', '10.238.185.9', 
            '10.238.185.10', '10.238.185.11', '10.238.185.12', '10.238.185.13', '10.238.185.14',
            '10.238.185.15', '10.238.185.16', '10.238.185.17', '10.238.185.18', '10.238.185.19', 
            '10.238.185.20', '10.238.185.21', '10.238.185.22', '10.238.185.23']

def get_ip_cmd(ip):
    """
        获取每个ip的mingling
        @param:     ip          类型     str
        @return:    cmd_list   类型     list[str,str,...]
    """
    cmd_list = ['./zabbix_get -s {} -k UsedDisk[/]'.format(ip),
            './zabbix_get -s {} -k UsedDisk[/opt/data1]'.format(ip),
            './zabbix_get -s {} -k UsedDisk[/opt/data2]'.format(ip),
            './zabbix_get -s {} -k UsedDisk[/opt/data3]'.format(ip),
            './zabbix_get -s {} -k UsedDisk[/opt/data4]'.format(ip),
            './zabbix_get -s {} -k UsedDisk[/opt/data5]'.format(ip),
            './zabbix_get -s {} -k UsedDisk[/opt/data6]'.format(ip),
            './zabbix_get -s {} -k UsedDisk[/opt/data7]'.format(ip),
            './zabbix_get -s {} -k UsedDisk[/opt/data8]'.format(ip),
            './zabbix_get -s {} -k UsedDisk[/opt/data9]'.format(ip),
            './zabbix_get -s {} -k UsedDisk[/opt/data10]'.format(ip),
            './zabbix_get -s {} -k UsedDisk[/opt/data11]'.format(ip),
            './zabbix_get -s {} -k UsedDisk[/opt/data12]'.format(ip),
            './zabbix_get -s {} -k check_df'.format(ip),
            './zabbix_get -s {} -k check_jps'.format(ip),
            './zabbix_get -s {} -k check_recv'.format(ip),
            ]
    return cmd_list

def get_now_date_time():
    """
        获取当前时间  "2020-11-20 22:00:00"
    """
    now_date_time= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now_date_time