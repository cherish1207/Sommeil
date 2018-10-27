#1. 공공데이터 이용하기
import requests
from bs4 import BeautifulSoup

def find_weather():
    r = requests.get("http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108") #기상청에서 가져오기
    soup = BeautifulSoup(r.text, 'xml') #parsing
    raw_data = soup.wf.string
    raw_data = raw_data.replace('(',' ') #문자 바꾸기
    raw_data = raw_data.replace(')',' ')
    raw_data = raw_data.replace('℃','도')
    raw_data = raw_data.replace(':',' ')
    raw_data = raw_data.replace('~','부터')

    data = raw_data.split('<br />')

    return(data[0]+data[1])

print(find_weather())
