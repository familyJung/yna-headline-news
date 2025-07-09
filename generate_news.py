import requests
from bs4 import BeautifulSoup

# 연합뉴스 헤드라인 URL
URL = "https://www.yna.co.kr/report/headline?site=wholemenu_headline"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 기사 목록 찾기
articles = soup.select(".list-type038 li")  # 기사 리스트 요소

# HTML로 구성할 변수
html_output = '<div style="font-family: Arial, sans-serif;">\n'
html_output += '<h2>📰 연합뉴스 헤드라인</h2>\n<ul>\n'

for article in articles[:10]:  # 상위 10개 기사만 표시
    title_tag = article.select_one("a")
    if title_tag:
        link = title_tag["href"]
        title = title_tag.get_text(strip=True)
        html_output += f'  <li style="margin: 8px 0;"><a href="{link}" target="_blank" style="text-decoration: none; color: #333;">{title}</a></li>\n'

html_output += "</ul>\n</div>"

# 결과 출력
print(html_output)
