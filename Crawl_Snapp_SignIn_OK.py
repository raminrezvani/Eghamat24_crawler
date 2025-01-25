import os
os.system("title Crawl Snapp SignIn OK")
import os
import json
import requests
import time
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from insert_influx import Influxdb
influx = Influxdb()
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=100)  # Adjust the max_workers based on your needs
executor_room = ThreadPoolExecutor(max_workers=100)  # Adjust the max_workers based on your needs

token='ee14f8316cb5ca88776ed7ad50b109d6e25f56722e6dbefdf6e35929d847bcd7c5f7e06c80f717c6dd8cb040bc38fcebc12f'
# Function to get hotel data
def fetch_hotel_data(city_id, date_from, date_to, page):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://business.snapptrip.com',
        'Referer': 'https://business.snapptrip.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-auth-id':  token,  # Replace with actual auth ID
    }
    params = {
        'date_from': date_from,
        'date_to': date_to,
        'orderBy': 'selling',
        'page': str(page),
        'city_id': city_id,
    }
    while True:
        try:
            response = requests.get('https://business2.snapptrip.com/service2/hotelbooking/hotels', params=params, headers=headers)
            influx.capture_logs(1, 'Snapp')
            return json.loads(response.text)
        except:
            print(f'Retrying page {page}...')
            time.sleep(2)

# Function to get room data for a specific hotel
def fetch_room_data(hotelID, date_from, date_to):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://business.snapptrip.com',
        'Referer': 'https://business.snapptrip.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-auth-id':token
    }
    params = {
        'date_from': date_from,
        'date_to': date_to,
        'hotel_id': hotelID,
        'page': '1',
    }
    while True:
        try:
            response = requests.get('https://business2.snapptrip.com/service2/hotelbooking/hotels', params=params, headers=headers)
            influx.capture_logs(1, 'Snapp')
            return json.loads(response.text)
        except:
            print(f'Retrying room data for hotel {hotelID}...')
            time.sleep(2)

# Flask endpoint to get room data
@app.route('/SnappTrip_Hotelrooms', methods=['GET'])
def get_hotel_rooms():
    city_id = request.args.get('city_id')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    lst_hotels = []

    futures = []
    for i in range(1, 10):  # Assuming 4 pages of hotels
        futures.append(executor.submit(fetch_hotel_data, city_id, date_from, date_to, i))

    for future in as_completed(futures):
        json_data = future.result()
        for htl in json_data['data']:
            hotelName = htl['title']
            hotelID = htl['id']
            hotel = {
                'hotel_name': hotelName,
                'hotel_star': htl['stars'],
                'min_price': '',
                'provider': 'Snapp',
                'rooms': []
            }
            # Fetch room data in a new thread
            room_data_future = executor_room.submit(fetch_room_data, hotelID, date_from, date_to)

            json_data_room = room_data_future.result()
            rooms = json_data_room['data'][0]['rooms']
            for rom in rooms:
                available_rooms=rom['available_rooms']
                if (rom['available_rooms']==0):
                    continue

                room = {
                    'name': rom['title'],
                    'price': rom['prices']['local_price_off'],
                    'capacity':rom['adults'],
                    'provider': 'Snapp',
                }
                hotel['rooms'].append(room)
            lst_hotels.append(hotel)

    return jsonify(lst_hotels)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, threaded=False)



