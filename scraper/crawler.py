from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
    review_link= browser.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span')
    total_num = review_link.text.strip(' 則評論')
    total_num = total_num.replace(',','')
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





if __name__ == "__main__":
    print('start')
    time.sleep(1.5)

    search_place()
    num = find_review_link()
    print(num)
    time.sleep(3)
    find_latest_sorting_tag()
 
    


    
    time.sleep(30) 

    print('End')
