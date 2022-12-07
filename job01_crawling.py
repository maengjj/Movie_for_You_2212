from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)

# 네이버 영화 크롤링
# 디렉토리-개봉년도 를 이용해 크롤링! (제작년도로 크롤링 시 리뷰가 없는 경우가 많다.)


url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2022&page=1'







