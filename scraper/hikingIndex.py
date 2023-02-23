from bs4 import BeautifulSoup
from env_crawler import hiking_index_url,driver_path,options
import requests
from models import Attraction
import csv

# browser = webdriver.Chrome(chrome_options=options ,executable_path=driver_path)
# browser = webdriver.Chrome(executable_path='./chromedriver')
# browser.get(hiking_index_url)

def check_req_status(id):
    r = requests.get(hiking_index_url+str(id))
    if r.status_code != requests.codes.ok:
        print(r)
        return False
    else:
        get_data(r,id)
        return True

def get_data(r,id):
    soup = BeautifulSoup(r.text, "html5lib")
    title = soup.find(class_="text-3xl").getText()
    text = soup.find(class_="leading-relaxed").getText()
    loc = soup.find(class_="flex-1 p-4").getText()
    writer.writerow([id,title,text, loc,hiking_index_url+str(id)])
    print(id,title , loc)


if __name__ == "__main__":
    with open('Location.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id','title', 'text','loc','hiking_url'])

    for id in range(1750):
        if check_req_status(id)==True:
            print(hiking_index_url+str(id)) 
            # Attraction.source_url = hiking_index_url+id 
