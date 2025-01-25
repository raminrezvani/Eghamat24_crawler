import os
import json
import requests
import jdatetime
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
# from concurrent.futures import ThreadPoolExecutor
# from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
# Function to get the Shamsi date seven days from now
def get_shamsi_date():
    d1 = datetime.now() + timedelta(days=4)
    d2 = datetime.now() + timedelta(days=7)
    return str(d1.date()),str(d2.date())

# Function to load cookies and headers from a JSON file
def load_cookies_and_headers(output_file):
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            data = json.load(f)
            return data.get("request_headers", {}), data.get("cookies_dict", {})
    return None, None

# Function to save cookies and headers to a JSON file
def save_cookies_and_headers(output_file, headers, cookies):
    with open(output_file, 'w') as f:
        json.dump({"request_headers": headers, "cookies_dict": cookies}, f, indent=4)

def sign_IN(driver):
    # driver.set_page_load_timeout(20)
    while(True):
        try:
            driver.get('https://www.alaedin.travel/account/login')
            driver.find_element(By.XPATH, '//input[@name="userName"]').clear()
            driver.find_element(By.XPATH, '//input[@name="userName"]').send_keys('0920262961')

            driver.find_element(By.XPATH, '//input[@name="password"]').clear()
            driver.find_element(By.XPATH, '//input[@name="password"]').send_keys('MST1231020')

            driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            print('SingIn Successfull!')
            break
        except:
            print('error in SignIN --- retry ...')


# Function to get headers and cookies from Alaedin website
def get_Snapp_cookies_headers(url, output_file):
    options = webdriver.ChromeOptions()
    with webdriver.Chrome(seleniumwire_options={}, options=options) as driver:
        #-- sign in
        # sign_IN(driver)

        driver.get(url)

        # Filter for the specific API request
        for request in driver.requests:
            if "rooms?" in request.url and request.response:
                print('asd')
                request_headers = dict(request.headers)
                request_cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
                # print(request_cookies)
                save_cookies_and_headers(output_file, request_headers, request_cookies)
                return request_headers, request_cookies
    return {}, {}

import time
# Setup Flask app
app = Flask(__name__)
# executor = ThreadPoolExecutor(max_workers=1)

# Endpoint to get room data
@app.route('/SnappTrip_Hotelrooms', methods=['GET'])
def get_hotel_rooms():
    city_id=request.args.get('city_id')
    date_from=request.args.get('date_from')
    date_to=request.args.get('date_to')
    lst_hotels=[]

    #-- get hotel ---
    params = {
        'city_id': int(city_id),
        'date_from': date_from,
        'date_to': date_to,
        'page': '1',
        'order_by': 'selling',
        'token': 'Jek',
    }

    while(True):
        response = requests.get('https://hapi.snapptrip.com/hotel/api/v2/search-city', params=params)
        if (response.status_code==200):
            break
        else:
            time.sleep(2)
            continue

    json_data=json.loads(response.text)

    for htl in json_data['data']:
        hotelName=htl['url'].replace('-',' ')
        hotelID=htl['id']

        #--- get rooms
        params = {
            'date_from': date_from,
            'date_to': date_to,
            'token': 'Jek',
        }
        response = requests.get(f'https://hapi.snapptrip.com/hotel/api/v2/hotels/{hotelID}/rooms', params=params)


        hotel = {}
        hotel['hotel_name'] = hotelName
        hotel['hotel_star'] = ''
        hotel['min_price'] = ''
        hotel['provider'] = 'Snapp'
        hotel['rooms'] = []

        #---- strucure of hotel and rooms
        json_data_room=json.loads(response.text)
        for rom in json_data_room:
            if (rom['available_rooms']==0):
                continue

            roomName=rom['title']
            roomPrice=rom['prices']['local_price']

            room={
                'name':roomName,
                'price': roomPrice,
                'provider': 'Snapp',
            }
            hotel['rooms'].append(room)

        lst_hotels.append(hotel)
        print(f'hotelName == {hotelName}')
        #----
    return lst_hotels




if __name__ == '__main__':
    # #--- get cookies -----------
    # d1,d2 = get_shamsi_date()
    # output_file = "SnapTrip_cookies.json"
    # # Load existing cookies and headers or retrieve them from Alaedin if not available
    # request_headers, cookies_dict = load_cookies_and_headers(output_file)
    # if not request_headers or not cookies_dict:
    #     # url = f'https://www.alaedin.travel/hotels/kish/arya/{shamsi_date_api}/3'
    #     url=f'https://www.snapptrip.com/%D8%B1%D8%B2%D8%B1%D9%88-%D9%87%D8%AA%D9%84/%DA%A9%DB%8C%D8%B4/%D9%87%D8%AA%D9%84-%D8%A2%D8%B1%DB%8C%D8%A7?date_from={d1}&date_to={d2}&city_name=%DA%A9%DB%8C%D8%B4&source=searchBox'
    #     request_headers, cookies_dict = get_Snapp_cookies_headers(url, output_file)
    # #------------
    #
    app.run(host='0.0.0.0', port=5004,threaded=False)


#==== example
#
# import requests
# url = 'http://localhost:5003/SnappTrip_Hotelrooms'
# params = {
#     'date_from': '2024-11-05',
#     'date_to': '2024-11-08',
#     'city_id': '6326',
# }
#
# response = requests.get(url, params=params)


# get_hotels('6326','2024-11-05','2024-11-08')


#
# hotel = {}
# hotel['hotel_name'] = ''
# hotel['hotel_star'] = ''
# hotel['min_price'] = ''
# hotel['provider'] = ''
# hotel['rooms'] = [
#     {
#         'name': '',
#         'price': '',
#         'provider': '',
#     }
# ]
# pass

#