#============== Old Code ========
# import os
# import json
# import requests
# import jdatetime
# from datetime import datetime, timedelta
# from flask import Flask, request, jsonify
# # from concurrent.futures import ThreadPoolExecutor
# # from seleniumwire import webdriver
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# # Function to get the Shamsi date seven days from now
# import time
# # Setup Flask app
# app = Flask(__name__)
# # executor = ThreadPoolExecutor(max_workers=1)
#
# # Endpoint to get room data
# @app.route('/SnappTrip_Hotelrooms', methods=['GET'])
# def get_hotel_rooms():
#     city_id=request.args.get('city_id')
#     date_from=request.args.get('date_from')
#     date_to=request.args.get('date_to')
#     lst_hotels=[]
#
#     # city_id='6326'
#     # date_from='2024-11-08'
#     # date_to='2024-11-11'
#     # lst_hotels=[]
#
#
#     # params = {
#     #     'date_from': '2024-11-05',
#     #     'date_to': '2024-11-08',
#     #     'city_id': '6326',
#     # }
#     #
#
#
#     #--- get hotels with sign
#     import requests
#
#     headers = {
#         'Accept': '*/*',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Connection': 'keep-alive',
#         'Content-Type': 'application/json',
#         'Origin': 'https://business.snapptrip.com',
#         'Referer': 'https://business.snapptrip.com/',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-site',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
#         'lang': 'fa',
#         'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'x-auth-id': 'e1e748bb6926fcc842d8fcf22f9604a8c5ad6d346c6c001e2f3ca53c65cc510981fb7b7d6ae7b829cbf7b8891ca30919920a',
#     }
#     for i in range(1,5):
#         params = {
#             'date_from': date_from,
#             'date_to': date_to,
#             'orderBy': 'selling',
#             'page': str(i),
#             # 'sourceName': 'کیش',
#             'city_id': city_id,
#             # 'sourceName': 'کیش',
#             # 'city_id': '6918',
#         }
#         while(True):
#             try:
#                 response = requests.get('https://business2.snapptrip.com/service2/hotelbooking/hotels', params=params,
#                                         headers=headers)
#                 print(f'successfull get {i}')
#                 break
#             except:
#                 print('Try again ...')
#                 time.sleep(2)
#
#
#
#         json_data=json.loads(response.text)
#
#         for htl in json_data['data']:
#             hotelName=htl['title']
#             hotelID=htl['id']
#
#             #--- get rooms
#
#             # --- get rooms
#             params = {
#                 'date_from': date_from,
#                 'date_to': date_to,
#                 'hotel_id': hotelID,
#                 'page': '1',
#                 # 'sourceName': 'آریا',
#             }
#
#             response = requests.get('https://business2.snapptrip.com/service2/hotelbooking/hotels', params=params,
#                                     headers=headers)
#
#
#             hotel = {}
#             hotel['hotel_name'] = hotelName
#             hotel['hotel_star'] = htl['stars']
#             hotel['min_price'] = ''
#             hotel['provider'] = 'Snapp'
#             hotel['rooms'] = []
#
#             #---- strucure of hotel and rooms
#             json_data_room=json.loads(response.text)
#             rooms=json_data_room['data'][0]['rooms']
#             for rom in rooms:
#                 # if (rom['available_rooms']==0):
#                 #     continue
#
#                 roomName=rom['title']
#                 roomPrice=rom['prices']['local_price_off']
#
#                 room={
#                     'name':roomName,
#                     'price': roomPrice,
#                     'provider': 'Snapp',
#                 }
#                 hotel['rooms'].append(room)
#
#             lst_hotels.append(hotel)
#             # print(f'hotelName == {hotelName}')
#             #----
#     return lst_hotels
#
#
# # get_hotel_rooms()
#
# if __name__ == '__main__':
#     # #--- get cookies -----------
#     # d1,d2 = get_shamsi_date()
#     # output_file = "SnapTrip_cookies.json"
#     # # Load existing cookies and headers or retrieve them from Alaedin if not available
#     # request_headers, cookies_dict = load_cookies_and_headers(output_file)
#     # if not request_headers or not cookies_dict:
#     #     # url = f'https://www.alaedin.travel/hotels/kish/arya/{shamsi_date_api}/3'
#     #     url=f'https://www.snapptrip.com/%D8%B1%D8%B2%D8%B1%D9%88-%D9%87%D8%AA%D9%84/%DA%A9%DB%8C%D8%B4/%D9%87%D8%AA%D9%84-%D8%A2%D8%B1%DB%8C%D8%A7?date_from={d1}&date_to={d2}&city_name=%DA%A9%DB%8C%D8%B4&source=searchBox'
#     #     request_headers, cookies_dict = get_Snapp_cookies_headers(url, output_file)
#     # #------------
#     #
#     app.run(host='0.0.0.0', port=5004,threaded=False)
#
#
# #==== example
# #
# # import requests
# # url = 'http://localhost:5003/SnappTrip_Hotelrooms'
# # params = {
# #     'date_from': '2024-11-05',
# #     'date_to': '2024-11-08',
# #     'city_id': '6326',
# # }
# #
# # response = requests.get(url, params=params)
#
#
# # get_hotels('6326','2024-11-05','2024-11-08')
#
#
# #
# # hotel = {}
# # hotel['hotel_name'] = ''
# # hotel['hotel_star'] = ''
# # hotel['min_price'] = ''
# # hotel['provider'] = ''
# # hotel['rooms'] = [
# #     {
# #         'name': '',
# #         'price': '',
# #         'provider': '',
# #     }
# # ]
# # pass
#
# #
