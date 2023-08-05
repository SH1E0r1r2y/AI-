import json
import random

# 讀取原始 JSON 檔案
with open('Confusion Matrix/phishing_jsrepo.json', 'r') as f:
    data = json.load(f)

random_sample = random.sample(data, 260)

# 計算 "phishing" 為 True 的數量
true_count = sum(1 for item in random_sample if item["phishing"] == True)

print("隨機抽取的 260 個結果中，'phishing' 為 True 的數量：", true_count)

# 將選中的結果寫入新的 JSON 檔案
with open('Confusion Matrix/choose_phishing.json', 'w') as f:
    json.dump(random_sample, f, indent=2)

print("已將選中的結果寫入 selected_results.json 檔案")
