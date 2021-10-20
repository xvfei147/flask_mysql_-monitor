from common_tools import sql_lite_monitor_source


def get_all():
    rows = sql_lite_monitor_source.query_all()
    result = {
        'rows': rows,
        'total': len(rows)
    }
    return result


def delete(_id):
    try:
        sql_lite_monitor_source.execute_delete(_id)
        return 'success'
    except Exception as e:
        return e


# 保存  需要保证顺序 title,receiver,cron_str,sql_str
def save(form):
    try:
        name = form['name']
        host = form['host']
        port = form['port']
        username = form['username']
        password = form['password']
        database = form['database']
        _id = form['id']
        item = (name, host, port, username, password, database) if len(_id) == 0\
            else (name, host, port, username, password, database, _id)
        sql_lite_monitor_source.execute_save(item)
        return 'success'
    except Exception as e:
        return e


def test_conn(form):
    args = {
        'host': form['host'],
        'port': int(form['port']),
        'username': form['username'],
        'password': form['password'],
        'database': form['database']
    }
    from common_tools import mysql_tools
    return mysql_tools.test_conn(args)


if __name__ == '__main__':
    # sql_lite_tools.create_table()
    # insert_data = ('监控测试4', 'wangyuquan@dhibank.com', '*/1 * * * *', 'select 4')
    # insert_data2 = ('监控测试2', 'wangyuquan@dhibank.com', '0 * * * *', 'select 2')
    # insert_data3 = ('监控测试3', 'wangyuquan@dhibank.com', '30 * * * *', 'select 3')
    # sql_lite_tools.execute_insert(insert_data)
    # sql_lite_tools.execute_insert(insert_data2)
    # sql_lite_tools.execute_insert(insert_data3)
    pass

