# 網頁一般驗證碼通過 - 2capcha
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time,random
from fake_useragent import UserAgent 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests, os
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.action_chains import ActionChains
import base64
from selenium.webdriver.common.keys import Keys
import api

ua = UserAgent()
options = Options() 
# options.add_argument('--headless') 
options.add_argument("user-agent=" + ua.chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(5)

# 下載驗證碼圖片
url_books_login = 'https://cart.books.com.tw/member/login?loc=customer_003&url=https%3A%2F%2Fwww.books.com.tw%2F'
driver.get(url_books_login)

image_base64 = driver.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele,0,0);
    return cnv.toDataURL('image/jpeg').substring(22);
    """, driver.find_element(By.ID, 'captcha_img').find_element(By.TAG_NAME, 'img'))

with open('capcha.png', 'wb') as image:
    image.write(base64.b64decode(image_base64))


# 傳送網頁一般驗證碼到2capcha 服務
api_key = api.api_key
file = {'file': open('capcha.png', 'rb')}
data = {
    'key':api_key,
    'method':'post'
}
url_capcha = 'http://2captcha.com/in.php'
response_capcha = requests.post(url=url_capcha, files=file, data=data)
capcah_id = response_capcha.text.split("|")[1]

# 取得網頁一般驗證碼的結果
for i in range(10):
    
    result_capcha = requests.get(f'http://2captcha.com/res.php?key={api_key}&action=get&id={capcah_id}')
    if result_capcha.text.find('CAPCHA_NOT_READY') > -1:
        time.sleep(5)
    elif result_capcha.text.find('OK') > -1:
        capcha_text = result_capcha.text.split("|")[1]
        break
    else:
        print('error')

driver.find_element(By.ID, "captcha").send_keys(capcha_text)
time.sleep(10)
    
driver.close()