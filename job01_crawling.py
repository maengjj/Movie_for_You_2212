# 팀장의 지시사항
# crawling 작업

# crawling은 각자 진행해보고 빨리 완성되는 코드로 연도를 나눠서 작업할게요.
# 일단 2022년 개봉작만 클롤링 해주세요.
# 나머지는 연도별로 나눠서 작업할게요.
# 컬럼명은 ['titles', 'reviews']로 통일해주세요.
# 파일명은 'reviews_{}.csv'.format(연도) 로 해주세요.
# crawling 코드 완성되는대로 PR해주세요.

from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)


review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'          # 리뷰 버튼
review_num_path = '//*[@id="reviewTab"]/div/div/div[2]/span/em'     # 총 리뷰 개수
review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'     # 리뷰 내용

# 네이버 영화 크롤링
# 디렉토리-개봉년도 를 이용해 크롤링! (제작년도로 크롤링 시 리뷰가 없는 경우가 많다.)


your_year = [2021, 2020]
your_page = [39, 38]
for i in range(2):
    for page in range(1, your_page[i]):
        url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={}&page={}'.format(your_year[i], page)
        titles = []
        reviews = []
        try:
            for title_num in range(1, 21):
                driver.get(url)  # 페이지 열기
                time.sleep(0.1)
                # 영화 제목 클릭
                movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(title_num)
                title = driver.find_element('xpath', movie_title_xpath).text
                print('title', title)
                driver.find_element('xpath', movie_title_xpath).click()
                time.sleep(0.1)

                try:
                    # 리뷰 버튼 클릭
                    driver.find_element('xpath', review_button_xpath).click()
                    time.sleep(0.1)

                    # 리뷰 페이지의 수 찾기
                    review_num = driver.find_element('xpath', review_num_path).text
                    review_num = review_num.replace(',', '')  # 리뷰가 1000개가 넘어가면 ,를 찍는다. , 제거
                    review_range = (int(review_num) - 1) // 10 + 1  # 총 리뷰 페이지의 수
                    if review_range > 3:
                        review_range = 3
                    for review_page in range(1, review_range + 1):
                        review_page_button_xpath = '//*[@id="pagerTagAnchor{}"]'.format(review_page)
                        driver.find_element('xpath', review_page_button_xpath).click()
                        time.sleep(0.1)

                        # 각 리뷰의 제목 클릭
                        for review_title_num in range(1, 11):
                            review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a'.format(review_title_num)
                            driver.find_element('xpath', review_title_xpath).click()
                            time.sleep(0.1)
                            # 내용을 불러오지 못하면 driver.back()으로 다시 돌아간다. 튕김 방지
                            try:
                                # 각 리뷰의 내용 불러오기
                                review = driver.find_element('xpath', review_xpath).text
                                titles.append(title)
                                reviews.append(review)
                                driver.back()  # 뒤로가기
                            except:
                                print('review', page, title_num, review_title_num)
                                driver.back()
                except:
                    print('review button', page, title_num)
            df = pd.DataFrame({'titles': titles, 'reviews': reviews})
            df.to_csv('./crawling_data/reviews_{}_{}page.csv'.format(your_year, page), index=False)
        except:
            print('error', page, title_num)











