import requests
import os
from bs4 import BeautifulSoup


def get_html(url):
    try:
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            content = response.text
            return content
        else:
            print(f"URL {url} returned an error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_text(html_content):
    text = []
    if html_content:
        # 使用 BeautifulSoup 解析 HTML 內容
        soup = BeautifulSoup(html_content, "html.parser")

        # 印出標題文字
        text.append(soup.title.text.strip())
        paragraphs = soup.find_all("p")
        for p in paragraphs:
            text.append(p.text)

        text.append("\nURLs:")
        links = soup.find_all("a")
        for link in links:
            text.append(link.get("href"))
        total_text = '\n'.join(text)
        return total_text
    else:
        text.append("無法取得網頁內容")
        total_text = '\n'.join(text)
        return total_text


def main():
    urls = ["https://example.com"]
    for url in urls:
        html_content = get_html(url)  # 在 url 的陣列裡面
        Total_text = get_text(html_content)
        output_folder = 'weeeb/data/filtered_data.txt'
        with open(output_folder, 'w', encoding='utf-8') as text_file:
            text_file.write(Total_text)


if __name__ == "__main__":
    main()
    print("OK")
