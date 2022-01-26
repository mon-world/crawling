'''
파이썬 매뉴얼을 재귀적으로 다운받는 프로그램

하이퍼 링크도 스스로 들어가서, 다운받는다.
'''
# 모듈 읽어 들이기 
from bs4 import BeautifulSoup
from urllib.request import *
from urllib.parse import *
from os import makedirs
import os.path, time, re
# 이미 처리한 파일인지 확인하기 위한 변수 
proc_files = {}
# HTML 내부에 있는 링크를 추출하는 함수 : 내부 하이퍼링크를 저장
def enum_links(html, base):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select("link[rel='stylesheet']") 
    links += soup.select("a[href]") 
    result = []
    # href 속성을 추출하고, 링크를 절대 경로로 변환 
    for a in links:
        href = a.attrs['href']
        url = urljoin(base, href)
        result.append(url)
    return result
# 파일을 다운받고 저장하는 함수 
def download_file(url):
    o = urlparse(url)
    savepath = "./" + o.netloc + o.path
    if re.search(r"/$", savepath): # 폴더라면 index.html
        savepath += "index.html"
    savedir = os.path.dirname(savepath)
    # 모두 다운됐는지 확인
    if os.path.exists(savepath): return savepath
    # 다운받을 폴더 생성
    if not os.path.exists(savedir):
        print("mkdir=", savedir)
        makedirs(savedir)
    # 파일 다운받기 / 실패 표시
    try:
        print("download=", url)
        urlretrieve(url, savepath)
        time.sleep(1) 
        return savepath
    except:
        print("다운 실패: ", url)
        return None        
# HTML을 분석하고 다운받는 함수 
def analyze_html(url, root_url):
    savepath = download_file(url)
    if savepath is None: return
    if savepath in proc_files: return 
    proc_files[savepath] = True
    print("analyze_html=", url)
    # 링크 추출 
    html = open(savepath, "r", encoding="utf-8").read()
    links = enum_links(html, url)
    for link_url in links:  # enum_links에서 출력된 링크들을 들어가며 analyze_html를 실행한다.
        # 링크가 루트 이외의 경로를 나타낸다면 무시 
        if link_url.find(root_url) != 0:
            if not re.search(r".css$", link_url): continue
        # HTML이라면
        if re.search(r".(html|htm)$", link_url):
            # 재귀적으로 HTML 파일 분석하기 : 자기 한번 더 호출해서 모든 링크 안을 들어감.
            analyze_html(link_url, root_url)
            continue
        # 기타 파일
        download_file(link_url)
if __name__ == "__main__":
    # URL에 있는 모든 것 다운받기
    url = "https://docs.python.org/3.7/library/"
    analyze_html(url, url)