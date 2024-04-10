import sqlite3
import subprocess
import json
import os

def create_database(database_path):
    # 创建一个 SQLite 数据库连接
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    # 创建表格用于存储包名、版本和发布时间信息
    c.execute('''CREATE TABLE IF NOT EXISTS packages
                 (name TEXT, version TEXT, publish_time TEXT)''')
    conn.commit()
    conn.close()

def get_package_publish_time_from_database(package_name, package_version, database_path):
    # 尝试从数据库中获取包的发布时间
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    c.execute("SELECT publish_time FROM packages WHERE name=? AND version=?", (package_name, package_version))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_package_publish_time(package_name, package_version):
    # 尝试从数据库中获取包的发布时间
    publish_time = get_package_publish_time_from_database(package_name, package_version, 'packages.db')
    if publish_time:
        return publish_time

    # 如果本地数据库中不存在，则从 npm 服务器上获取
    command = f"npm view {package_name}@{package_version} time --json"
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        package_time = json.loads(output)
        publish_time = package_time.get(package_version)
        if publish_time is None:
            raise ValueError(f"Package '{package_name}' version '{package_version}' publish time not found.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to retrieve package '{package_name}' information from npm.") from e
    except (json.JSONDecodeError, KeyError):
        raise RuntimeError(f"Failed to parse package '{package_name}' information.") from None

    # 将获取到的发布时间存入数据库
    conn = sqlite3.connect('packages.db')
    c = conn.cursor()
    c.execute("INSERT INTO packages (name, version, publish_time) VALUES (?, ?, ?)", (package_name, package_version, publish_time))
    conn.commit()
    conn.close()

    return publish_time

# 创建数据库（如果不存在）
create_database('packages.db')

# 测试获取指定版本的发布时间
package_name = "@0no-co/graphql.web"
package_version = "1.0.4"
publish_time = get_package_publish_time(package_name, package_version)
print(f"The publish time of {package_name}@{package_version} is: {publish_time}")
