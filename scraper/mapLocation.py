
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



def search_place_data(place_name):
    print("init data")
    Place = browser.find_element(By.CLASS_NAME,'searchboxinput')
    print('search_name :',place_name)
    Place.send_keys("")
    Place.send_keys(place_name)
    submit = browser.find_element(By.ID,"searchbox-searchbutton")
    print(submit.text)
    submit.click()
    time.sleep(5)

    # 有資料
    place_list = browser.find_elements(By.CLASS_NAME, 'hfpxzc')
    # print('span: ', browser.find_element(By.CLASS_NAME ,'ah5Ghc').text)

    print(" start ")
    # print(len(place_list))
    for i in range(len(place_list)):
        print(i,'name: ', place_list[i].get_attribute('aria-label') )
        print(i,'source_url: ' ,place_list[i].get_attribute('href'))
        print(i,'span: ' ,place_list[i].get_attribute('title'))
        print(i,'test: ' , place_list[i].find_element(By.CLASS_NAME, 'lI9IFe'))


    # address 
    place_list_a = browser.find_elements(By.CLASS_NAME, 'lI9IFe') 
    print('len  = ',len(place_list_a) )
    for i in range(len(place_list_a)): 
        tmp = place_list_a[i].find_elements(By.CLASS_NAME, 'W4Efsd')
        for j in range(len(tmp)):
            print(place_list_a[i],' index =',tmp[j].text)


    #description
    place_list2 = browser.find_elements(By.CLASS_NAME, 'qty3Ue')
    print('len 1 = ',len(place_list2) )
    for i in range(len(place_list2)): 
    
        tmp = place_list2[i].find_elements(By.CLASS_NAME, 'ah5Ghc')
        for j in range(len(tmp)):
            print(tmp[j].text)
    
    # for item in place_list:
        # t = item.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/div[2]')      
        # print(t.get_attribute('aria-label'))
    # 找不到資料 
    # text = browser.find_element(By.CLASS_NAME, 'Q2vNVc')
    # print(text.text)
    time.sleep(3)
    clear = browser.find_element(By.XPATH,'//*[@id="searchbox"]/div[3]/button/div')
    print(clear.text)
    clear.click()
    time.sleep(3)


    print('search key word finish')


def search_place_no_data(place_name):
    print("init no data")
    Place = browser.find_element(By.CLASS_NAME,'searchboxinput')
    print(place_name)
    Place.send_keys("")
    Place.send_keys(place_name)
    submit = browser.find_element(By.ID,"searchbox-searchbutton")
    print(submit.text)
    submit.click()
    time.sleep(3)

    # 找不到資料 
    text = browser.find_element(By.CLASS_NAME, 'Q2vNVc')
    print(text.text)
    time.sleep(5)
    clear = browser.find_element(By.XPATH,'//*[@id="searchbox"]/div[3]/button/div')
    print(clear.text)
    clear.click()
    time.sleep(3)
    print('search key word finish')


if __name__ == "__main__":
    print("map location start")
    # 1. read loc
    fn = 'Location.csv' 
    with open(fn) as csvFile : 
        csvReader = csv.reader(csvFile) 
        listReport = list(csvReader) 
    # for i in range(11):
    #     if(i!=0):
    #         search_place_data(listReport[i][1])

    # try:
    #     search_place_data(listReport[1613][1])
    # except Exception as e: 
    #     search_place_no_data(listReport[1613][1])

    
    for i in range(5):
        print("index" , i)
        if i!=0:
            try:
                print(" ok ",listReport[i][0],listReport[i][1])
                search_place_data(listReport[i][1])
                # continue
            except Exception as NoSuchElementException: 
                print("error",listReport[i][0],listReport[i][1])
                search_place_no_data(listReport[i][1])
                # continue
    
    time.sleep(15)
    
            
    # 2. check loc is exist
    

    # 3. get loc detail data (first , sec ,third)


    # 4. write file 