import json
import urllib.request

import json
import urllib.request

def get_author_info(package_info):
    author = package_info.get('_npmUser')
    if author:
        return author
    maintainers = package_info.get('maintainers', [])
    if maintainers:
        return maintainers[0]  # 按顺序先找到则返回第一个维护者信息
    return None

def format_author_info(author_info):
    if not author_info:
        return "Unknown"
    elif isinstance(author_info, dict):
        name = author_info.get('name', 'Unknown')
        email = author_info.get('email', '')
        if email:
            return f"{name} <{email}>"
        else:
            return name
    elif isinstance(author_info, list):
        formatted_authors = []
        for author in author_info:
            formatted_author = format_author_info(author)
            formatted_authors.append(formatted_author)
        return ', '.join(formatted_authors)
    else:
        return "Unknown"


def get_package_info(package_name, package_version):
    url = f"https://registry.npmjs.org/{package_name}/{package_version}"
    try:
        print(f"Fetching package '{package_name}@{package_version}' information from: {url}")
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            print(f"Retrieved data: {data}")
            author = data.get('author')
            if author:
                return author
            else:
                return "Unknown"
    except Exception as e:
        print(f"Failed to retrieve package '{package_name}@{package_version}' information: {e}")
        return None

# 测试获取指定版本的包的作者信息
packages = [
    {"name": "qs", "version": "6.10.1"},
    # {"name": "react", "version": "16.14.0"},
    # {"name": "react-dom", "version": "16.14.0"},
    # {"name": "react-native", "version": "0.64.2"},
    # {"name": "socket.io-client", "version": "4.7.2"}
]

for package in packages:
    author = get_package_info(package["name"], package["version"])
    if author:
        print(f"The author of package '{package['name']}' version '{package['version']}' is: {author}")
    else:
        print(f"Failed to retrieve author information for package '{package['name']}' version '{package['version']}'.")


# def get_package_author(package_name):
#     url = f"https://registry.npmjs.org/{package_name}"
#     try:
#         print(f"Fetching package '{package_name}' information from: {url}")
#         with urllib.request.urlopen(url) as response:
#             data = json.load(response)
#             print(f"Retrieved data: {data}")
#             author = data.get('author')
#             if author:
#                 return author
#             else:
#                 return "Unknown"
#     except Exception as e:
#         print(f"Failed to retrieve package '{package_name}' information: {e}")
#         return None

# # 测试获取指定包的作者信息
# # packages = ["qs", "react", "react-dom", "react-native", "socket.io-client"]
# packages = ["qs"]
# for package in packages:
#     author = get_package_author(package)
#     if author:
#         print(f"The author of package '{package}' is: {author}")
#     else:
#         print(f"Failed to retrieve author information for package '{package}'.")
