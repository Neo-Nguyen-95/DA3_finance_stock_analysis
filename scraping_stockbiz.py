#%% LIBRARY
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

#%% URL SET-UP
# URL information
company_name = 'POW'
url = 'https://stockbiz.vn/ma-chung-khoan/' + company_name

#%% LOGIN
service = Service(executable_path='/Users/dungnguyen/Downloads/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)
driver.get(url)

#%% SHOW DATA
time.sleep(1)
driver.execute_script("window.scrollBy(0, 3000);")
time.sleep(1)
driver.execute_script("window.scrollBy(0, 1500);")
time.sleep(1)
driver.find_element(
    By.XPATH, "//*[contains(@class, 'text-lg text-center') and text()='Tài chính']").click()


time.sleep(1)
driver.find_element(
    By.XPATH, "//*[contains(@class, 'inline-flex items-center justify-center text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background bg-secondary text-secondary-foreground hover:bg-secondary/80 h-9 px-3 rounded-md') and text()='Báo cáo tài chính']").click()

time.sleep(1)
Select(
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/main/div/div[3]/div[2]/div/div[2]/table/thead/tr/th[1]/div/div[2]/select')
    ).select_by_visible_text('Theo năm')

time.sleep(1)
Select(
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/main/div/div[3]/div[2]/div/div[2]/table/thead/tr/th[1]/div/div[3]/select')
        ).select_by_visible_text('1')

time.sleep(0.5)
driver.execute_script("window.scrollBy(0, 250);")
time.sleep(0.5)

#%% GET DATA - INCOMESTATEMENT

def get_income_data():
    # year
    content_year = driver.find_element(
        By.XPATH, '//*[@id="__next"]/div[3]/div/main/div/div[3]/div[2]/div/div[2]/table/thead/tr').text
    
    content_year = content_year.splitlines()[-1]
    year_list = list(content_year.split())
    
    # statistics
    content_stat = driver.find_element(
        By.XPATH, '//*[@id="__next"]/div[3]/div/main/div/div[3]/div[2]/div/div[2]/table/tbody').text
    
    content_stat = content_stat.replace(',', '')
    content_stat = content_stat.splitlines()
    try:
        content_stat.remove('I. DOANH THU HOẠT ĐỘNG')
        content_stat.remove('II. CHI PHÍ HOẠT ĐỘNG')
        content_stat.remove('III. DOANH THU HOẠT ĐỘNG TÀI CHÍNH')
        content_stat.remove('IV. CHI PHÍ TÀI CHÍNH')
        content_stat.remove('VIII. THU NHẬP KHÁC VÀ CHI PHÍ KHÁC')
        content_stat.remove('XIII. THU NHẬP THUẦN TRÊN CỔ PHIẾU PHỔ THÔNG')
        content_stat.remove('13.1. Lãi cơ bản trên cổ phiếu (Đồng/1 cổ phiếu)')
        content_stat.remove('13.2. Thu nhập pha loãng trên cổ phiếu (Đồng/1 cổ phiếu)')
    except:
        pass
    
    item = []
    stat = []
    
    for i in range(len(content_stat)):
        if i % 2 == 0:
            item.append(content_stat[i])
        else:
            stat.append(content_stat[i])
    
    df = pd.DataFrame(stat, index=item)
    df = df[0].str.split(expand=True)
    df.columns = year_list
    
    return df
    
df = get_income_data()

condition = True
while condition == True:
    try:
        driver.find_element(
            By.XPATH, '//*[@id="__next"]/div[3]/div/main/div/div[3]/div[2]/div/div[2]/table/thead/tr/th[1]/div/div[1]/button[1]').click()
        time.sleep(2)
        df2 = get_income_data()
        df = df.join(df2.iloc[:, 0])
        time.sleep(0.5)
    except:
        print("End scraping income statement!")
        condition = False

df = df.reindex(columns = df.columns.sort_values())

df.T.to_csv(company_name + "_income.csv")
df.to_excel(company_name + "_income.xlsx")

#%% GET DATA - BALANCE SHEET
time.sleep(.5)
driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/main/div/div[3]/div[2]/div/div[1]/div/button[1]').click()
time.sleep(1)

def get_bsheet_data():
    # year
    content_year = driver.find_element(
        By.XPATH, '//*[@id="__next"]/div[3]/div/main/div/div[3]/div[2]/div/div[2]/table/thead/tr').text
    
    content_year = content_year.splitlines()[-1]
    year_list = list(content_year.split())
    
    # statistics
    content_stat = driver.find_element(
        By.XPATH, '//*[@id="__next"]/div[3]/div/main/div/div[3]/div[2]/div/div[2]/table/tbody').text
    
    content_stat = content_stat.replace(',', '')
    content_stat = content_stat.splitlines()
    try:
        content_stat.remove('TÀI SẢN')
        content_stat.remove('NGUỒN VỐN')
        # content_stat.remove('LỢI NHUẬN ĐÃ PHÂN PHỐI CHO NHÀ ĐẦU TƯ')
        # content_stat.remove('1. Lợi nhuận đã phân phối cho Nhà đầu tư trong năm')
        
    except:
        pass
    
    item = []
    stat = []
    
    for i in range(len(content_stat)):
        if i % 2 == 0:
            item.append(content_stat[i])
        else:
            stat.append(content_stat[i])
    
    df = pd.DataFrame(stat, index=item)
    df = df[0].str.split(expand=True)
    df.columns = year_list
    
    return df

df = get_bsheet_data()

condition = True
while condition == True:
    try:
        driver.find_element(
            By.XPATH, '//*[@id="__next"]/div[3]/div/main/div/div[3]/div[2]/div/div[2]/table/thead/tr/th[1]/div/div[1]/button[1]').click()
        time.sleep(1)
        df2 = get_bsheet_data()
        df = df.join(df2.iloc[:, 0])
        time.sleep(3)
    except:
        print("End scraping balance sheet!")
        condition = False

df = df.reindex(columns = df.columns.sort_values())

df.T.to_csv(company_name + "_bsheet.csv")
df.to_excel(company_name + "_bsheet.xlsx")

#%% GET DATA - CASH FLOW
time.sleep(0.5)
driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/main/div/div[3]/div[2]/div/div[1]/div/button[4]').click()
time.sleep(0.5)

def get_cashflow_data():

    content_year = driver.find_element(
        By.XPATH, '//*[@id="__next"]/div[3]/div/main/div/div[3]/div[2]/div/div[2]/table/thead/tr').text
    
    content_year = content_year.splitlines()[-1]
    year_list = list(content_year.split())
    
    # statistics
    content_stat = driver.find_element(
        By.XPATH, '//*[@id="__next"]/div[3]/div/main/div/div[3]/div[2]/div/div[2]/table/tbody').text
    
    content_stat = content_stat.replace(',', '')
    content_stat = content_stat.splitlines()
    try:
        content_stat.remove('I. Lưu chuyển tiền từ hoạt động kinh doanh')
        content_stat.remove('II. Lưu chuyển tiền từ hoạt động đầu tư')  
        content_stat.remove('III. Lưu chuyển tiền từ hoạt động tài chính')
        # content_stat.remove('I. LƯU CHUYỂN TIỀN TỪ HOẠT ĐỘNG KINH DOANH')
    except:
        pass
    
    item = []
    stat = []
    
    for i in range(len(content_stat)):
        if i % 2 == 0:
            item.append(content_stat[i])
        else:
            stat.append(content_stat[i])
    
    df = pd.DataFrame(stat, index=item)
    df = df[0].str.split(expand=True)
    df.columns = year_list
    
    return df

df = get_cashflow_data()
df = df.reset_index()

condition = True
while condition == True:
    try:
        driver.find_element(
            By.XPATH, '//*[@id="__next"]/div[3]/div/main/div/div[3]/div[2]/div/div[2]/table/thead/tr/th[1]/div/div[1]/button[1]').click()
        time.sleep(1)
        df2 = get_cashflow_data()
        df = df.join(df2.reset_index().iloc[:, 1])
        time.sleep(1)
    except:
        print("End scraping cashflow!")
        condition = False

df = df.set_index('index')
df = df.reindex(columns = df.columns.sort_values())

df.T.to_csv(company_name + "_cashflow.csv")
df.to_excel(company_name + "_cashflow.xlsx")
    



