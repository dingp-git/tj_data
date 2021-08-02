import uvicorn
from loguru import logger
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List
from func.save_data import save_ipsy_data

app = FastAPI()

class log_nums_item(BaseModel):
    proxy_ip_addr: List[str]
    storage_ip_addr: List[str]
    proxy_total: List[int]
    storage_total: List[int]
    d_time: List[datetime]

class log_increment_item(BaseModel):
    db_name: List[str]
    ip_addr: List[str]
    data_num: List[str]
    d_time: List[datetime]

@app.post('/tj_data/ipsy/log_nums')
async def get_log_nums(request_data: log_nums_item):
    """
         ## **param**:
            proxy_ip_addr:      代理服务器IP(必传参数)                List[str]
            storage_ip_addr:    存储服务器IP(必传参数)                List[str]
            proxy_total:        代理服务器入库数据量(必传参数)         List[int]
            storage_total:      存储服务器入库数据量(必传参数)         List[int]
            d_time:             采集时间（每30min采集一次）(必传参数)  List[datetime]
        ## **return**:
            [
                (
                    "1.1.1.1",
                    "1.1.1.1",
                    12523,
                    4511,
                    "2021-07-30T02:07:23.867000+00:00"
                ),
                ...
            ]
    """
    ret_list = [] 
    for item in request_data:
        ret_list.append(item[1])
    result = []
    for i in range(len(ret_list[0])):
        temp_list = [x[i] for x in ret_list]
        result.append(temp_list)
    if result:
        result = [tuple(j) for j in result]
        logger.debug(result)
        save_ipsy_data.save_log_data(result)


@app.post('/tj_data/ipsy/log_increment')
async def get_log_increment(request_data: log_increment_item):
    """
         ## **param**:
            db_name:      数据库/表名称(必传参数)               List[str]
            ip_addr:      服务器ip(必传参数)                   List[str]
            data_num:     数据库/表数据增量(必传参数)           List[str]
            d_time:       采集时间（每30min采集一次）(必传参数)  List[datetime]
        ## **return**:
            [
                (
                    "dbms",
                    "1.1.1.1",
                    "12523",
                    "2021-07-30T02:07:23.867000+00:00"
                ),
                ...
            ]
    """
    ret_list = []
    for item in request_data:
        ret_list.append(item[1])
    result = []
    for i in range(len(ret_list[0])):
        temp_list = [x[i] for x in ret_list]
        result.append(temp_list)
    if result:
        result = [tuple(j) for j in result]
        logger.debug(result)
        save_ipsy_data.save_log_increment(result)

