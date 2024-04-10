import json
import subprocess
import os
from  db.package_info_db_v2 import create_database
from  db.package_info_db_v2 import get_package_info

def get_default_pack(name, version=''):
    """
    获取默认的包信息。
    
    Args:
    name (str): 包名称
    version (str): 包版本
    
    Returns:
    dict: 默认的包信息字典
    """
    return { 
        'name': name,
        'version': version,
        'publishTime': '',   
        'author': '',  
        'integrity': ' ',
        'shasum': ' ',
        'license': '',
        'dependencies': '',
        'peerDependencies': '', 
    }

def build_package_info(name, package_data):
    """
    构建包信息字典。
    
    Args:
    name (str): 包名称
    package_data (dict): 包数据字典
    
    Returns:
    dict: 构建的包信息字典
    """
    version = package_data.get('version', '')

    # 获取特定版本的信息
    publish_time, author, dist_info, license = get_package_info(name, version) 

    peers = list(package_data.get('peerDependencies', {}).keys())
    deps = list(package_data.get('dependencies', {}).keys())
    
    package_info = { 
        'name': name,
        'version': version,
        'publishTime': publish_time,  
        'author': author,   
        'integrity': dist_info.get('integrity', ''),
        'shasum': dist_info.get('shasum', ''),
        'license': license,
        'dependencies': deps,
        'peerDependencies': peers,
    }

    print(f"Built package info for {name}: {package_info}")
    return package_info,peers

def parse_package_lock(package_lock_path, MAX_COUNT=0): 
    create_database()

    proDeps = []
    package_list = []
    peer_list = [] 
    package_map = {}

    with open(package_lock_path, 'r') as f:
        package_lock_data = json.load(f)

    count = 1
    for package_name, package_data in package_lock_data.get('packages', {}).items():
        if package_name == '':
            proDeps = list(package_data.get('dependencies', {}).keys())
            continue

        name = package_name.replace('node_modules/', '')
        isRoot =  True if name in proDeps else False

        if name not in package_map:
            package_map[name] = package_data

        if package_data.get('dev', False) is True:
            continue

        if not isRoot:
            continue

        package_info,peers = build_package_info(name, package_data)
        if peers:
            peer_list.extend(peers)

        package_list.append(package_info)

        count += 1
        if MAX_COUNT == 0:
            continue

        if count >= MAX_COUNT:
            break

    # 计算差异
    diff_list = list(set(peer_list) - set(proDeps))
    for diff in diff_list :
        package_data = package_map.get(diff, '')
        if package_data: 
            package_info,_ = build_package_info(diff, package_data)
        else:
            package_info = get_default_pack(diff, '')

        package_list.append(package_info)

    # 排序
    package_list = sorted(package_list, key=lambda x: x['name']) 

    return proDeps, package_list, package_map
