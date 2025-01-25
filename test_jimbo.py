import requests
# # ==========ssssssssss test Booking =======
# # urll = "http://45.149.76.168:5002/booking_hotels"
# urll = "http://127.0.0.1:5002/booking_hotels"
# params = {
#     'start_date': '2024-12-21',
#     'end_date': '2024-12-24',
#     'adults': '2',
#     'target': 'KIH'
# }
# response = requests.get(urll, params=params)
# data = response.json()
# print(data)
# # =============

# ==========ssssssssss -===== test Jimbo ========
# urll = "http://45.149.76.168:5020/Jimbo_hotels"
urll = "http://127.0.0.1:5020/Jimbo_hotels"
params = {
    'start_date': '2024-12-21',
    'end_date': '2024-12-24',
    'adults': '2',
    'target': 'KIH'
}
response = requests.get(urll, params=params)
data = response.json()
print(data)
# =============




#
# #================ test booking ===========
# # 'mobile': '09153148721',
# # 'password': '@MST8451030yf',
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# driver=webdriver.Chrome()
# driver.get('https://www.booking.ir/sign-in/')
# print('Signed in...')
#
# try:
#     driver.find_element(By.XPATH,'//input[@id="Mobile"]').clear()
#     driver.find_element(By.XPATH,'//input[@id="Mobile"]').send_keys('09153148721')
# except:
#     ''
# driver.find_element(By.XPATH,'//span[contains(text(),"ورود با رمز ثابت")]/..').click()
# time.sleep(1)
# driver.find_elements(By.XPATH,'//input[@placeholder="رمز عبور ثابت"]')[1].clear()
# driver.find_elements(By.XPATH,'//input[@placeholder="رمز عبور ثابت"]')[1].send_keys('@MST8451030yf')
#
# driver.find_elements(By.XPATH,'//span[text()="ورود"]/..')[-1].click()
#
# time.sleep(1)
# if (driver.current_url=="https://www.booking.ir/account/companies/?returnUrl=/"):
#     print('In page mojalal safar...')
#     driver.find_element(By.XPATH,'//button[contains(text(),"مجلل سفر طلایی")]').click()
#
#
# #== get cookie
# # Retrieve cookies
# import json
# cookies = driver.get_cookies()
# # Save cookies to a JSON file
# with open("cookies.json", "w") as file:
#     json.dump(cookies, file)
#
#
# # #============
# # driver.find_element(By.XPATH,'//label[text()="شماره موبایل خود را وارد کنید"]/../div[@class="sign-up__input-inner"]/input[@id="Mobile"]').clear()
# # driver.find_element(By.XPATH,'//label[text()="شماره موبایل خود را وارد کنید"]/../div[@class="sign-up__input-inner"]/input[@id="Mobile"]').send_keys('09153148721')
#
# # driver.find_element(By.XPATH,'//input[@id="Mobile"]').send_keys('09153148721')
#
#
#
#

