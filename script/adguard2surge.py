import requests, os

source_file = "source/custom/Advertising/source.list"
output_file = "output/surge.txt"
os.makedirs("output", exist_ok=True)

all_rules = []
with open(source_file, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    for url in urls:
        print(f"Fetching: {url}")
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            for line in r.text.splitlines():
                if line.startswith("||") and "^" in line:
                    d = line[2:].split("^")[0]
                    all_rules.append(f"DOMAIN-SUFFIX,{d},REJECT")
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("[Rule]\n")
    f.write("\n".join(all_rules))
