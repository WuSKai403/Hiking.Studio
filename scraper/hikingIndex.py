from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from env_crawler import hiking_index_url,driver_path,options



browser = webdriver.Chrome(chrome_options=options ,executable_path=driver_path)
# browser = webdriver.Chrome(executable_path='./chromedriver')
browser.get(hiking_index_url)



def search_place():
    Place = browser.find_element(By.CLASS_NAME,'tactile-searchbox-input')
    Place.send_keys("金面山親山步道")
    submit = browser.find_element(By.ID,"searchbox-searchbutton")
    print(submit.text)
    submit.click()
    # time.sleep(15)
    print('search key word finish')
