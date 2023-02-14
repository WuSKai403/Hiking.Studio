from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time



options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

browser = webdriver.Chrome(chrome_options=options ,executable_path='./chromedriver')
browser.get("https://www.google.com/maps/")

if __name__ == "__main__":
    print('start')
    time.sleep(2)

    Place = browser.find_element(By.CLASS_NAME,'tactile-searchbox-input')
    Place.send_keys("Paris")
    submit = browser.find_element(By.ID,"searchbox-searchbutton")
    print(submit.text)
    submit.click()
    print('search place final')
    print('End')
    time.sleep(30)