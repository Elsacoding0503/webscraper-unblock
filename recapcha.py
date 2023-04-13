# 網頁圖像驗證碼通過 - reCAPTCHA Enterprise
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from fake_useragent import UserAgent 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import api

chrome_driver_path = "/Users/mac/chromedriver_mac64/chromedriver"
ua = UserAgent()
options = Options() 
# options.add_argument('--headless') 
options.add_argument("user-agent=" + ua.chrome)
# driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(5)

url_checkseats = 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip119/queryTime'
driver.get(url_checkseats)

driver.find_element(By.ID, "startStation").send_keys('1000-臺北')
driver.find_element(By.ID, "endStation").send_keys('7000-花蓮')

# id
api_key = api.api_key
data_sitekey = '6LdHYnAcAAAAAI26IgbIFgC-gJr-zKcQqP1ineoz' # 從網頁原始碼找
# &enterprise=1 代表reCAPTCHA Enterpise V2，文件要求
api_url= f'http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={url_checkseats}&enterprise=1'
response_recapcha = requests.get(url=api_url)
recapcha_id= response_recapcha.text.split("|")[1]
print(recapcha_id)

# 將id傳送至res.php
recapcha_res_php_url=f'http://2captcha.com/res.php?key={api_key}&action=get&id={recapcha_id}'

for i in range(10):
    result_recapcha = requests.get(url=recapcha_res_php_url)
    
    if result_recapcha.text.find('CAPCHA_NOT_READY') > -1:
        time.sleep(10)
    elif result_recapcha.text.find('OK') > -1:
        recapcha_text = result_recapcha.text.split("|")[1]
        break
    else:
        print('error')
print(recapcha_text)

        
# 回填result，看文件
driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML=arguments[0]', recapcha_text)

# 點選查詢按鈕
driver.find_element(By.ID, "searchButton").click()
time.sleep(10)

driver.close()