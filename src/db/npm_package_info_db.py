import subprocess
import json
import sqlite3
from datetime import datetime
DATABASE_PATH = 'npm_package_info_db.db'

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

def get_package_info_from_database(package_name, package_version):
    """
    从数据库中获取包信息。
    
    Args:
        package_name (str): 包名称
        package_version (str): 包版本
    
    Returns:
        tuple: 发布时间、作者、分发信息、许可证
    """
    result = execute_query("SELECT publish_time, author, maintainers, npm_user, contributors, dist_info, license FROM packages WHERE name=? AND version=?", (package_name, package_version), fetchone=True)
    if result: 
        publish_time, author, maintainers, npm_user, contributors, dist_info, license = result 
        print(f"{package_name}@{package_version} 信息从数据库中读取成功")
        
        return publish_time, author, npm_user, json.loads(dist_info), json.loads(license)

    return None

def validate_package_info(package_info,package_name,package_version):
    """
    验证包信息是否有效。并返回包信息
    
    Args:
        package_info (): 包信息
        package_version (str): 包版本
        
    
    Returns:
        is_valid (bool): 包信息是否有效
        author (str): 包名称
        package_version (str): 包版本
        publish_time (str): 发布时间
        dist_info (str): 分发信息
        license (str): 许可证
        command (str): npm命令
    """
    
    publish_time = package_info.get('time', {}).get(package_version)
    author = package_info.get('author', '')
    maintainers = package_info.get('maintainers', [])
    npm_user = package_info.get('_npmUser', '')
    contributors = package_info.get('contributors', [])
    dist_info = package_info.get('dist', {})
    license = package_info.get('license', '')
    
    is_valid = True

    if publish_time is None:
        print(f"Package '{package_name}' version '{package_version}' publish time not found.")
        is_valid = False

    if dist_info is None:
        print(f"Package '{package_name}' version '{package_version}' dist_info found.")
        is_valid = False

    if license is None:
        print(f"Package '{package_name}' version '{package_version}' license found.")
        is_valid = False

    if is_valid:
        print(f"{package_name}@{package_version} 信息获取完成") 
        
    return is_valid,publish_time,author,maintainers,npm_user,contributors, dist_info, license 


def get_package_info_from_npm(package_name, package_version):
    """
    从npm获取包信息。
    
    Args:
        package_name (str): 包名称
        package_version (str): 包版本
    
    Returns:
        tuple: 发布时间、作者、分发信息、许可证
    """
    command = f"npm view {package_name}@{package_version} time author maintainers _npmUser contributors dist license --json"
    try:
        print(f"正在获取{package_name}@{package_version}信息...")
        output = subprocess.check_output(command, shell=True, text=True)
        package_info = json.loads(output)
        
        is_valid,publish_time,author,maintainers,npm_user,contributors, dist_info, license = validate_package_info(package_info,package_name,package_version)
        
        if is_valid is True:
            # 存储到数据库中 
            execute_query("INSERT INTO packages (name, version, publish_time, author, maintainers, npm_user, contributors, dist_info, license) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (package_name, package_version, publish_time, author, json.dumps(maintainers),  npm_user, json.dumps(contributors), json.dumps(dist_info), json.dumps(license))) 
 
            return publish_time, author, npm_user, dist_info, license
        
    except Exception as e:
        print(f"Failed to retrieve or process package '{package_name}' information: {e}")
        publish_time = datetime.now().isoformat()
        author = npm_user = license = maintainers= contributors = dist_info = ''

    return publish_time, author, npm_user, json.loads(dist_info), license

def get_package_info(package_name, package_version):
    """
    获取包信息，优先从数据库中获取，若数据库中不存在则从npm获取。
    
    Args:
        package_name (str): 包名称
        package_version (str): 包版本
    
    Returns:
        tuple: 发布时间、作者、分发信息、许可证
    """
    package_info = get_package_info_from_database(package_name, package_version)
    if package_info:
        return package_info

    return get_package_info_from_npm(package_name, package_version)

