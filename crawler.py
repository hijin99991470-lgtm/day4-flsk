import sys
import io
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def setup_stdout():
    if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

RSS_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
EXCLUDE_SOURCES = ["조선일보"]


def fetch_news(limit=10):
    resp = requests.get(RSS_URL, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "xml")
    items = soup.find_all("item")

    news = []
    for item in items:
        if len(news) >= limit:
            break

        title = item.title.text if item.title else ""
        link = item.link.text if item.link else ""
        pub_date = item.pubDate.text if item.pubDate else ""

        if any(src in title for src in EXCLUDE_SOURCES):
            continue

        # description에서 두 번째 li를 요약으로 사용 (첫 번째는 메인 기사와 동일)
        desc_raw = item.description.text if item.description else ""
        desc_soup = BeautifulSoup(desc_raw, "html.parser")
        lis = desc_soup.find_all("li")
        summary = lis[1].get_text(strip=True) if len(lis) > 1 else ""

        if pub_date:
            try:
                dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S GMT")
                pub_date = dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                pass

        news.append({
            "title": title,
            "summary": summary,
            "link": link,
            "pub_date": pub_date,
        })

    return news


def display(news_list):
    WIDTH = 70

    for i, n in enumerate(news_list, 1):
        print("=" * WIDTH)
        print(f"  {i}. {n['title']}")
        print("-" * WIDTH)
        print(f"  발행  {n['pub_date']}")
        print(f"  요약  {n['summary'][:120]}")
        print(f"  링크  {n['link']}")
    print("=" * WIDTH)


if __name__ == "__main__":
    setup_stdout()
    print("구글 뉴스 한국어 RSS 크롤러 (조선일보 제외)\n")
    articles = fetch_news(limit=10)
    display(articles)
    print(f"\n총 {len(articles)}건 수집 완료")
