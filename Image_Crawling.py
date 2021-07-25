import os
import time
import urllib
import uuid
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


keyword = input('수집할 이미지 입력 : ')
path = 'C:/Users/Min/AppData/Roaming/JetBrains/PyCharmCE2021.1/scratches/{0}'.format(keyword)

try:
  if not os.path.exists(path):
    os.makedirs(path)
except OSError:
  print('Error : Creating directory.' + path)

driver = webdriver.Chrome('C:/Users/Min/AppData/Roaming/JetBrains/PyCharmCE2021.1/scratches/chromedriver.exe', options=chrome_options)
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
elem = driver.find_element_by_name("q")
elem.send_keys(keyword)
elem.send_keys(Keys.RETURN)

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector(".n3VNCb").click()
        except:
            break
    last_height = new_height

count = 1
images = driver.find_elements_by_css_selector(".wXeWr.islib.nfEiy")
for image in images:
    try:
        image.click()
        time.sleep(2)
        imgUrl = driver.find_element_by_xpath(
            '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img').get_attribute(
            "src")
        file_ext=imgUrl.split(".")[-1]
        file_name = uuid.uuid4()
        urllib.request.urlretrieve(imgUrl, "{}/{}.{}".format(path,file_name,file_ext))
        print("{}.{} 저장완료, {}개 저장완료".format(file_name,file_ext,count))
        count += 1
    except:
        pass