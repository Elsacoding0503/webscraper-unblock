# 隨機輪換Proxy IP
import requests
import re
import random
from fake_useragent import UserAgent 
from bs4 import BeautifulSoup as bs
import pandas as pd

# Free Proxy List
response_proxy = requests.get('https://www.sslproxies.org/')
soup_proxy = bs(response_proxy.text, 'lxml')

# 建立多組清單
proxy_ips = re.findall("\d+\.\d+\.\d+\.\d+\:\d+", response_proxy.text)

# table = soup_proxy.find('tbody')
# ips = table.find_all('tr')
# for ip in ips:
#     print(ip.find_all('td')[0].text+':'+ip.find_all('td')[1].text)

# 認證Proxt IP的有效性
valid_ips = []
for proxy_ip in proxy_ips:
    try:
        if len(valid_ips) < 3:
            verification = requests.get('https://ip.seeip.org/jsonip?',
                        proxies={'http':proxy_ip, 'https':proxy_ip},
                         timeout=10
                        )
            valid_ips.append(proxy_ip)
        else:
            break
    except:
        print(f"{proxy_ip} invalid")

# 隨機選擇一組IP
ip = random.choice(valid_ips)
print(f"選擇IP {ip}")

proxies={
    'http':ip, 
    'https':ip
}

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}

url_tsmc = 'https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date=20230301&stockNo=2330&response=json&_=1681287102939'
response_twse = requests.get(url=url_tsmc, headers=headers, proxies=proxies)
data_twse = response_twse.json()

code = [content_twse[0] for content_twse in data_twse['data']]
titles = [content_twse[1] for content_twse in data_twse['data']]
yield_ = [content_twse[2] for content_twse in data_twse['data']]
dividend_year = [content_twse[3] for content_twse in data_twse['data']]
pe_ratio = [content_twse[4] for content_twse in data_twse['data']]
prb = [content_twse[5] for content_twse in data_twse['data']]
financial_statement_yq = [content_twse[6] for content_twse in data_twse['data']]

semi_con = {}
semi_con["證券代號"]=code
semi_con["股票名稱"]=titles
semi_con["殖利率"]=yield_
semi_con["股利年度"]=dividend_year
semi_con["本益比"]=pe_ratio
semi_con["股價淨值比"]=prb
semi_con["財報年度年/季"]=financial_statement_yq

df_semi = pd.DataFrame(semi_con)
print(df_semi)