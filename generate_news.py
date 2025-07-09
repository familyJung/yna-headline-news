import requests
from bs4 import BeautifulSoup
from datetime import datetime

RSS_URL = "https://www.yna.co.kr/rss/all01.xml"
time_slots = {"07:30": 450, "10:30": 630, "14:30": 870, "18:00": 1080}

def fetch_news():
    response = requests.get(RSS_URL)
    soup = BeautifulSoup(response.content, "html.parser")  # ← 여기 수정됨
    items = soup.find_all("item")
    news_data = []
    for item in items:
        pub_time = datetime.strptime(item.pubDate.text, "%a, %d %b %Y %H:%M:%S %z").strftime("%H:%M")
        news_data.append({
            "title": item.title.text,
            "link": item.link.text,
            "time": pub_time
        })
    return news_data

def get_slot(t):
    h, m = map(int, t.split(":"))
    total = h * 60 + m
    return min(time_slots.keys(), key=lambda k: abs(total - time_slots[k]))

def group_news(news):
    result = {k: [] for k in time_slots}
    for item in news:
        slot = get_slot(item["time"])
        if len(result[slot]) < 5:
            result[slot].append(item)
    return result

def build_html(grouped):
    html = """<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>연합뉴스 헤드라인</title>
    <style>body{font-family:'Noto Sans KR',sans-serif;padding:20px}
    .time-block{margin:1em 0;padding:1em;border-radius:10px;background:#f5f5f5}
    .time-title{font-weight:bold;font-size:1.2em;margin-bottom:0.5em}
    a{color:#007BFF;text-decoration:none}a:hover{text-decoration:underline}
    </style></head><body><h1>📰 연합뉴스 이 시각 헤드라인</h1>"""
    for slot, articles in grouped.items():
        html += f"<div class='time-block'><div class='time-title'>🕒 {slot}</div><ul>"
        for a in articles:
            html += f"<li><a href='{a['link']}' target='_blank'>{a['title']}</a></li>"
        html += "</ul></div>"
    html += "</body></html>"
    return html

if __name__ == "__main__":
    news = fetch_news()
    grouped = group_news(news)
    html = build_html(grouped)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
