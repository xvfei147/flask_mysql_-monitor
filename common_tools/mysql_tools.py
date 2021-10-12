import pymysql
import pandas as pd


def get_conn_by_obj(args):
    return pymysql.Connection(host=args['host'], port=args['port'], user=args['username'], password=args['password'],
                              db=args['database'], charset='utf8')


def insert_update(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def execute_query(conn, sql):
    # print(sql)
    cursor = conn.cursor()
    cursor.execute(sql)
    result_list = list()
    for row in cursor.fetchall():
        result_list.append(row)
    return result_list


def execute_query_with_header(conn, sql):
    # print(sql)
    cursor = conn.cursor()
    cursor.execute(sql)
    col = cursor.description
    col_row = [c[0] for c in col]
    result_list = list()
    result_list.append(tuple(col_row))
    for row in cursor.fetchall():
        result_list.append(row)
    return result_list


def execute_df_query_with_header(conn, sql):
    # 根据sql查询mysql，返回列数据和列名
    cursor = conn.cursor()
    if 'limit' not in sql.lower():
        sql += ' limit 20'
    cursor.execute(sql)
    col = cursor.description
    header = []
    for i in range(len(col)):
        header.append(col[i][0])
    result = cursor.fetchall()
    df = pd.DataFrame(list(result), columns=header) if len(list(result)) > 0 else None
    return df


def execute_query_return_count(conn, sql):
    # 根据sql查询mysql，返回结果数量
    cursor = conn.cursor()
    count_sql = 'select count(*) from ({})c'.format(sql)
    cursor.execute(count_sql)
    row = cursor.fetchone()
    if row is not None and len(row) > 0:
        return row[0]
    else:
        return 0


def is_exist(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return True if rows is not None and len(rows) > 0 else False


def get_one(conn, sql):
    cursor = conn.cursor()
    # print(sql)
    cursor.execute(sql)
    rows = cursor.fetchone()
    if rows is not None and len(rows) > 0:
        return rows[0]
    else:
        return None


def test_conn(conn):
    try:
        get_conn_by_obj(conn)
        return "连接成功"
    except Exception as e:
        print(e)
        return e.args[1]


if __name__ == '__main__':
    args = {
        'host': '172.16.12.1',
        'port': 3306,
        'username': 'devroot',
        'password': 'devroot1',
        'database': 'winghead'
    }
    try:
        get_conn_by_obj(args)
        print("连接成功")
    except Exception as e:
        print(e.args[1])