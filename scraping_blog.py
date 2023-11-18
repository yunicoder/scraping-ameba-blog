import time
import requests
from bs4 import BeautifulSoup

def scrape_entry_urls(blog_url):
    response = requests.get(blog_url)
    if response.status_code != 200:
        return "Error: Unable to access the blog list page."

    soup = BeautifulSoup(response.content, 'html.parser')

    ameblo_url = 'https://ameblo.jp'
    entry_links = soup.find_all('li', class_='skin-borderQuiet')
    entry_titles = [link.text for link in entry_links]
    entry_urls = [ameblo_url + link.find('a').attrs['href'] for link in entry_links]

    return entry_urls, entry_titles

def get_publish_date(soup):
    """datetimeが取れなかったので無理やりmetaデータのurlから取得する"""
    img_url = soup.find('meta',{'name':'twitter:image'})['content']
    pub_date = img_url.split('/')[4]

    if len(pub_date) != 8:  # 8桁の数字ではない場合はnodateにする
        pub_date = "nodate"

    return pub_date


def scrape_blog_entry(url):
    # リクエストを送信してHTMLを取得
    response = requests.get(url)
    if response.status_code != 200:
        return "Error: Unable to access the page."

    soup = BeautifulSoup(response.text, 'html.parser')

    # タイトルと本文を抽出
    title = soup.find('title').get_text()
    content = soup.find('div', class_='skin-entryBody').get_text()
    pub_date = get_publish_date(soup)

    return title, content, pub_date

def main():
    # ブログの一覧ページのURL
    blog_url = "https://ameblo.jp/juicejuice-official/theme-10103223818.html"

    # エントリーURLをスクレイピング
    entry_urls, entry_titles = scrape_entry_urls(blog_url)

    # 各エントリーをスクレイピングして結果を表示
    for url, title in zip(entry_urls, entry_titles):
        _, content, pub_date = scrape_blog_entry(url)

        # 保存
        saved_name = f"outputs/{pub_date}_{title}.txt"
        with open(saved_name, mode="w") as f:
            f.write(content)

        time.sleep(0.1)

if __name__ == '__main__':
    main()
