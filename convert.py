import requests
import json
import os

# --- 核心配置区：在这里添加或修改你的分类和链接 ---
# 格式： "文件名.json": ["链接1", "链接2", ...]
TASKS = {
    "ChatGPT.json": [
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/OpenAI/OpenAI.list"
    ],
    "Other Ai.json": [
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Copilot/Copilot.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Gemini/Gemini.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Claude/Claude.list",
        "https://raw.githubusercontent.com/liandu2024/clash/refs/heads/main/list/MetaAi.list",
        "https://raw.githubusercontent.com/liandu2024/clash/refs/heads/main/list/Perplexity.list"
    ],
    "GitHub.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/GitHub/GitHub.list"],
    "TikTok.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/TikTok/TikTok.list"],
    "Instagram.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Instagram/Instagram.list"],
    "Telegram.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Telegram/Telegram.list"],
    "Twitter_FB_WA.json": [
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Twitter/Twitter.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Facebook/Facebook.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Whatsapp/Whatsapp.list"
    ],
    "Steam.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Steam/Steam.list"],
    "Game.json": [
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Epic/Epic.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/EA/EA.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Blizzard/Blizzard.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/UBI/UBI.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Sony/Sony.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Nintendo/Nintendo.list"
    ],
    "YouTube.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/YouTube/YouTube.list"],
    "Disney.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Disney/Disney.list"],
    "Netflix.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Netflix/Netflix.list"],
    "Spotify.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Spotify/Spotify.list"],
    "Amazon.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Amazon/Amazon.list"],
    "Apple.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Apple/Apple.list"],
    "Microsoft.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Microsoft/Microsoft.list"],
    "Google.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Google/Google.list"],
    "TEST.json": ["https://raw.githubusercontent.com/liandu2024/clash/refs/heads/main/list/Check.list"],
    "Block.json": [
        "https://raw.githubusercontent.com/liandu2024/clash/refs/heads/main/list/Block.list",
        "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/refs/heads/master/rule/Clash/BlockHttpDNS/BlockHttpDNS.list"
    ],
    "Emby-Proxy.json": ["https://raw.githubusercontent.com/2024JinFeng/clash/refs/heads/main/Emby-Proxy.list"],
    "Emby-Direct.json": ["https://raw.githubusercontent.com/2024JinFeng/clash/refs/heads/main/Emby-Direct.list"],
    "Direct.json": [
        "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/refs/heads/master/rule/Clash/Proxy/Proxy.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/ChinaMax/ChinaMax.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/China/China.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/PrivateTracker/PrivateTracker.list"
    ],
    "AMD.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/AMD/AMD.list"],
    "Nvidia.json": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Nvidia/Nvidia.list"]
}

def process_convert():
    for filename, urls in TASKS.items():
        print(f"正在处理分类: {filename} ...")
        
        result = {
            "version": 1,
            "rules": [{
                "domain": [],
                "domain_suffix": [],
                "domain_keyword": [],
                "ip_cidr": []
            }]
        }
        rule = result["rules"][0]

        for url in urls:
            try:
                # 自动处理 GitHub 网页链接为 Raw 链接
                raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                resp = requests.get(raw_url, timeout=15)
                resp.raise_for_status()
                resp.encoding = 'utf-8'
                
                for line in resp.text.splitlines():
                    line = line.strip()
                    if not line or line.startswith(("#", "payload:")): continue
                    if line.startswith("- "): line = line[2:]

                    parts = line.split(",")
                    if len(parts) < 2: continue
                    
                    t, v = parts[0].strip().upper(), parts[1].strip()
                    if t == "DOMAIN": rule["domain"].append(v)
                    elif t == "DOMAIN-SUFFIX": rule["domain_suffix"].append(v)
                    elif t == "DOMAIN-KEYWORD": rule["domain_keyword"].append(v)
                    elif t in ["IP-CIDR", "IP-CIDR6"]: rule["ip_cidr"].append(v)
            except Exception as e:
                print(f"警告: 链接 {url} 获取失败: {e}")

        # 去重、排序并清理
        for key in list(rule.keys()):
            if rule[key]:
                rule[key] = sorted(list(set(rule[key])))
            else:
                del rule[key]

        # 写入对应的 JSON
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"✅ 已生成: {filename}")

if __name__ == "__main__":
    process_convert()
