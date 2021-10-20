import sqlite3


class SqlLite3Tools:
    def __init__(self, db='monitor.db', create_sql=None):
        self.db = db
        self.conn = sqlite3.connect(db)
        self.create_sql = create_sql

    def get_conn(self):
        self.conn = sqlite3.connect(self.db)

    def create_table(self):
        """
        monitor:
        create table monitor (id integer primary key,title varchar(100)  NOT NULL,receiver varchar(200)
         NOT NULL,cron_str varchar(10) NOT NULL, sql_str text NOT NULL,source varchar(20) NOT NULL )
        :return:
        """
        self.get_conn()
        self.conn.execute(self.create_sql)
        self.conn.commit()
        self.conn.close()

    # 插入数据时如果无该表则新建
    def execute_save(self, sql, save_data):
        try:
            self.get_conn()
            # sql = 'insert into monitor (title,receiver,cron_str,sql_str,source) values (?,?,?,?,?)'\
            #     if len(insert_data) == 5 \
            #     else 'update monitor set title= ? ,receiver=?,cron_str=?,sql_str=?,source=? where id = ?'
            self.conn.execute(sql, save_data)
            self.conn.commit()
            self.conn.close()
        except sqlite3.OperationalError:
            self.create_table()
            self.execute_save(sql, save_data)

    def execute_delete(self, table, ids):
        self.get_conn()
        # 按照参数个数  拼接对应个数的占位符
        sql_args = ('?,' * len(ids))[:-1]
        sql = 'delete from %s where id in (%s) ' % (table, sql_args)
        self.conn.execute(sql, ids)
        self.conn.commit()
        self.conn.close()

    def query_all(self, table):
        try:
            self.get_conn()
            sql = 'select * from %s' % table
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            self.conn.close()
            return result
        except sqlite3.OperationalError:
            self.create_table()
            return None

    def query_one(self, table, _id):
        self.get_conn()
        sql = 'select * from %s where id = ?' % table
        cursor = self.conn.cursor()
        cursor.execute(sql, _id)
        row = cursor.fetchone()
        self.conn.close()
        return row

    def query_by_sql(self, sql):
        self.get_conn()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        self.conn.close()
        return rows


if __name__ == '__main__':
    db_tools = SqlLite3Tools()
    print(db_tools.query_one('monitor', '5'))
