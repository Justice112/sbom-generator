import subprocess
import json
import sqlite3
from datetime import datetime
DATABASE_PATH = 'db/packages_v2.db'

def create_database(): 
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS packages
                     (name TEXT, version TEXT, publish_time TEXT, author TEXT, maintainers TEXT, npm_user TEXT, contributors TEXT, dist_info TEXT, license TEXT)''')

def execute_query(query, params=(), fetchone=False):
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        if fetchone:
            return c.fetchone()

def get_valid_author(author, maintainers, npm_user, contributors):
    valid_fields = [author, npm_user,maintainers, contributors]
    for field in valid_fields:
        if field: 
            if isinstance(field, (list, tuple)):
                return ', '.join(field)
            else:
                return field
    return ''


def get_package_info(package_name, package_version):
    # 获取数据库中的信息
    result = execute_query("SELECT publish_time, author, maintainers, npm_user, contributors, dist_info, license FROM packages WHERE name=? AND version=?", (package_name, package_version), fetchone=True)
    if result: 
        publish_time, author, maintainers, npm_user, contributors, dist_info, license = result
        author = get_valid_author(author, json.loads(maintainers), json.loads(npm_user), json.loads(contributors))

        return publish_time, author, json.loads(dist_info), json.loads(license)

    # 如果数据库中没有，则从 npm 获取
    command = f"npm view {package_name}@{package_version} time author maintainers _npmUser contributors dist license --json"
    try:
        print(f"正在获取{package_name}@{package_version}信息...")
        output = subprocess.check_output(command, shell=True, text=True)
        package_info = json.loads(output)
        publish_time = package_info.get('time', {}).get(package_version)
        author = package_info.get('author', '')
        maintainers = package_info.get('maintainers', '')
        npm_user = package_info.get('_npmUser', '')
        contributors = package_info.get('contributors', '')
        dist_info = package_info.get('dist', '')
        license = package_info.get('license', '')
        print(f"{package_name}@{package_version} 信息获取完成")
        if publish_time is None:
            print(f"Package '{package_name}' version '{package_version}' publish time not found. command:{command}")
    except Exception as e:
        print(f"Failed to retrieve or process package '{package_name}' information: {e}")
        publish_time = datetime.now().isoformat()
        author = maintainers = npm_user = contributors = dist_info = license = ''

    # 存储到数据库中 
    execute_query("INSERT INTO packages (name, version, publish_time, author, maintainers, npm_user, contributors, dist_info, license) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (package_name, package_version, publish_time, author, json.dumps(maintainers), json.dumps(npm_user), json.dumps(contributors), json.dumps(dist_info), json.dumps(license))) 

    author= get_valid_author(author, maintainers, npm_user, contributors)

    return publish_time, author, dist_info, license
