#%% IMPORT LIBRARY
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

#%% URL SET-UP
# URL information
company_name = 'FPT'
url = 'https://www.bsc.com.vn/cong-ty/tong-quan/' + company_name

#%% LOGIN
service = Service(executable_path='/Users/dungnguyen/Downloads/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)
driver.get(url)

time.sleep(2)
data = driver.find_element(
    By.XPATH, "/html/body/div[3]/div[3]/div[4]/div[4]/div[1]/div[7]/table").text
print(data)

#%% PROCESS DATA

lines = data.splitlines()
# important lines: 9, 10, 15, 16, 17
