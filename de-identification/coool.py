"""有 meta 值、html、url，有資料夾"""
import os
from bs4 import BeautifulSoup
import re


def filter_html_tags(html_content, allowed_tags):
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 過濾指定標籤的內容
    def is_allowed(tag):
        return tag.name in allowed_tags

    # 逐行搜索
    lines = []
    meta_tags = soup.find_all('meta')

    for meta_tag in meta_tags:
        lines.append(str(meta_tag))

    for line in soup.stripped_strings:
        if any(tag in line for tag in allowed_tags):
            lines.append(line)

     # 合併txt檔
    result_text = '\n'.join(lines)
    return result_text


def remove_empty_lines(text):
    # 分割並過濾空行
    lines = filter(lambda x: x.strip(), text.splitlines())
    # 合併txt檔
    result_text = '\n'.join(lines)
    return result_text


def extract_urls(html_content):
    # 使用正則表達提取HTML中的URL
    urls = re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html_content)
    return urls


def process_html_files(input_folder, output_folder, allowed_tags):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 獲取文件夾中的名稱
    html_files = [file for file in os.listdir(
        input_folder) if file.endswith('.html')]

    for html_file in html_files:
        # HTML 來源資料夾
        input_file_path = os.path.join(input_folder, html_file)

        # HTML内容
        with open(input_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # 過濾標籤、刪除空行
        filtered_data = filter_html_tags(html_content, allowed_tags)
        filtered_data_without_empty_lines = remove_empty_lines(filtered_data)

        # 結果位置，名稱與輸入相同，指示改為.txt）
        output_file_path = os.path.join(
            output_folder, os.path.splitext(html_file)[0] + '.txt')

        # 提取URL
        urls_data = extract_urls(html_content)

        # 將處理後的保存到文件中
        with open(output_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(filtered_data_without_empty_lines)
            text_file.write('\n\nURLs:\n')
            for url in urls_data:
                text_file.write(url + '\n')


# 指定要保留的HTML label
allowed_tags = ['head', 'title', 'meta', 'body', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'strong',
                'a', 'img', 'hr', 'table', 'tbody', 'tr', 'th', 'td', 'ol', 'ul', 'li', 'ruby', 'label']

# 填寫輸入與輸出路徑
input_folder_path = 'de-identification/html'
output_folder_path = 'de-identification/ans'

process_html_files(input_folder_path, output_folder_path, allowed_tags)
print("OK")
