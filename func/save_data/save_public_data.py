# Standard library imports
import datetime, time
# Third party imports
from loguru import logger
# Local application imports
from utils.mysql_conn_pool.mysql_helper import MySqLHelper
from utils.global_var import get_gloabls_var
from utils import send_to_axxnr

def save_topo_data(data):
    """
        保存拓扑数据
        @params:
            data :   保存数据(必填参数)    list
    """
    db = MySqLHelper()
    sql = """REPLACE INTO t_public_topo (ip, config, crcity, crlacpoint, crprovince_name, 
        dfcoding, dmodel_name, dname, dstatus_name, maindept_name, mperson_name, rname, d_time) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    # sql = """INSERT IGNORE INTO t_public_topo (ip, config, crcity, crlacpoint, crprovince_name, 
    #     dfcoding, dmodel_name, dname, dstatus_name, maindept_name, mperson_name, rname) 
    #     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        result = db.insertmany(sql, data)
        logger.debug('save_topo_data: {}'.format(result))
    except Exception as e:
        logger.error(e)