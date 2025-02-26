import time
import re  # 이 줄을 추가하세요
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 이하 코드는 그대로 유지


driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

# 검색어 설정
keyword = "강남역 맛집"

# 네이버 지도 검색 URL 접속
naver_map_search_url = f'https://map.naver.com/v5/search/{keyword}/place'
driver.get(naver_map_search_url)
time.sleep(1)  # 페이지 로딩 대기

# 검색 결과 URL에서 장소 코드 추출
current_url = driver.current_url
res_code = re.findall(r"place/(\d+)", current_url)

if res_code:
    # 리뷰 페이지로 이동
    final_url = 'https://pcmap.place.naver.com/restaurant/' + res_code[0] + '/review/visitor#'
    driver.get(final_url)
    time.sleep(1)
    
    # 데이터 수집 로직 작성
    # 예: 리뷰 텍스트 수집
    reviews = []
    review_elements = driver.find_elements(By.CSS_SELECTOR, ".review_text")
    for element in review_elements:
        reviews.append(element.text)
    
    # 결과 저장
    df = pd.DataFrame({"리뷰": reviews})
    df.to_csv('naver_map_reviews.csv', encoding='utf-8-sig', index=False)

driver.quit()
