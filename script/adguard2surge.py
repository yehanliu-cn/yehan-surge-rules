import requests
import re
import os

# AdGuard订阅链接文件
source_file = "source/custom/Advertising/source.list"

# 输出文件夹及路径
output_dir = "output"
output_file = os.path.join(output_dir, "surge.list")
os.makedirs(output_dir, exist_ok=True)

def adguard_to_surge(content):
    rules = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("!"):
            continue
        if line.startswith("||"):
            rule = "DOMAIN-SUFFIX," + line[2:].split("^")[0] + ",REJECT"
        elif line.startswith("http"):
            rule = "DOMAIN," + re.findall(r"https?://([^/]+)", line)[0] + ",REJECT"
        elif line.startswith("/") and line.endswith("/"):
            continue  # 忽略正则
        elif "*" in line:
            rule = "DOMAIN-SUFFIX," + line.replace("*", "") + ",REJECT"
        else:
            continue
        rules.append(rule)
    return "[Rule]\n" + "\n".join(rules)

def main():
    with open(source_file, "r") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    all_rules = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                converted = adguard_to_surge(response.text)
                all_rules.append(converted)
            else:
                print(f"请求失败: {url}")
        except Exception as e:
            print(f"错误: {url} - {e}")

    with open(output_file, "w") as f:
        f.write("\n".join(all_rules))

if __name__ == "__main__":
    main()
