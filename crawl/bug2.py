import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            return content
        else:
            print(f"URL {url} returned an error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def main():
    url = "https://example.com"  # 要爬取的網頁 URL

    html_content = get_html(url)
    if html_content:
        # 使用 BeautifulSoup 解析 HTML 內容
        soup = BeautifulSoup(html_content, "html.parser")

        # 印出標題文字
        print(soup.title.text.strip())
        paragraphs = soup.find_all("p")
        for p in paragraphs:
            print(p.text)

        print("\nURLs:")
        links = soup.find_all("a")
        for link in links:
            print(link.get("href"))

    else:
        print("無法取得網頁內容")


if __name__ == "__main__":
    main()
