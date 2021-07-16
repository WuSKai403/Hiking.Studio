#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium.webdriver import Firefox
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import time
from selenium.common.exceptions import TimeoutException
import random
import csv
import os
from tqdm.notebook import tqdm


# In[2]:


fp = pd.read_excel('clean_new_trail_list.xlsx')

def get_related_words():
    try:
        related_words = driver.find_elements_by_class_name("Ph5evf-qwU8Me-GGk1K")
        related_words = [i.text for i in related_words]
        rm_strings = ['餐廳','飯店','名勝景點','大眾運輸','停車場','藥局','全部']
        for s in rm_strings:
            related_words.remove(s)
        for i in range(len(related_words)):
            related_words[i] = related_words[i].replace('\n',"_")
        return(related_words)
    except:
        return("no related words")

def id_keywords(i):
    try:
        trail_id = fp.iloc[i]['trail_id']
        key_words = eval(fp.iloc[i]['find_place'])
        return(trail_id,key_words)
    except:
        return (trail_id,False)
    

def check_digits(all_review_button):
    num_of_comments = all_review_button.text.split(' ')[0]
    try:
        num_of_comments = int(num_of_comments)
    except:
        num_of_comments = int(num_of_comments.replace(',',''))
    return(num_of_comments)

def scroll_page(num_of_comments):
    scroll_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.section-scrollbox')))
   
    for i in tqdm(range(int(num_of_comments/10)+1)):
        time.sleep(3)
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',scroll_box)
        review_name = driver.find_elements_by_class_name("ODSEW-ShBeI-title")
        num_com = len(review_name)

def scroll_times(num_of_comments):
    if num_of_comments%10 == 0:
        scroll_times = num_of_comments/10
    else:
        scroll_times = int(num_of_comments/10)+1
    return(scroll_times)
        
        
def scroll_page1(num_of_comments):
    tmp = 0
    st = int(num_of_comments/10)
    scroll_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.section-scrollbox')))
    with tqdm(total = st-1) as pbar:
        i = 0
        while(i<st):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',scroll_box)
            time.sleep(1)
            review_text = driver.find_elements_by_class_name("ODSEW-ShBeI-text") 
            #print(len(review_name))
            scroll_times_re=scroll_times(len(review_text))#目前滾了幾次        
            #print("目前滾動次數:{}".format(scroll_times_re))
            if tmp != scroll_times_re:
                pbar.update()
                tmp = scroll_times_re
                #print(tmp)
                i = scroll_times_re
                                                     
def expand_all_reviews():
    try:
        element = driver.find_elements_by_css_selector(".ODSEW-KoToPc-ShBeI")
        for i in element:
            i.click()
    except:
        pass
    
def get_review_data():
    review_text = driver.find_elements_by_class_name("ODSEW-ShBeI-text")
    review_name = driver.find_elements_by_class_name("ODSEW-ShBeI-title")
    review_star = driver.find_elements_by_class_name("ODSEW-ShBeI-H1e3jb")
    review_date = driver.find_elements_by_class_name("ODSEW-ShBeI-RgZmSc-date")
    review_text_list = []
    for a in review_text:
        text = a.text.replace('\n','')
        review_text_list.append(text)
        
    review_name_list = [a.text for a in review_name]
    review_date_list = [a.text for a in review_date]
    review_star_list = [a.get_attribute("aria-label") for a in review_star]
    
    location_data = []
    
    for a in zip(review_name_list,review_date_list,review_star_list,review_text_list):
        location_data.append(a)
    return(location_data)

def write_csv(location_data,file_name,related_words):
    path = 'results'
    path = os.path.join(path,file_name)
    with open(path,'w',encoding = 'utf-8',newline='') as f:
        headers = ['name','published_date','star','review','key_review']
        csv_out=csv.writer(f)
        if related_words[0] != "no related words":
            csv_out.writerow(related_words)
        csv_out.writerow(headers)
        csv_out.writerows(location_data)
        f.close()


# In[ ]:


#path = r"C:\Users\USER\Downloads\geckodriver.exe"#driver path
error_list = []
for i in range(0,10):
    key_words = id_keywords(i)[1]
    trail_id = id_keywords(i)[0]
    if key_words != False:
        for key_word in key_words:
            try:
                file_name = str(trail_id)+"_"+str(key_word)+'.csv'
                print("=========================================================================")
                print("processing {}".format(file_name))
                driver = Firefox(executable_path = path)
                driver.get('https://www.google.com.tw/maps/@24.9561947,121.1824813,15z') 
                search_place = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'searchboxinput')))
                search_place.send_keys(key_word)
                search_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'searchbox-searchbutton')))
                search_button.click()
                time.sleep(5)
                try:
                    #get avg rating stars of the place(avg_rating_stars.text)
                    avg_rating_stars = driver.find_element_by_css_selector('.gm2-display-2')
                except:
                    to_right_page = driver.find_element_by_css_selector('div:nth-child(1) > .V0h1Ob-haAclf > .a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd')
                    to_right_page.click()
                    time.sleep(2)
                    avg_rating_stars = driver.find_elements_by_css_selector('.gm2-display-2')
                #get rating stars and total number of ratings
                all_review_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.OAO0-ZEhYpd-vJ7A6b > span > .widget-pane-link')))
                #check total comment
                num_of_comments = check_digits(all_review_button)
                print("total coments:{}".format(num_of_comments))
                #get into comments page
                all_review_button.click()
                time.sleep(5)
                related_words = get_related_words()
                print(related_words)

                #scroll pages
                scroll_page1(num_of_comments)
                expand_all_reviews()
                location_data = get_review_data()
                write_csv(location_data,file_name,related_words)
                driver.quit()
                time.sleep(2)
                print("=========================================================================")
            except Exception as e:
                print("something wrong at {}".format(file_name))
                print(e)
                error_list.append(file_name)
                driver.quit()
                pass
                
    else:
        print("this trail id {} has no results".format(trail_id))
        pass


# In[ ]:


print(error_list)

