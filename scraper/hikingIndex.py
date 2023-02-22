# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from env_crawler import hiking_index_url,driver_path,options
import requests
from models import Attraction


# browser = webdriver.Chrome(chrome_options=options ,executable_path=driver_path)
# browser = webdriver.Chrome(executable_path='./chromedriver')
# browser.get(hiking_index_url)

def check_req_status(id):
    r = requests.get(hiking_index_url+str(id))
    if r.status_code != requests.codes.ok:
        print(r)
        return False
    else:
        return True


if __name__ == "__main__":

    for id in range(1750):
        if check_req_status(id)==True:
            print(hiking_index_url+str(id)) 
            # Attraction.source_url = hiking_index_url+id 
