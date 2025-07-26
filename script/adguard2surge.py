import os
import requests

source_file = "source/custom/Advertising/source.list"
output_file = "output/surge.list"

def convert_adguard_to_surge_rule(adguard_text):
    lines = adguard_text.splitlines()
    surge_rules = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('!') or line.startswith('#'):
            continue
        if line.startswith('||'):
            domain = line[2:]
            if '/' in domain:
                domain = domain.split('/')[0]
            surge_rules.append(f'DOMAIN-SUFFIX,{domain},REJECT')
        elif line.startswith('|') and line.endswith('|'):
            domain = line[1:-1]
            surge_rules.append(f'DOMAIN,{domain},REJECT')
        elif line.startswith('|'):
            domain = line[1:]
            surge_rules.append(f'DOMAIN,{domain},REJECT')
        elif line.startswith('@@'):
            # 忽略白名单规则
            continue
        else:
            surge_rules.append(f'DOMAIN-SUFFIX,{line},REJECT')
    return '\n'.join(surge_rules)

def main():
    if not os.path.exists(source_file):
        print(f"{source_file} not found.")
        return

    with open(source_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    all_rules = []
    for url in urls:
        try:
            print(f"Fetching: {url}")
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            adguard_text = resp.text
            surge_rule = convert_adguard_to_surge_rule(adguard_text)
            all_rules.append(surge_rule)
        except Exception as e:
            print(f"Error processing {url}: {e}")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write('\n'.join(all_rules))

    print(f"Conversion complete. Output saved to {output_file}")

if __name__ == "__main__":
    main()
