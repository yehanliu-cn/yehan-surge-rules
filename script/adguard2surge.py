import os
import re

# 源规则列表文件路径
source_file = "source/custom/Advertising/source.list"

# 输出路径
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "surge.list")  # 生成 .list 文件而非 .txt

def adguard_to_surge(content):
    rules = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("!") or line.startswith("["):
            continue  # 跳过注释和空行

        # DOMAIN-SUFFIX
        if line.startswith("||"):
            domain = line[2:].split("^")[0]
            rules.append(f"DOMAIN-SUFFIX,{domain},REJECT")
        # DOMAIN
        elif line.startswith("http"):
            domains = re.findall(r"https?://([^/]+)", line)
            for d in domains:
                rules.append(f"DOMAIN,{d},REJECT")
        # 通配符域名，尝试简化为 DOMAIN-SUFFIX
        elif "*" in line:
            domain = line.replace("*", "")
            if domain:
                rules.append(f"DOMAIN-SUFFIX,{domain},REJECT")
    return rules

# 读取源文件
with open(source_file, "r", encoding="utf-8") as f:
    content = f.read()

# 转换规则格式
rules = adguard_to_surge(content)

# 写入 Surge 格式 .list 文件（无 [Rule] 头）
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(rules))
