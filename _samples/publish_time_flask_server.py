from flask import Flask, request, jsonify
import sqlite3
import subprocess
import json

app = Flask(__name__)

def create_database(database_path):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS packages
                 (name TEXT, version TEXT, publish_time TEXT)''')
    conn.commit()
    conn.close()

def get_package_publish_time_from_database(package_name, package_version, database_path):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    c.execute("SELECT publish_time FROM packages WHERE name=? AND version=?", (package_name, package_version))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_package_publish_time(package_name, package_version):
    publish_time = get_package_publish_time_from_database(package_name, package_version, 'packages.db')
    if publish_time:
        return publish_time

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

    conn = sqlite3.connect('packages.db')
    c = conn.cursor()
    c.execute("INSERT INTO packages (name, version, publish_time) VALUES (?, ?, ?)", (package_name, package_version, publish_time))
    conn.commit()
    conn.close()

    return publish_time

@app.route('/publish_time', methods=['GET'])
def get_publish_time():
    package_name = request.args.get('name')
    package_version = request.args.get('version')
    if not package_name or not package_version:
        return jsonify({'error': 'Package name and version are required.'}), 400

    publish_time = get_package_publish_time(package_name, package_version)
    return jsonify({'name': package_name, 'version': package_version, 'publish_time': publish_time})

if __name__ == '__main__':
    create_database('packages.db')
    app.run(debug=True)
