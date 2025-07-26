import os
import requests

# 一定要和你仓库里的路径一致！
SOURCE_LIST = "source/custom/Advertising/source.list"
OUTPUT_FILE = "output/surge.list"

def fetch_and_convert(url):
    """下载单个 AdGuard 规则，并转成 Surge 格式"""
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"❌ 下载失败 {url}: {e}")
        return []

    out = []
    for line in r.text.splitlines():
        line = line.strip()
        if not line or line.startswith(("!", "#", "[")):
            continue
        if line.startswith("||"):
            domain = line[2:].split("^")[0]
            out.append(f"DOMAIN-SUFFIX,{domain},REJECT")
        elif line.startswith("|") and line.endswith("|"):
            host = line[1:-1]
            out.append(f"DOMAIN,{host},REJECT")
        elif line.startswith("/"):
            regex = line.strip("/").replace("\\/", "/")
            out.append(f"URL-REGEX,{regex},REJECT")
        else:
            out.append(f"DOMAIN-SUFFIX,{line},REJECT")
    return out

def main():
    # 检查 source.list 是否存在
    if not os.path.isfile(SOURCE_LIST):
        print(f"❌ 找不到订阅源文件：{SOURCE_LIST}")
        return

    # 读取所有订阅链接
    with open(SOURCE_LIST, encoding="utf-8") as f:
        urls = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    all_rules = []
    for u in urls:
        print(f"🔄 处理：{u}")
        all_rules += fetch_and_convert(u)

    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # 写入 surge.list
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(all_rules))

    print(f"✅ 完成！已生成：{OUTPUT_FILE} （共 {len(all_rules)} 条规则）")

if __name__ == "__main__":
    main()
