import json
import logging

# 设置日志记录
logging.basicConfig(level=logging.ERROR)

def load_report(json_file):
    try:
        with open(json_file, 'r', encoding='utf-16') as f:
            return json.load(f)
    except (UnicodeDecodeError, json.JSONDecodeError):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"读取 JSON 报告时出错: {e}")
            return None
    except Exception as e:
        logging.error(f"读取 JSON 报告时出错: {e}")
        return None

# 转换报告为 DataFrame 
def create_dataframe(report):
    data = {}

    for item in report.get('data', []):
        for result in item.get('results', []):
            component = result.get('component', '未知')
            version = result.get('version', '未知')
            vulnerabilities = result.get('vulnerabilities', [])

            for vulnerability in vulnerabilities:
                severity = vulnerability.get("severity", "未知")
                is_acceptable = "No" if severity in ["high", "critical"] else "Yes"
                reason_for_acceptability = (
                    "Severity is low or moderate" if severity in ["low", "moderate"] else "Critical vulnerability"
                )

                row = {  
                    'Vulnerable': True,
                    "Acceptable": is_acceptable,
                    'Vulnerability Details': vulnerability.get('identifiers', {}).get('summary', '无'),
                    'CVE': ', '.join(vulnerability.get('identifiers', {}).get('CVE', [])),
                    'CWE': ', '.join(vulnerability.get('cwe', [])),
                    'Severity': severity,
                    'Recommend Version': vulnerability.get('below', '无'),
                    "Reason for Acceptability": reason_for_acceptability
                }

                if component not in data:
                    data[component] = []  # 使用列表来保存多个漏洞信息
                data[component].append(row)  # 直接添加行信息

    return data

def parse_retire_report(file_path):  
    report = load_report(file_path)
    if report:  
        df = create_dataframe(report)
        return df
    else:
        return {}
