
from concurrent.futures import ThreadPoolExecutor, wait,as_completed


import urllib3

from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import jdatetime

from lxml import etree
from io import StringIO
import requests

class Alaedin:
    def __init__(self, target, start_date, end_date, adults):
        self.target = target
        self.start_date = start_date
        self.end_date = end_date
        self.adults = adults
        self.executor = ThreadPoolExecutor(max_workers=50)

        self.cookies = []
        self.destin_text={
            'KIH':'kish',

        }
    def get_rooms(self,hotelCod, start_date, stay):
        # Define the parameters
        params = {
            # 'hotelCod': '1006',  # Example hotel code
            'hotelCod': hotelCod,  # Example hotel code
            'start_date': start_date,  # Example Shamsi date in 'yyyyMMdd' format
            'stay': stay  # Example stay duration in nights
        }

        # Send a GET request to the API
        response = requests.get("http://45.149.76.168:5003/Alaedin_rooms", params=params)
        json_data = json.loads(response.text)
        rooms = []
        for i in range(len(json_data['room'])):
            room = {}
            room['name'] = json_data['room'][i]['roomTypeName']
            room['price'] = json_data['room'][i]['price']
            room['provider'] = 'Alaedin'
            rooms.append(room)

        return rooms


    def get_result(self):
        try:

            start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
            shamsi_start_date = jdatetime.date.fromgregorian(date=start_date)
            shamsi_start_date_hotel=str(shamsi_start_date).replace('-','')

            end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
            stay_duration = (end_date - start_date).days

            # aa = requests.get('https://www.alaedin.travel/hotels/kish/14030803/3')
            aa = requests.get(f'https://www.alaedin.travel/hotels/kish/{shamsi_start_date_hotel}/{stay_duration}')
            # ==parsing
            parser = etree.HTMLParser()
            htmlparsed = etree.parse(StringIO(aa.text), parser=parser)
            lst_hotels = htmlparsed.xpath('//div[contains(@class,"hotel-box")]')
            res_lst_hotels = list()
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_hotel = {}
                for hotel in lst_hotels:
                    hotelName = hotel.xpath('.//div[@class="hotel-name"]/text()')[0]
                    hotelCode = hotel.xpath('.//input[@class="hotelCode"]')[0].get('value')
                    # hotelHref='https://www.alaedin.travel'+hotel.xpath('./../@href')[0]

                    hotel_data = {}
                    hotel_data['hotel_name'] =hotelName
                    hotel_data['hotel_star'] = ''
                    hotel_data['min_price'] =''
                    hotel_data['provider'] = 'Alaedin'
                    hotel_data['rooms'] = []
                    # == get rooms
                    future = executor.submit(self.get_rooms, hotelCode, str(shamsi_start_date), stay_duration)
                    future_to_hotel[future] = hotel_data  # Keep track of hotel data

                # Collect results as they complete
                for future in as_completed(future_to_hotel):
                    hotel_data = future_to_hotel[future]
                    try:
                        hotel_data['rooms'] = future.result()  # Get the result from the future
                    except Exception as exc:
                        print(f'Error fetching rooms for {hotel_data["hotel_name"]}: {exc}')


                    res_lst_hotels.append(hotel_data)

            return res_lst_hotels

        except:
            return {'status': False, "data": [], 'message': "اتمام زمان"}







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
# #=== Alaedin ===
#
# Alaedin=Alaedin('KIH','2024-10-30','2024-11-04','2')
# Alaedin.get_result()
# #===========
