#!/usr/bin/env python3
import os, requests

# 1. 读取你的订阅 URL 列表
src = "source/custom/Advertising/subscriptions.list"
# 2. 输出文件
out = "output/substore.list"
os.makedirs(os.path.dirname(out), exist_ok=True)

with open(src, encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

merged = []
for url in urls:
    print("拉取：", url)
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        merged.append(r.text.strip())
    except Exception as e:
        print(f"⚠️ 拉取失败 {url}：{e}")

# 3. 合并并写入
with open(out, "w", encoding="utf-8") as f:
    f.write("\n\n".join(merged))

print(f"✅ 完成：合并 {len(merged)} 个订阅，输出 -> {out}")
