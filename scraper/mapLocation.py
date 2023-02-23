
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import csv
import time
from env_crawler import hiking_index_url,driver_path,options,google_map_url
import requests

url = 'https://www.ettoday.net/news/news-list.html'
# 假的 headers 資訊
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
# 加入 headers 資訊
web = requests.get(url, headers=headers)
web.encoding = 'utf8'
# 假的 headers 資訊
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"



options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
# 加入 headers 資訊
options.add_argument('--user-agent=%s' % user_agent)

browser = webdriver.Chrome(chrome_options=options ,executable_path='./chromedriver')
# browser = webdriver.Chrome(executable_path='./chromedriver')
browser.get("https://www.google.com/maps/")



def search_place(place_name):
    print("init ")
    Place = browser.find_element(By.CLASS_NAME,'searchboxinput')
    print(place_name)
    Place.send_keys(place_name)
    submit = browser.find_element(By.ID,"searchbox-searchbutton")
    print(submit.text)
    submit.click()
    time.sleep(15)

    # 有資料
    place_list = browser.find_elements(By.CLASS_NAME, 'hfpxzc')
    print(place_list)
    for item in place_list:
        item.find_element()
        print(item)
    # 找不到資料 
    # text = browser.find_element(By.CLASS_NAME, 'Q2vNVc')
    # print(text.text)
    # time.sleep(15)
    print('search key word finish')

if __name__ == "__main__":
    print("map location start")
    # 1. read loc
    fn = 'Location.csv' 
    with open(fn) as csvFile : 
        csvReader = csv.reader(csvFile) 
        listReport = list(csvReader) 
        
    search_place(listReport[1][1])
    time.sleep(15)
    
    # for i in range(1):
    #     if i!=0:
    #         print(listReport[i][0],listReport[i][1])
            
    # 2. check loc is exist
    

    # 3. get loc detail data (first , sec ,third)


    # 4. write file 