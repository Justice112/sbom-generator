import requests

def get_author_info(package_name, version):
    url = f"https://registry.npmjs.org/{package_name}/{version}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'author' in data:
            author_info = data['author']
            return author_info
        else:
            return "作者信息未找到"
    except Exception as e:
        return f"发生错误: {e}"

if __name__ == "__main__":
    package_name = "axios"
    version = "0.21.1"  # 你要查询的版本号
    author_info = get_author_info(package_name, version)
    print(author_info)
