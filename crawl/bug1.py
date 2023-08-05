import requests
from bs4 import BeautifulSoup

allowed_tags = ['head', 'title', 'meta', 'body', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'strong',
                'a', 'img', 'hr', 'table', 'tbody', 'tr', 'th', 'td', 'ol', 'ul', 'li', 'ruby', 'label']


def extract_allowed_tags(url):
    try:
        # 發送 GET 請求，獲取網頁內容
        response = requests.get(url)
        response.raise_for_status()  # 檢查是否成功取得網頁內容
        content = response.text

        # 使用 BeautifulSoup 解析網頁內容
        soup = BeautifulSoup(content, 'html.parser')

        # 提取允許的標籤
        extracted_tags = []
        for tag in soup.find_all(allowed_tags):
            extracted_tags.append(tag)

        return extracted_tags

    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        return None


if __name__ == "__main__":
    # 要爬取的網頁 URL
    url = "https://example.com"  # 待研究：不允許爬蟲該怎麼辦？

    # 執行爬蟲並獲取允許的標籤
    extracted_tags = extract_allowed_tags(url)

    # 印出提取的允許的標籤
    if extracted_tags:
        for tag in extracted_tags:
            print(tag)
    else:
        print("Failed to extract tags.")
