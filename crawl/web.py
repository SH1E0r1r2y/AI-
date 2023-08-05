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
    input_urls = ["https://landbank.co.id",
                  "http://109.206.243.124/MI0BLZ0ZJ9ACO/controle",
                  "https://pub-07116cf802b841148cc4dac8eb3af312.r2.dev/index.html#vanda.c...",
                  "https://wit.spaloniakshell.pl/synapsa/email@example.com...",
                  "https://dade2be954bd9eb321a516607a48ebdd.trsdha.pl/prgros/sgrpwla/7bef...",
                  "https://adam.gronowiecka.pl/sekret/email@example.com...",
                  "https://franciszek.bbrzezinska.pl/mariusury/email@example.com...",
                  "https://marek.spaloniakshell.pl/synapsa/email@example.com...",
                  "https://volos.mariuszslabon.pl/jurtom/email@example.com...",
                  "https://spytek.gosiafox.pl/zdzislaw/email@example.com...",
                  "https://lew.monikazabaw.pl/konrad/email@example.com...",
                  "https://roman.spaloniakshell.pl/synapsa/email@example.com...",
                  "https://maciej.monikajarosz.pl/sebastian/email@example.com...",
                  "https://przemysl.hulboj.org.pl/tobowski/email@example.com...",
                  "https://bozho.gronowiecka.pl/sekret/email@example.com...",
                  "https://instant-link.vercel.app/check.php?id=abddl...",
                  "https://marek.gosiafox.pl/zdzislaw/email@example.com...",
                  "https://seweryn.monikazabaw.pl/konrad/email@example.com...",
                  "https://campaigns-events.lon-1.onpdr.com/track/link/2d5qy6knqd/3iifpph...",
                  ]

    for index, url in enumerate(input_urls):
        final_url, html_after_js = get_final_url_and_html(url)

        # Save HTML to a file
        with open(f"html_{index}.html", "w", encoding="utf-8") as file:
            file.write(html_after_js)

        # Capture and save the screenshot
        capture_screenshot(url, f"screenshot_{index}.png")

        print(f"URL {url} -> Final URL: {final_url}")


if __name__ == "__main__":
    main()
