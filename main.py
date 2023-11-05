import datetime
import json
import os
import re
import sys
import time
import uuid

from Sqlite3Tool import Sqlite3ToolSql

key_pattern = r'[a-zA-Z0-9\-\_]{40,}'
pattern = r"^(vi_|p_)"


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
        if re.match(key_pattern, s):
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
                print("输入的路径有误,请重新运行")
                time.sleep(3)
                sys.exit()
    else:
        print("检测数据库丢失")
        time.sleep(10)
        sys.exit()


def data_pk():
    with open(output_file.name, 'r') as file_read:
        lines = file_read.readlines()
    # 过滤符合规则的行并分组
    groups = []
    current_group = []
    with open(f"./restfulFile/pk_file_{get_current_time()}.txt", 'a', encoding='utf8') as file:
        for line in lines:
            if re.match(pattern, line):
                current_group.append(line.strip())
                if len(current_group) == 25:
                    groups.append(current_group)
                    current_group = []
            else:
                file.writelines(line)
        file.writelines("\n")

        current_group_pk = []
        for group in groups:
            val = "".join(group)
            current_group_pk.append(val)

        for cs in current_group_pk:
            file.writelines("/pk" + " " + cs + "\n")

        file.writelines("/pk" + " " + "\n".join(current_group) + "\n")


# D:\dataKey\ChatExport_2023-10-31 (1)\blg2023-10-31-0113.json

if __name__ == '__main__':
    read_file_path = check_database()
    db = Sqlite3ToolSql()
    try:
        db.__init__()
        with open(read_file_path, 'r', encoding='utf8') as json_file:
            data = json.load(json_file)['messages']
            output_file = open(f"./restfulFile/file_{get_current_time()}.txt", 'a', encoding='utf8')
            for index, value in enumerate(data):
                if letters(data[index]['text']):
                    keys = re.findall(key_pattern, data[index]['text'])
                    for key in keys:
                        sql = f"SELECT file_key, num FROM key_data WHERE file_key = '{key}'"
                        if len(db.execute(sql, True)) == 0:
                            sql = insert_key_data(key, db)
                            output_file.writelines(key + "\n")
                        else:
                            sql = update_key_data(key, db)
                            output_file.writelines(key + "\n")
                        print(f"[{index}/{len(data)}/{int((index / len(data)) * 100)}%]:{sql}")

        print("已经生成新的数据文件，10秒后自动关闭...")
    except Exception as e:
        print(f"发生错误：{str(e)}")
    finally:
        db.__exit__()
        data_wailk()
        if 'output_file' in locals():
            output_file.close()
        if 'json_file' in locals():
            json_file.close()
        time.sleep(1)
