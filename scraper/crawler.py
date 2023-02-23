from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
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


def search_place():
    Place = browser.find_element(By.CLASS_NAME,'searchboxinput')
    Place.send_keys("金面山親山步道")
    submit = browser.find_element(By.ID,"searchbox-searchbutton")
    print(submit.text)
    submit.click()
    time.sleep(15)
    print('search key word finish')


def find_review_link():
    #allxGeDnJMl__button
    review_link= browser.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span')
    total_num = review_link.text.strip(' 則評論')
    total_num = total_num.replace(',','')
    total_num = total_num.replace('(','')
    total_num = total_num.replace(')','')
    review_link.click()
    print("click review link") 
    return int(total_num)


def find_sorting_tag():
    sorting_tag = browser.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button/span')
    sorting_tag.click()
    time.sleep(1.5)
    print("click sorting tag")
  

def find_latest_tag():
    latest_link= browser.find_element(By.XPATH, '//*[@id="action-menu"]/div[2]') 
    latest_link.click()
    time.sleep(1.5)
    print("click latest tag") 

## #action-menu > div:nth-child(2) css
#//*[@id="action-menu"]/div[2] xpath

def scroll_data(counter):
    last_height = browser.execute_script("return document.body.scrollHeight")
    print('scrolling... ',last_height)

    for _i in range(counter):
        scrollable_div = browser.find_element( By.XPATH,'//div[@class="lXJj5c Hk4XGb"]')
        h = browser.execute_script("return document.body.scrollHeight")
        # browser.execute_script(
        #         'document.getElementsByClassName("dS8AEf")[0].scrollTop = document.getElementsByClassName("dS8AEf")[0].scrollHeight',
        #         scrollable_div
        #     )
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        print("AAAA",_i,"/",counter,h)
        # get_data()
        time.sleep(3)


def scroll_data_ok(counter):

    # 設定等待時間和動態滾動步長
    WAIT_TIME = 2
    scroll_area = browser.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
    last_height = browser.execute_script("return arguments[0].scrollHeight", scroll_area)
    SCROLL_STEP = last_height/4 #滾輪滾四次
    reset_num = int(last_height/SCROLL_STEP)
    print('scrolling... ',"last_height : ",last_height, "SCROLL_STEP:",SCROLL_STEP,"reset_num:",reset_num)
    
    for _i in range(counter):
        browser.execute_script('arguments[0].scrollBy(0, arguments[1]);', scroll_area, SCROLL_STEP)
        i = _i+1
        tmp =   i % reset_num
        if(tmp== 0):
            print("Loading...." , tmp, reset_num , i)
            more_ele = browser.find_elements(By.CLASS_NAME , 'w8nwRe')
            for list_more_ele in more_ele:
                list_more_ele.click()
                
            elements = browser.find_elements(By.CLASS_NAME , 'jftiEf')
            for data in elements:
                    name = data.find_element(By.CLASS_NAME , 'd4r55').text
                    text = data.find_element(By.CLASS_NAME , 'wiI7pd').text
                    score = data.find_element(By.CLASS_NAME , 'kvMYJc').get_attribute("aria-label")
                    print(name," , ",text," , ",score)
            time.sleep(WAIT_TIME) # Loading ....建議降速 , 太快會被ban
        else:
            time.sleep(0.2) # Scrooll.... 


        WebDriverWait(browser, WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[last()]')))


def test2():
    print("test2 ---- ")
    # 設定等待時間和滾動步長
    WAIT_TIME = 3
    SCROLL_STEP = 1000

    # 定位到滾動區域的元素
    scroll_area = browser.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')

    # 獲取網頁內容的高度
    last_height = browser.execute_script("return arguments[0].scrollHeight", scroll_area)
    print('scrolling... ',last_height,SCROLL_STEP,last_height/SCROLL_STEP)

    # 持續滾動，直到滾動到頁面底部
    while True:
        # 滾動一個步長
        browser.execute_script('arguments[0].scrollBy(0, arguments[1]);', scroll_area, SCROLL_STEP)

        try:
            # 等待頁面內容加載完畢
            print("loading...")
            WebDriverWait(browser, WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[last()]')))
        except:
            # 如果超時，則停止滾動
            print("Timeout...")
            break

        # 獲取滾動後的網頁內容高度
        new_height = browser.execute_script("return arguments[0].scrollHeight", scroll_area)
        print(new_height)
        # 如果滾動到頁面底部，則停止滾動
        if new_height == last_height:
            print(" SAME",)
            break

        # 更新 last_height
        last_height = new_height



if __name__ == "__main__":
    print('start')
    time.sleep(5)

    search_place()
    num = find_review_link()
    print(num)
    time.sleep(3)
    find_sorting_tag()
    find_latest_tag()
    scroll_data_ok(num)
    # test2()    

    
    time.sleep(30) 

    print('End')
