import requests

def get_publish_time(package_name, package_version):
    url = 'http://localhost:5000/publish_time'
    params = {'name': package_name, 'version': package_version}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('publish_time')
    else:
        print(f"Failed to get publish time for package '{package_name}' version '{package_version}'.")
        return None

# 测试获取指定包名和版本的发布时间
package_name = "@0no-co/graphql.web"
package_version = "1.0.4"
publish_time = get_publish_time(package_name, package_version)
if publish_time:
    print(f"The publish time of {package_name}@{package_version} is: {publish_time}")
