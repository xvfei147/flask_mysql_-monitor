from common_tools.sql_lite_tools import SqlLite3Tools

# 监控创建sql
create_sql = '''
create table monitor 
(id integer primary key,
title varchar(100)  NOT NULL,
receiver varchar(200) NOT NULL,
cron_str varchar(10) NOT NULL,
sql_str text NOT NULL,
source varchar(20) NOT NULL
)
'''


def execute_save(insert_data):
    db = SqlLite3Tools(create_sql=create_sql)
    sql = 'insert into monitor (title,receiver,cron_str,sql_str,source) values (?,?,?,?,?)'\
        if len(insert_data) == 5 \
        else 'update monitor set title= ? ,receiver=?,cron_str=?,sql_str=?,source=? where id = ?'
    db.execute_save(sql, insert_data)


def execute_delete(_id):
    db = SqlLite3Tools()
    db.execute_delete('monitor', _id)


def query_all():
    db = SqlLite3Tools(create_sql=create_sql)
    rows = db.query_all("monitor")
    result = list()
    if rows:
        for row in rows:
            item = {
                'id': row[0],
                'title': row[1],
                'receiver': row[2],
                'cron_str': row[3],
                'sql_str': row[4],
                'source': row[5]
            }
            result.append(item)
    return result


def query_one(_id):
    db = SqlLite3Tools()
    row = db.query_one("monitor", _id)
    item = {
        'id': row[0],
        'title': row[1],
        'receiver': row[2],
        'cron_str': row[3],
        'sql_str': row[4],
        'source': row[5]
    }
    return item


if __name__ == '__main__':
    a = (1, 2, 3, 4, 5)
    print(len(a))
