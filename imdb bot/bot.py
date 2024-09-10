from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import json

def get_people(driver, element_xpath):
    elements = driver.find_elements(By.XPATH, element_xpath)
    people = []
    for li in elements:
        try:
            a_elements = li.find_elements(By.TAG_NAME, "a")
            for a_element in a_elements:
                text_content = driver.execute_script("return arguments[0].textContent;", a_element)
                people.append(text_content)
        except Exception as e:
            print("Hata:", e)
    return people


def get_genre(driver,element_class):
    element=driver.find_element(By.CLASS_NAME,element_class)
    elements=element.find_elements(By.TAG_NAME,"span")
    genre=[]
    for i in range(len(elements)):
        text_content=driver.execute_script("return arguments[0].textContent;", elements[i])
        genre.append(text_content)
    return genre

def find_element_with_alternatives(driver, xpaths):
    for xpath in xpaths:
        try:
            element = driver.find_element(By.XPATH, xpath)
            return element
        except NoSuchElementException:
            continue
    return None

data_list=[]


driver = webdriver.Chrome()

driver.get("https://www.imdb.com")
wait = WebDriverWait(driver, 10)

element1 = wait.until(EC.element_to_be_clickable((By.ID, "imdbHeader-navDrawerOpen")))
element1.click()

element2 = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/nav/div[2]/aside[1]/div/div[2]/div/div[1]/span/div/div/ul/a[2]/span")))
element2.click()

reklam = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/button[1]")))
reklam.click()

element4 = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul")))
li_element4_name = element4.find_elements(By.CLASS_NAME, "ipc-title-link-wrapper")

for i in range(len(li_element4_name)):
    element4 = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul")))
    li_element4_name = element4.find_elements(By.CLASS_NAME, "ipc-title-link-wrapper")
    driver.execute_script("arguments[0].scrollIntoView();", li_element4_name[i])
    time.sleep(5)
    li_element4_name[i].click()
    name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "hero__primary-text")))

    year = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a")
    xpaths = [
        "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]",
        "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[2]",
    ]
    t=find_element_with_alternatives(driver, xpaths)
    star = driver.find_element(By.CSS_SELECTOR, ".sc-eb51e184-1.ljxVSS")    
    
    genre=get_genre(driver,"ipc-chip-list__scroller")
    directors = get_people(driver, "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[2]/div/ul/li[1]/div")
    writers = get_people(driver, "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[2]/div/ul/li[2]/div")   
    stars = get_people(driver, "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[2]/div/ul/li[3]/div")
    
  
    data={
    'Name':name.text,
    'Year':year.text,
     'Time':t.text,
     'Rate':star.text,
     'Genre':genre,
     'Directors':directors,
     'Writers':writers,
     'Stars':stars
     }

    data_list.append(data)
    with open('data.json','w',encoding='utf-8') as f:
        json.dump(data_list,f,ensure_ascii=False,indent=4)

    
    
    driver.back()
    time.sleep(5)

driver.quit()