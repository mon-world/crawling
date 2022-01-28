'''
실시간 환률 정보 가져오기.
url : 네이버 환률 주소
'''

import requests
import datetime
from bs4 import BeautifulSoup
import pandas as pd

url="https://finance.naver.com/marketindex/"

response = requests.get(url) # 입력한 주소로 request하고, request에 대한 응답을 받는다.
html = response.content # response 객체에서 html 코드만 가져오기.

# BeautifulSoup으로 element를 객체화 시키기.
soup = BeautifulSoup(html, 'html.parser')
exchange_list = soup.select_one("#exchangeList")    # exchangeList만 가지고 있으면, 전체 리스트를 가지고 올 수 있으므로 1개만 가져오게 한다.
exchange_li_list = exchange_list.select("li")       # li 태그 안에 환률이 존재한다.

# h3 안쪽에 나라 이름이 들어있고, div 안쪽에 환률, 상승, 하락 등의 정보가 있음.
# h3과 div가 중요한 정보.

# 환률 정보를 한번에 가져오기
country_names = [] # 나라 이름들을 저장
values = [] # 환율 값을 저장
changes = [] # 변동 금액 저장
updowns = [] # 상승 / 하락 여부 저장

for exchange_li in exchange_li_list : # 순회하면서 하나씩 가져오게 할 것.
    country_name = exchange_li.select_one("h3.h_lst").text

    head_info = exchange_li.select_one("div.head_info")
    value = head_info.select_one("span.value").text
    change = head_info.select_one("span.change").text
    updown = exchange_li.select_one("div.head_info > span.blind").text

    print(country_name, value, change, updown)

    country_names.append(country_name)
    values.append(value)
    changes.append(change)
    updowns.append(updown)

# 데이터 프레임 형태로 만들기
datas = {
    "국가명" : country_names,
    "환율" : values,
    "변동" : changes,
    "등락" : updowns
}

finance_df = pd.DataFrame(datas)
finance_df

# 파일 저장 : 현재 시간
fliename = datetime.datetime.now().strftime("%Y-%m-%d") # 현재시간을 불러오기
finance_df.to_csv("./naver_finance " + fliename + ".csv", encoding = 'utf-8')
print("저장 완료!")