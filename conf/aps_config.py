# Standard library imports

# Third party imports
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# Local application imports
from func.get_data import get_603_data, get_509_data, get_ipsy_data


jobstores = {
    'default': MemoryJobStore()     # 使用内存作为作业存储器
}

executors = {
    'default': ThreadPoolExecutor(20),  # 最大线程数为20
    'processpool': ProcessPoolExecutor(10)  # 最大进程数为10
}

job_default = {
    'coalesce': False,
    'max_instance': 3       # 作业的默认最大运行实例限制为3
}

scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_default=job_default)


# 每小时（上下浮动120秒区间内）运行'get_center_data' jitter振动参数，给每次触发添加一个随机浮动秒数,避免同时运行造成服务拥堵
# scheduler.add_job(get_603_data.get_center_data, id='get_center_data', trigger='interval', hours=1, jitter=120)
# scheduler.add_job(get_603_data.get_chanct_data, id='get_chanct_data',trigger='interval', minutes=10)
# scheduler.add_job(get_603_data.get_match_data, id='get_match_data', trigger='interval', minutes=15)
# scheduler.add_job(get_603_data.get_sms_sjjs_data, id='get_sms_sjjs_data', trigger='interval', minutes=5)
# scheduler.add_job(get_603_data.get_sms_load_data, id='get_sms_load_data', trigger='interval', minutes=5)
# scheduler.add_job(get_603_data.get_mms_sjjs_data, id='get_mms_sjjs_data', trigger='interval', minutes=5)
# scheduler.add_job(get_603_data.get_mms_load_data, id='get_mms_load_data', trigger='interval', minutes=5)
# scheduler.add_job(get_603_data.get_relate_rate_data, id='get_relate_rate_data', trigger='interval', minutes=10)

# scheduler.add_job(get_509_data.get_loading_rate_data, args=['10.41.18.69'] , id='get_loading_rate_data', trigger='interval', minutes=2)
# scheduler.add_job(get_509_data.get_hive_db_data, args=['10.41.18.69'], id='get_hive_db_data', trigger='interval', minutes=10)
# scheduler.add_job(get_509_data.get_hive_db_increment, id='get_hive_db_increment', trigger='interval', minutes=60)
# scheduler.add_job(get_509_data.get_loading_rate_increment, id='get_loading_rate_increment', trigger='interval', minutes=5)
# scheduler.add_job(get_509_data.get_row_flow, id='get_row_flow', trigger='interval', minutes=8)


scheduler.add_job(get_603_data.get_center_data, id='get_center_data', trigger='interval', minutes=6)
scheduler.add_job(get_603_data.get_chanct_data, id='get_chanct_data',trigger='interval', minutes=3)
scheduler.add_job(get_603_data.get_match_data, id='get_match_data', trigger='interval', minutes=4)
scheduler.add_job(get_603_data.get_sms_sjjs_data, id='get_sms_sjjs_data', trigger='interval', minutes=5)
scheduler.add_job(get_603_data.get_sms_load_data, id='get_sms_load_data', trigger='interval', minutes=5)
scheduler.add_job(get_603_data.get_mms_sjjs_data, id='get_mms_sjjs_data', trigger='interval', minutes=5)
scheduler.add_job(get_603_data.get_mms_load_data, id='get_mms_load_data', trigger='interval', minutes=5)
scheduler.add_job(get_603_data.get_relate_rate_data, id='get_relate_rate_data', trigger='interval', minutes=7)

scheduler.add_job(get_509_data.get_loading_rate_data, args=['10.41.18.69'] , id='get_loading_rate_data', trigger='interval', minutes=2)
scheduler.add_job(get_509_data.get_hive_db_data, args=['10.41.18.69'], id='get_hive_db_data', trigger='interval', minutes=8)
scheduler.add_job(get_509_data.get_hive_db_increment, id='get_hive_db_increment', trigger='interval', minutes=6)
scheduler.add_job(get_509_data.get_loading_rate_increment, id='get_loading_rate_increment', trigger='interval', minutes=8)
scheduler.add_job(get_509_data.get_row_flow, id='get_row_flow', trigger='interval', minutes=8)

