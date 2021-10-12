#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/26 13:33
# @Author  : wyq
# @File    : cron_tools.py

import croniter, datetime, time


def datetime_to_timestamp(timestring, format="%Y-%m-%d %H:%M:%S"):
    """ 将普通时间格式转换为时间戳(10位), 形如 '2016-05-05 20:28:54'，由format指定 """
    try:
        # 转换成时间数组
        timeArray = time.strptime(timestring, format)
    except Exception:
        raise
    else:
        # 转换成10位时间戳
        return int(time.mktime(timeArray))


def get_current_timestamp():
    """ 获取本地当前时间戳(10位): Unix timestamp：是从1970年1月1日（UTC/GMT的午夜）开始所经过的秒数，不考虑闰秒 """
    return int(time.mktime(datetime.datetime.now().timetuple()))


def timestamp_after_timestamp(timestamp=None, seconds=0, minutes=0, hours=0, days=0):
    """ 给定时间戳(10位),计算该时间戳之后多少秒、分钟、小时、天的时间戳(本地时间) """
    # 1. 默认时间戳为当前时间
    timestamp = get_current_timestamp() if timestamp is None else timestamp
    # 2. 先转换为datetime
    d1 = datetime.datetime.fromtimestamp(timestamp)
    # 3. 根据相关时间得到datetime对象并相加给定时间戳的时间
    d2 = d1 + datetime.timedelta(seconds=int(seconds), minutes=int(minutes), hours=int(hours), days=int(days))
    # 4. 返回某时间后的时间戳
    return int(time.mktime(d2.timetuple()))


def timestamp_datetime(timestamp, format='%Y-%m-%d %H:%M:%S'):
    """ 将时间戳(10位)转换为可读性的时间 """
    # timestamp为传入的值为时间戳(10位整数)，如：1332888820
    timestamp = time.localtime(timestamp)
    # 经过localtime转换后变成
    # time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    return time.strftime(format, timestamp)


def cron_run_next_time(sched, timeFormat="%Y-%m-%d %H:%M:%S", queryTimes=1):
    """计算定时任务下次运行时间
    sched str: 定时任务时间表达式
    timeFormat str: 格式为"%Y-%m-%d %H:%M"
    queryTimes int: 查询下次运行次数
    """
    try:
        now = datetime.datetime.now()
    except ValueError:
        raise
    else:
        # 以当前时间为基准开始计算
        cron = croniter.croniter(sched, now)
        return [cron.get_next(datetime.datetime).strftime(timeFormat) for i in range(queryTimes)]


def CrontabRunTime(sched, ctime, timeFormat="%Y-%m-%d %H:%M"):
    """计算定时任务运行次数
    sched str: 定时任务时间表达式
    ctime str: 定时任务创建的时间，与timeFormat格式对应
    timeFormat str: 格式为"%Y-%m-%d %H:%M"
    """
    try:
        ctimeStrp = datetime.datetime.strptime(ctime, timeFormat)
    except ValueError:
        raise
    else:
        # 根据定时任务创建时间开始计算
        cron = croniter.croniter(sched, ctimeStrp)
        now = get_current_timestamp()
        num = 0
        while 1:
            timestring = cron.get_next(datetime.datetime).strftime(timeFormat)
            timestamp = datetime_to_timestamp(timestring, "%Y-%m-%d %H:%M")
            if timestamp > now:
                break
            else:
                num += 1
        return num


if __name__ == '__main__':
    # sched = "*/1 * * * *"
    sched = "0 9,17 * * *"
    print(cron_run_next_time(sched))
    # ctime = "2017-08-16 15:24"
    # print(CrontabRunTime(sched, ctime))