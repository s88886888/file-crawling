import sqlite3


class Sqlite3ToolSql:

    def __init__(self, filename="telegram_data"):
        self.filename = filename + ".db"
        self.db = sqlite3.connect(self.filename)

    def __exit__(self):
        self.db.cursor().close()
        self.db.close()

    def execute(self, sql: str, commit: bool = False) -> any:
        try:
            _db = self.db.cursor()
            # 执行SQL获取结果
            _db.execute(sql)
            if commit:
                self.db.commit()
            data = _db.fetchall()
            _db.close()
            return data
        except Exception as e:
            print(f"执行 SQL 语句出错：{e}")
            self.db.rollback()
            raise e

    def crateDataBase(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS key_data(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_key TEXT,
                create_time DATETIME,
                num INTEGER
            )
        '''

        self.execute(sql, True)
        print("初始化数据库成功")


if __name__ == '__main__':
    db = Sqlite3ToolSql()
    db.__init__()
    db.crateDataBase()
