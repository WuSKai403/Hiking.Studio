from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time



# options = Options()
# options.add_argument("start-maximized")
# options.add_argument("disable-infobars")
# options.add_argument("--disable-extensions")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")

# browser = webdriver.Chrome(chrome_options=options ,executable_path='./chromedriver')
browser = webdriver.Chrome(executable_path='./chromedriver')
browser.get("https://www.google.com/maps/")


def search_place():
    Place = browser.find_element(By.CLASS_NAME,'tactile-searchbox-input')
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


def find_latest_sorting_tag():
    sorting_tag = browser.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button/span')
    sorting_tag.click()
    print("click sorting tag")
    latest_link= browser.find_element(By.XPATH, '//*[@id="action-menu"]/div[2]')
    latest_link.click()
    print("click latest tag")
    # //*[@id="action-menu"]/div[2]

def scroll_data(counter):
    last_height = browser.execute_script("return document.body.scrollHeight")
    print('scrolling... ', last_height)

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


def scroll_the_page():
		try:
			WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root")))
			pause_time = 2
			max_count = 5
			x = 0

			while(x<max_count):
				scrollable_div = browser.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
				try:
					browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
				except:
					pass
				time.sleep(pause_time)
				x=x+1
		except:
			browser.quit()



def scroll_data2(counter):
    last_height = browser.execute_script("return document.body.scrollHeight")
    print('scrolling... ', last_height)

    for _i in range(counter):
        h = browser.execute_script("return document.body.scrollHeight")
        ele = browser.find_element( By.XPATH,'//*[@id="QA0Szd"]')
        browser.execute_script('arguments[0].scrollBy(0, 2000);', ele) 
        # browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        print("AAAA",_i,"/",counter,h)
        # get_data()
        time.sleep(3)

def scroll_too():
    last_height = browser.execute_script("return document.body.scrollHeight")
    SCROLL_PAUSE_TIME = 5

    number = 0

    while True:
        number = number+1

    # Scroll down to bottom
        # ele = browser.find_element( By.XPATH,'//*[@id="QA0Szd"]') 
        ele = browser.find_element( By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
        browser.execute_script('arguments[0].scrollBy(0, 2000);', ele)

    # Wait to load page

        time.sleep(2)

    # Calculate new scroll height and compare with last scroll height
        print(f'last height: {last_height}')
        #//*[@id="QA0Szd"]
        # ele = browser.find_element( By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
        ele = browser.find_element( By.XPATH,'//*[@id="QA0Szd"]')
        new_height = browser.execute_script("return arguments[0].scrollHeight", ele)

        print(f'new height: {new_height}')

        if number == 5:
            break

        if new_height == last_height:
            break

        print('cont')
        last_height = new_height

def test2():

    # 設定等待時間和滾動步長
    WAIT_TIME = 10
    SCROLL_STEP = 1000

    # 定位到滾動區域的元素
    scroll_area = browser.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')

    # 獲取網頁內容的高度
    last_height = browser.execute_script("return arguments[0].scrollHeight", scroll_area)

    # 持續滾動，直到滾動到頁面底部
    while True:
        # 滾動一個步長
        browser.execute_script('arguments[0].scrollBy(0, arguments[1]);', scroll_area, SCROLL_STEP)

        try:
            # 等待頁面內容加載完畢
            WebDriverWait(browser, WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[last()]')))
        except:
            # 如果超時，則停止滾動
            break

        # 獲取滾動後的網頁內容高度
        new_height = browser.execute_script("return arguments[0].scrollHeight", scroll_area)

        # 如果滾動到頁面底部，則停止滾動
        if new_height == last_height:
            break

        # 更新 last_height
        last_height = new_height



if __name__ == "__main__":
    print('start')
    time.sleep(1.5)

    search_place()
    num = find_review_link()
    print(num)
    time.sleep(3)
    find_latest_sorting_tag()
 
    # scroll_data2(int(int(num)/10)+1)
    # scroll_too()
    test2()

    # get_data()
    
    time.sleep(30) 

    print('End')
