import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor, wait,as_completed

from datetime import datetime


driver=webdriver.Chrome()
driver.get('https://www.alaedin.travel/account/login')
driver.find_element(By.XPATH,'//input[@name="userName"]').clear()
driver.find_element(By.XPATH,'//input[@name="userName"]').send_keys('0920262961')


driver.find_element(By.XPATH,'//input[@name="password"]').clear()
driver.find_element(By.XPATH,'//input[@name="password"]').send_keys('MST1231020')

driver.find_element(By.XPATH,'//button[@type="submit"]').click()





print('asdasd')