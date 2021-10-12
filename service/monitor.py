#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/26 12:05
# @Author  : wyq
# @File    : monitor.py

from common_tools import sql_lite_monitor
from common_tools import sql_lite_monitor_source
from common_tools import cron_tools
from common_tools import sql_monitor_style
from common_tools import mysql_tools
from common_tools import send_email
from common_tools import log_tools
from threading import Thread
import datetime
import time
import queue

now_main_thread = None
exit_tag = False
logging = log_tools.Logger('monitor', 'monitor.log').get_logger()


class Monitor(Thread):
    """
    监控线程  每个sql对应一个线程
    """
    def __init__(self, item):
        Thread.__init__(self)
        self.title = item.title
        self.receiver = item.receiver
        self.cron = item.cron_str
        self.sql = item.sql_str
        self.source = item.source
        self._id = item.id
        self.next_time = item.next_time
        self.result = None
        self.content = ''
        self.conn = self.get_conn()
        self.count = 0

    def run(self):
        logging.info('任务%s在%s开始执行' % (self._id, self.next_time))
        try:
            self.result = mysql_tools.execute_df_query_with_header(self.conn, self.sql)
            if self.result is not None:
                # 开始报警
                logging.warn('任务%s在%s执行时满足报警条件,开始报警' % (self._id, self.next_time))
                self.send_waring_email()

        except Exception as e:
            logging.error(e)
            logging.error('任务%s在执行sql时报错' % self._id)
        finally:
            self.conn.close()

    def send_waring_email(self):
        """
        发送报警邮件，带html样式
        :return:
        """
        style = sql_monitor_style.style
        self.count = mysql_tools.execute_query_return_count(self.conn, self.sql)
        self.content = "<style>" + style + "</style>"
        self.content += self.result.to_html(header=True, border=0, classes='table15_1', index=False)
        self.content += '\n\n<br/><br/>执行结果共<font style="color:red">{}</font>条:\n'.format(self.count)
        self.content += '\n\n<br/><br/>执行sql:\n' + self.sql
        # logging.debug(self.title)
        send_email.send_email_by_csr(self.content, self.title, self.receiver)
        logging.info('%s %s报警邮件发送成功' % (self._id, self.title))

    def get_conn(self):
        """
        从配置数据源的数据库中读取 数据库配置，建立并返回数据库连接
        :return:
        """
        conn_obj = sql_lite_monitor_source.query_by_name(self.source)
        return mysql_tools.get_conn_by_obj(conn_obj)


class MonitorItem(object):
    """
    监控类实体
    """
    def __init__(self, item):
        self.title = item['title']
        self.receiver = item['receiver']
        self.cron_str = item['cron_str']
        self.sql_str = item['sql_str']
        self.source = item['source']
        self.id = item['id']
        self.next_time = item['next_time']

    def __lt__(self, other):
        return self.next_time < other.next_time

    def __str__(self):
        return '(' + str(self.id)+',\'' + self.title + ',\'' + self.cron_str + ',\'' + self.next_time + '\')'


# 用于前端页面查询
def get_all():
    rows = sql_lite_monitor.query_all()
    result = {
        'rows': rows,
        'total': len(rows)
    }
    return result


def delete(ids):
    try:
        ids = ids.split(',')
        sql_lite_monitor.execute_delete(ids)
        restart()
        logging.info("删除成功, %s" % ids)
        return 'success'
    except Exception as e:
        logging.error(e)
        return 'error'


def execute(_id):
    row = sql_lite_monitor.query_one((_id,))
    row['next_time'] = datetime.datetime.now()
    item = MonitorItem(row)
    next_job = Monitor(item)
    next_job.start()
    next_job.join()
    if next_job.result is not None:
        return next_job.content
    else:
        return "执行sql返回结果为空，不发送报警邮件"


