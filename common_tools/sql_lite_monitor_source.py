from common_tools.sql_lite_tools import SqlLite3Tools

# 数据源创建sql
create_sql = '''
    CREATE TABLE source_config
(
    id integer PRIMARY KEY AUTOINCREMENT,
    name varchar(30) NOT NULL,
    host varchar(50) NOT NULL,
    port integer DEFAULT 3306,
    username varchar(30) NOT NULL,
    password varchar(30) NOT NULL,
    database varchar(30) NOT NULL,
    UNIQUE KEY `name` (`name`),
)
'''


# 插入数据时如果无该表则新建
def execute_save(insert_data):
    db = SqlLite3Tools(create_sql=create_sql)
    sql = 'insert into source_config (name,host,port,username,password,database) values (?,?,?,?,?,?)'\
        if len(insert_data) == 6 \
        else 'update source_config set name= ? ,host=?,port=?,username=?,password=?,database=? where id = ?'
    db.execute_save(sql, insert_data)


def execute_delete(_id):
    db = SqlLite3Tools()
    db.execute_delete('source_config', _id)


def query_all():
    db = SqlLite3Tools(create_sql=create_sql)
    rows = db.query_all("source_config")
    result = list()
    if rows:
        for row in rows:
            item = {
                'id': row[0],
                'name': row[1],
                'host': row[2],
                'port': row[3],
                'username': row[4],
                'password': row[5],
                'database': row[6]
            }
            result.append(item)
    return result


def query_one(_id):
    db = SqlLite3Tools()
    row = db.query_one("source_config", _id)
    item = {
        'id': row[0],
        'name': row[1],
        'host': row[2],
        'port': row[3],
        'username': row[4],
        'password': row[5],
        'database': row[6]
    }
    return item


def query_by_name(name):
    db = SqlLite3Tools()
    row = db.query_by_sql("select * from source_config where name = '%s'" % name)
    if len(row) > 0:
        row = row[0]
        item = {
            'id': row[0],
            'name': row[1],
            'host': row[2],
            'port': row[3],
            'username': row[4],
            'password': row[5],
            'database': row[6]
        }
        return item
    else:
        return None


if __name__ == '__main__':
    pass
