import requests
import re
import os

# 你的AdGuard订阅列表文件
source_file = "source/custom/Advertising/source.list"

# Surge输出文件夹
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def adguard_to_surge(content):
    rules = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("!"):
            continue
        if line.startswith("||"):
            rule = "DOMAIN-SUFFIX," + line[2:].split("^")[0] + ",REJECT"
        elif line.startswith("|http"):
            rule = "DOMAIN," + re.findall(r"https?://([^/^$]+)", line)[0] + ",REJECT"
        elif line.startswith("/"):
            continue  # 忽略正则
        elif "*" in line:
            continue  # 忽略通配符
        elif "." in line:
            rule = "DOMAIN-SUFFIX," + line.replace("^", "") + ",REJECT"
        else:
            continue
        rules.append(rule)
    return "\n".join(rules)

with open(source_file, "r", encoding="utf-8") as f:
    for url in f:
        url = url.strip()
        if not url or url.startswith("#"):
            continue
        print("downloading", url)
        resp = requests.get(url)
        rules = adguard_to_surge(resp.text)
        name = url.split("/")[-1].split("?")[0]
        if not name:
            name = "result.txt"
        out_path = os.path.join(output_dir, f"{name}.surge.conf")
        with open(out_path, "w", encoding="utf-8") as outf:
            outf.write(rules)
        print(f"written: {out_path}")
