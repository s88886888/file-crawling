import datetime
import json
import os
import re
import sys
import time
import uuid

from Sqlite3Tool import Sqlite3ToolSql

KEY_PATTERN = r'[a-zA-Z0-9\-\_]{40,}'


def get_current_time():
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y-%m-%d_%H-%M-%S")


def generate_unique_id():
    return str(uuid.uuid4())


def letters(s):
    s = str(s)
    if s == '':
        return False
    else:
        if re.match(KEY_PATTERN, s):
            return True
        else:
            return False


def insert_key_data(key, db):
    sql = f"INSERT INTO key_data (`file_key`, `create_time`, `num`) VALUES ('{key}', '{datetime.datetime.now()}', 1)"
    db.execute(sql, False)
    return sql


def update_key_data(key, db):
    sql = f"UPDATE key_data SET num = num + 1 WHERE file_key = '{key}'"
    db.execute(sql, False)
    return sql


def check_database():
    if os.path.exists("telegram_data.db"):
        user_input: str = input("请选择输入读取的文件（输入'exit'退出）: ")
        if user_input == 'exit':
            print("程序停止")
            time.sleep(10)
            sys.exit()
        else:
            if os.path.exists(f"{user_input}"):
                return user_input
            else:
                print("输入的路径有误")
                time.sleep(3)
                sys.exit()
    else:
        print("检测数据库丢失")
        time.sleep(10)
        sys.exit()


if __name__ == '__main__':
    # pyinstaller --console --onefile.txt
    # file_path = './user.config'
    # if os.path.exists(file_path):
    #     print("检测配置存在")
    #     with open(file_path, 'r', encoding='utf8') as file:
    #         user_config = file.read()
    # else:
    #     with open(file_path, 'w', encoding='utf8') as file:
    #         while True:
    #             # 获取用户输入
    #             print(
    #                 "请选择使用存储的方式：1.mysql(开源，免费，需要安装) 2.⭐sqlite3 (不需要下载安装，人走库还在，一库传三代)")
    #             user_input = input("请输入内容（输入 'exit' 退出）: ")
    #             if user_input == 'exit':
    #                 print("无效输入")
    #                 break
    #             else:
    #                 file.write(user_input + '\n')
    #                 user_config = user_input
    #                 break
    #         file.close()
    #
    # if user_config == '1\n':
    #     db = MysqlTool()
    # else:
    #     db = Sqlite3ToolSql()
    #     # db.crateDataBase()

    # 爬取文件的名称
    # read_file_path = r'./readFile/blg-2023-10-30-0138.json'

    read_file_path = check_database()
    db = Sqlite3ToolSql()
    db.__init__()
    with open(read_file_path, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)['messages']
        output_file = open(f"./restfulFile/file_{get_current_time()}.txt", 'a', encoding='utf8')
        for index, value in enumerate(data):
            if letters(data[index]['text']):
                keys = re.findall(KEY_PATTERN, data[index]['text'])
                for key in keys:
                    sql = f"SELECT file_key, num FROM key_data WHERE file_key = '{key}'"
                    if len(db.execute(sql, True)) == 0:
                        sql = insert_key_data(key, db)
                        output_file.writelines(key + "\n")
                    else:
                        sql = update_key_data(key, db)
                print(f"[{index}/{len(data)}/{int((index / len(data)) * 100)}%]:{sql}")
        output_file.close()
    json_file.close()
    print("已经生成新的数据文件，10秒后自动关闭...")
    time.sleep(10)
    db.__exit__()