# 保存  需要保证顺序 title,receiver,cron_str,sql_str
def save(form):
    try:
        title = form['title']
        receiver = form['receiver']
        cron_str = form['cron_str']
        sql_str = form['sql_str']
        source = form['source']
        _id = form['id']
        item = (title, receiver, cron_str, sql_str, source) if len(_id) == 0\
            else (title, receiver, cron_str, sql_str, source, _id)
        sql_lite_monitor.execute_save(item)
        logging.info("保存成功, %s" % item.__str__())
        restart()
        return 'success'
    except Exception as e:
        logging.error(e)
        return e


def start_monitor():
    logging.info('开始启动全部监控任务')
    rows = sql_lite_monitor.query_all()
    # 优先级队列  自动排序
    q = queue.PriorityQueue()
    if rows is None or len(rows) <= 0:
        logging.info("无监控任务")
        return
    # 初始化队列
    for row in rows:
        row['next_time'] = cron_tools.cron_run_next_time(row['cron_str'])[0]
        item = MonitorItem(row)
        q.put(item)
    while True:
        if q.empty():
            logging.info('队列已消耗完毕，等待10秒')
            time.sleep(10)
            continue
        recent_item = q.get()
        now_time = datetime.datetime.now()
        next_time = datetime.datetime.strptime(recent_item.next_time, '%Y-%m-%d %H:%M:%S')
        # 测试单个线程运行情况
        # next_job = Monitor(recent_item)
        # next_job.start()
        # break
        if next_time <= now_time:
            logging.info('下次执行时间%s小于等于当前时间%s，开始执行' % (next_time, now_time))
            next_job = Monitor(recent_item)
            next_job.start()
            recent_item.next_time = cron_tools.cron_run_next_time(recent_item.cron_str)[0]
            logging.info('id为%s的任务下次执行时间%s' % (recent_item.id, recent_item.next_time))
            q.put(recent_item)
        else:
            remain_time = (next_time - now_time).seconds
            logging.info('下次任务将在%s秒后执行，任务信息：%s' % (remain_time, recent_item))
            time.sleep(remain_time)
            next_job = Monitor(recent_item)
            next_job.start()
            recent_item.next_time = cron_tools.cron_run_next_time(recent_item.cron_str)[0]
            logging.info('id为%s的任务下次执行时间%s' % (recent_item.id, recent_item.next_time))
            q.put(recent_item)
        global now_main_thread, exit_tag
        if exit_tag:
            now_main_thread = Thread(target=start_monitor)
            exit_tag = False
            now_main_thread.start()
            logging.info('重启全部监控成功')
            break


def restart():
    global now_main_thread, exit_tag
    if now_main_thread is not None:
        if exit_tag is False:
            logging.info(now_main_thread)
            logging.info('重启指令已接收，将在下次监控任务执行完后重启所有监控')
            exit_tag = True
    else:
        exit_tag = False
        now_main_thread = Thread(target=start_monitor)
        now_main_thread.start()


if __name__ == '__main__':
    # sql_lite_tools.create_table()
    # insert_data = ('监控测试4', 'wangyuquan@dhibank.com', '*/1 * * * *', 'select 4')
    # insert_data2 = ('监控测试2', 'wangyuquan@dhibank.com', '0 * * * *', 'select 2')
    # insert_data3 = ('监控测试3', 'wangyuquan@dhibank.com', '30 * * * *', 'select 3')
    # sql_lite_tools.execute_insert(insert_data)
    # sql_lite_tools.execute_insert(insert_data2)
    # sql_lite_tools.execute_insert(insert_data3)
    # print(get_next_execute())
    # while True:
    #     restart()
    #     time.sleep(5)

    # 直接发送邮件测试
    # item = MonitorItem({"cron_str": "0/5 * * * *", "next_time": "123", "title": "123",
    #                     "receiver": "wangyuquan@dhibank.com", "id": 5,
    #                     "sql_str": "select 1"})
    # m = Monitor(item)
    # m.start()
    pass
    print(execute((12,)))

