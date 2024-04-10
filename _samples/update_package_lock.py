import json
import subprocess
import os

def get_package_publish_time(package_name):
    # 使用npm view命令获取包的发布时间
    command = f"npm view {package_name} time --json"
    output = subprocess.check_output(command, shell=True, text=True)
    package_time = json.loads(output)
    
    # 获取最新版本的发布时间
    latest_version = package_time['dist-tags']['latest']
    publish_time = package_time['time'][latest_version]

    return publish_time

def update_package_lock(package_name, publish_time):
    # 读取并解析package-lock.json文件
    with open('package-lock.json', 'r') as file:
        package_lock = json.load(file)

    # 将包的发布时间添加到package-lock.json文件中
    package_lock.setdefault('packages', {})
    package_lock['packages'].setdefault(package_name, {})
    package_lock['packages'][package_name]['publish_time'] = publish_time

    # 将更新后的package-lock.json写回文件
    with open('package-lock.json', 'w') as file:
        json.dump(package_lock, file, indent=2)

def get_package_publish_time(package_name, package_version):
    # 使用npm view命令获取包的发布时间
    command = f"npm view {package_name}@{package_version} time --json"
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        package_time = json.loads(output)
        # 获取特定版本的发布时间
        publish_time = package_time.get(package_version)
        if publish_time is None:
            raise ValueError(f"Package '{package_name}' version '{package_version}' publish time not found.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to retrieve package '{package_name}' information from npm.") from e
    except (json.JSONDecodeError, KeyError):
        raise RuntimeError(f"Failed to parse package '{package_name}' information.") from None

    return publish_time

# 测试获取指定版本的发布时间
package_name = "@0no-co/graphql.web"
package_version = "1.0.4"
publish_time = get_package_publish_time(package_name, package_version)
print(f"The publish time of {package_name}@{package_version} is: {publish_time}")


if __name__ == "__main__":
    package_name = 'your-package-name'  # 替换成你的包名
    publish_time = get_package_publish_time(package_name)
    update_package_lock(package_name, publish_time)
