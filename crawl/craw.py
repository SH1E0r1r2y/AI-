from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from PIL import Image


def get_final_url_and_html(url):
    driver = webdriver.Firefox()

    # Get the final URL after following redirects
    driver.get(url)
    final_url = driver.current_url

    # Get the HTML content after JavaScript execution
    html_after_js = driver.page_source

    # Close the browser
    driver.quit()

    return final_url, html_after_js


def capture_screenshot(url, save_path):

    driver = webdriver.Firefox()

    # Open the URL and take a screenshot
    driver.get(url)
    driver.save_screenshot(save_path)

    # Close the browser
    driver.quit()


def main():
    input_urls = ["http://e-etc.top/"]

    for index, url in enumerate(input_urls):
        final_url, html_after_js = get_final_url_and_html(url)
        try:
            response = requests.get(final_url)
            if response.status_code == 200:
                content = response.text
                # if "https://165.npa.gov.tw/" in content:
                #     print(f"{final_url}警政署關心您")
                # Save HTML to a file
                with open(f"html_{index}.html", "w", encoding="utf-8") as file:
                    file.write(html_after_js)

                # Capture and save the screenshot
                capture_screenshot(url, f"screenshot_{index}.png")

                print(f"URL {url} -> Final URL: {final_url}")
            else:
                print(f"{final_url}: ERROR {response.status_code}")

        except Exception as e:
            print(f"{final_url}: Exception {e}")


if __name__ == "__main__":
    main()
