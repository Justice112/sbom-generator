import json
from db.npm_package_info_db import create_database, get_package_info

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
        'npmUser': '',  
        'integrity': ' ',
        'shasum': ' ',
        'license': '',
        'dependencies': [],
        'peerDependencies': [], 
    }
    
def get_valid_author(author, npm_user): 
    valid_fields = [author, npm_user]
    for field in valid_fields:
        if field:
            return field
    return ''

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
    publish_time, author, npm_user,  dist_info, license = get_package_info(name, version) 

    peers = list(package_data.get('peerDependencies', {}).keys())
    deps = list(package_data.get('dependencies', {}).keys())
    
    validAuthor = get_valid_author(author,npm_user)
    
    package_info = { 
        'name': name,
        'version': version,
        'publishTime': publish_time,  
        'author': validAuthor,   
        'npmUser': npm_user,   
        'integrity': dist_info.get('integrity', ''),
        'shasum': dist_info.get('shasum', ''),
        'license': license,
        'dependencies': deps,
        'peerDependencies': peers,
    }

    return package_info, peers

def parse_package_lock(package_lock_path, max_count=0): 
    """解析 package-lock.json 文件并构建包信息列表。

    Args:
        package_lock_path (str): package-lock.json 文件的路径。
        max_count (int, optional): 解析的最大包数。默认为 0，表示解析全部。

    Returns:
        tuple: 一个元组，包含三个元素：
            - pro_deps (list): 项目依赖的包列表。
            - package_list (list): 构建的包信息列表。
            - package_map (dict): 包名称到包数据的映射字典。
    """
    create_database()

    pro_deps = []
    package_list = []
    peer_list = [] 
    package_map = {}

    with open(package_lock_path, 'r') as f:
        package_lock_data = json.load(f)

    count = 1
    for package_name, package_data in package_lock_data.get('packages', {}).items():
        if package_name == '':
            pro_deps = list(package_data.get('dependencies', {}).keys())
            continue

        name = package_name.replace('node_modules/', '')
        is_root = True if name in pro_deps else False

        if name not in package_map:
            package_map[name] = package_data

        if package_data.get('dev', False) is True:
            continue

        if not is_root:
            continue

        package_info, peers = build_package_info(name, package_data)
        if peers:
            peer_list.extend(peers)

        package_list.append(package_info)

        count += 1
        if max_count == 0:
            continue

        if count >= max_count:
            break

    diff_list = list(set(peer_list) - set(pro_deps))
    peers_not_exists = []
    for diff in diff_list:
        package_data = package_map.get(diff, '')
        if package_data: 
            package_info, _ = build_package_info(diff, package_data)
            package_list.append(package_info)
        else:
            peers_not_exists.append(diff)

    if len(peers_not_exists) > 0:
        print(f"peers_not_exists: {','.join(peers_not_exists)}")

    package_list = sorted(package_list, key=lambda x: x['name']) 

    return pro_deps, package_list, package_map
