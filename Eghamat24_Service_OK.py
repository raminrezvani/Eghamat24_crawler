import os
os.system("title Crawl Eghamat24_service_OK")
from flask import Flask, jsonify, request
import json
from lxml import etree
from io import StringIO
from concurrent.futures import ThreadPoolExecutor
import requests
from insert_influx import Influxdb
influx = Influxdb()

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=100)
# executor = ThreadPoolExecutor(max_workers=1)
class Eghamat24:
    def __init__(self, target='MHD', startdate='2024-10-16', stay='3'):
        self.target = target
        self.startdate = startdate
        self.stay = stay
        # self.executor = ThreadPoolExecutor(max_workers=100)
        self.hotelResults = list()

    def convert_to_number(self, persian_number):
        persian_to_arabic = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
        converted_number = persian_number.translate(persian_to_arabic).replace(',', '')
        try:
            return int(converted_number)
        except:
            return 'نامشخص'

    def get_one_hotel_Data(self, hotel):
        property_id = hotel['property_id']
        url = f'https://www.eghamat24.com/property-rooms/list-view?property_id={property_id}&check_in={self.startdate}&length_of_stay={self.stay}'
        res = requests.get(url).text
        influx.capture_logs(1, 'Eghamat24')
        parser = etree.HTMLParser()
        htmlparsed = etree.parse(StringIO(res), parser=parser)


        lst_hotelRow=htmlparsed.xpath('//div[contains(@class,"p-room card")]')


        lst_items = [a.xpath('.//div[@class="mb-3 mb-md-4"]')[0] for a in lst_hotelRow]
        lst_items_text = [' '.join(a.xpath('span/text()')).split('\r')[0] for a in lst_items]
        lst_prices =[a.xpath('.//div[@class="subtitle-3 fw-semibold fw-md-bold"]/text()')[0] for a in lst_hotelRow]
        lst_prices_text = [a.replace('\r\n', '').replace('تومان', '').strip() for a in lst_prices]

        lst_capacities = [a.xpath('.//div[@class="d-flex flex-wrap body-2 mb-3 mb-md-2"]/span/text()')[0] for a in lst_hotelRow]
        lst_capacities_text = [a.replace('\r\n', '').split('نفر')[0].replace('نفره', '').replace('-', '').replace('  ', '').strip() for a in lst_capacities]
        # lst_buttons = [a.xpath('.//button[@type="submit"]')[0] for a in lst_hotelRow]


        one_hotelResults = {
            'hotel_name': hotel['title'],
            'hotel_star': hotel['star'],
            'provider': 'Eghamat24',
            'min_price': '',
            'rooms': []
        }

        for iter in range(len(lst_items_text)):

            # چک کردن قابل رزرو بودن
            try:
                available=lst_hotelRow[iter].xpath('.//button[@type="submit"]')[0].text
            except:
                # قابل رزرو نیست
                continue


            dic = {
                'name': lst_items_text[iter],
                'price': self.convert_to_number(lst_prices_text[iter]),
                'capacity':lst_capacities_text[iter],
                'provider': 'Eghamat24'
            }
            one_hotelResults['rooms'].append(dic)


        try:
            one_hotelResults['min_price'] = min(
                int(room['price']) for room in one_hotelResults['rooms'] if room['price'] != 'نامشخص'
            )
        except:
            print('error_')
            one_hotelResults['min_price'] = 'نامشخص'

        # print('Eghamat24     '+hotel['title'])
        self.hotelResults.append(one_hotelResults)









        #===== OLD =======
        # lst_items = htmlparsed.xpath('//div[@class="mb-3 mb-md-4"]')
        # lst_items_text = [' '.join(a.xpath('span/text()')).split('\r')[0] for a in lst_items]
        # lst_prices = htmlparsed.xpath('//div[@class="subtitle-3 fw-semibold fw-md-bold"]/text()')
        # lst_prices_text = [a.replace('\r\n', '').replace('تومان', '').strip() for a in lst_prices]


        #
        # one_hotelResults = {
        #     'hotel_name': hotel['title'],
        #     'hotel_star': hotel['star'],
        #     'provider': 'Eghamat24',
        #     'min_price': '',
        #     'rooms': []
        # }
        #
        # for iter in range(len(lst_items_text)):
        #     dic = {
        #         'name': lst_items_text[iter],
        #         'price': self.convert_to_number(lst_prices_text[iter]),
        #         'provider': 'Eghamat24'
        #     }
        #     one_hotelResults['rooms'].append(dic)
        #
        # try:
        #     one_hotelResults['min_price'] = min(
        #         int(room['price']) for room in one_hotelResults['rooms'] if room['price'] != 'نامشخص'
        #     )
        # except:
        #     print('error_')
        #     one_hotelResults['min_price'] = 'نامشخص'
        #
        # print('Eghamat24     '+hotel['title'])
        # self.hotelResults.append(one_hotelResults)

    def get_data(self):
        # with open(f'eghamat_data/lstHotels_{self.target}_withProperty.json', 'r', encoding='utf-8') as file:
        with open(f'eghamat_data/lstHotels_{self.target}_withProperty.json', 'r', encoding='utf-8') as file:
            lst_items_ok = json.load(file)

        lst_thread = []
        for hotel in lst_items_ok:
            lst_thread.append(executor.submit(self.get_one_hotel_Data, hotel))

        for th in lst_thread:
            th.result()

    def get_hotelResults(self):
        return self.hotelResults

@app.route('/fetch_hotels', methods=['GET'])
def fetch_hotels():
    target = request.args.get('target', 'MHD')
    startdate = request.args.get('startdate', '2024-10-16')
    stay = request.args.get('stay', '3')

    eghamat = Eghamat24(target, startdate, stay)
    eghamat.get_data()
    results = eghamat.get_hotelResults()
    return jsonify(results)

if __name__ == '__main__':
    # app.run(debug=True,port=8022,host='0.0.0.0')
    app.run(debug=False,port=8022,host='0.0.0.0')





#
#
# #============================== StandAlone ==================
# import requests
# import json
# from lxml import etree
# from io import StringIO
# from concurrent.futures import ThreadPoolExecutor
# class Eghamat24():
#     def __init__(self,target='MHD',startdate='2024-10-16',stay='3'):
#         self.target=target
#         self.startdate=startdate
#         self.stay=stay
#         self.executor=ThreadPoolExecutor(max_workers=5)
#         self.hotelResults = list()
#     def convert_to_number(self,persian_number):
#         # persian_number = '۲۰,۳۸۵,۰۰۰'
#
#         # Create a translation map from Persian digits to Arabic numerals
#         persian_to_arabic = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
#
#         # Replace Persian digits and remove commas
#         converted_number = persian_number.translate(persian_to_arabic).replace(',', '')
#
#         # Convert the resulting string to an integer
#         try:
#             number = int(converted_number)
#         except:
#             number='نامشخص'
#
#         return number
#
#     def get_one_hotel_Data(self,hotel):
#
#         property_id=hotel['property_id']
#         print(hotel['title'])
#
#         url = f'https://www.eghamat24.com/property-rooms/list-view?property_id={property_id}&check_in={self.startdate}&length_of_stay={self.stay}'
#         res = requests.get(url).text
#         parser=etree.HTMLParser()
#         htmlparsed=etree.parse(StringIO(res),parser=parser)
#
#         lst_items=htmlparsed.xpath('//div[@class="mb-3 mb-md-4"]')
#         lst_items_text=[' '.join(a.xpath('span/text()')).split('\r')[0] for a in lst_items]
#
#         lst_prices=htmlparsed.xpath('//div[@class="subtitle-3 fw-semibold fw-md-bold"]/text()')
#         lst_prices_text=[a.replace('\r\n','').replace('تومان','').strip() for a in lst_prices]
#
#         hotel_grid=hotel['star'] # bayad jodagane baraye lstHotels_KIH_withProperty.json bedast biyad!
#         #===
#         one_hotelResults={}
#         one_hotelResults['hotel_name']=hotel['title']
#         one_hotelResults['hotel_star']=hotel_grid
#         one_hotelResults['provider']='Eghamat24'
#         one_hotelResults['min_price']=''
#         one_hotelResults['rooms']=[]
#
#         #===
#
#         for iter in range(len(lst_items_text)):
#             dic={}
#             # dic['hotelName']=item['title']
#             dic['name']=lst_items_text[iter]
#             dic['price']=self.convert_to_number(lst_prices_text[iter])
#             dic['provider']='Eghamat24'
#             one_hotelResults['rooms'].append(dic)
#
#         try:
#             one_hotelResults['min_price'] = min(
#                 int(room['price']) for room in one_hotelResults['rooms'] if room['price'] != 'نامشخص'
#             )
#         except:
#             one_hotelResults['min_price']='نامشخص'
#
#
#         self.hotelResults.append(one_hotelResults)
#
#
#         pass
#     def get_data(self):
#
#         with open(f'lstHotels_{self.target}_withProperty.json', 'r', encoding='utf-8') as file:
#             lst_items_ok = json.load(file)
#         lst_dic = list()
#
#
#         # self.executor
#         lst_thread=list()
#         for hotel in lst_items_ok:
#             lst_thread.append(self.executor.submit(self.get_one_hotel_Data,hotel))
#
#         for th in lst_thread:
#             th.result()
#
#
#             #
#             # property_id=item['property_id']
#             # print(item['title'])
#             #
#             # url = f'https://www.eghamat24.com/property-rooms/list-view?property_id={property_id}&check_in={self.startdate}&length_of_stay={self.stay}'
#             # res = requests.get(url).text
#             # parser=etree.HTMLParser()
#             # htmlparsed=etree.parse(StringIO(res),parser=parser)
#             #
#             # # lst_items=htmlparsed.xpath('//div[contains(@class,"card-body")]')
#             #
#             # lst_items=htmlparsed.xpath('//div[@class="mb-3 mb-md-4"]')
#             # lst_items_text=[' '.join(a.xpath('span/text()')).split('\r')[0] for a in lst_items]
#             #
#             # lst_prices=htmlparsed.xpath('//div[@class="subtitle-3 fw-semibold fw-md-bold"]/text()')
#             # lst_prices_text=[a.replace('\r\n','').replace('تومان','').strip() for a in lst_prices]
#             #
#             # hotel_grid='5'  # bayad jodagane baraye lstHotels_KIH_withProperty.json bedast biyad!
#             # #===
#             # one_hotelResults={}
#             # one_hotelResults['hotel_name']=item['title']
#             # one_hotelResults['hotel_star']=hotel_grid
#             # one_hotelResults['provider']='Eghamat24'
#             # one_hotelResults['min_price']=''
#             # one_hotelResults['rooms']=[]
#             #
#             # #===
#             #
#             # for iter in range(len(lst_items_text)):
#             #     dic={}
#             #     # dic['hotelName']=item['title']
#             #     dic['name']=lst_items_text[iter]
#             #     dic['price']=self.convert_to_number(lst_prices_text[iter])
#             #     dic['provider']='Eghamat24'
#             #     one_hotelResults['rooms'].append(dic)
#             #
#             # one_hotelResults['min_price'] = min(
#             #     int(room['price']) for room in one_hotelResults['rooms'] if room['price'] != 'نامشخص'
#             # )
#             #
#             #
#             # hotelResults.append(one_hotelResults)
#             #
#         return True
#     def get_hotelResults(self):
#         return self.hotelResults
# egh=Eghamat24()
# egh.get_data()
# ress=egh.get_hotelResults()
# print('sadasdad')
#
#
#
#
#
#
#
#
# #========================================
# hotelResults = [
#     {
#         'hotel_name': 'هتل شایان کیش',
#         'hotel_star': '5',
#         'min_price': 8800000,
#         'provider': 'deltaban',
#         'rooms': [
#             {
#                 'price': 9050000,
#                 'name': 'سویئت ساحلی دو تخته',
#                 'provider': 'deltaban'
#             }
#         ]
#     }
# ]
# #========================================
#
#
#
# #
# # def get_hotel(self):
# #     hotel = Hotel(source=self.source, target=self.target, start_date=self.start_date, end_date=self.end_date,
# #                   adults=self.adults)
# #     return hotel.get_result()
# #
# #  result = self.get_kih_data()
# #
# #     # # #
# #
# #     # --- moghim24
# # moghim = Moghim24(self.target, self.start_date, self.end_date, self.adults)
# # moghim = executor.submit(moghim.get_result)
# #
# # result = []
# # def get_result_deltaban():
# #     rooms = []
# #
# #     rooms.extend([{
# #         "price": convert_to_tooman(room['packagePrice']),
# #         "name": room['roomTypes'][0]['name'],
# #         "provider": "deltaban"
# #     } for room in data['items']])
# #     if data['isFinish']:
# #         break
# #
# #
# #     result.append({
# #         "hotel_name": hotel['persianName'],
# #         "hotel_star": hotel['star'],
# #         "min_price": convert_to_tooman(hotel['minimumPackagePrice']),
# #         "rooms": rooms,
# #         "provider": "deltaban"
# #     })
#
#
#
#
# #
# # cookies = {
# #     '_gcl_au': '1.1.4506529.1728120708',
# #     'analytics_campaign': '{%22source%22:%22google%22%2C%22medium%22:%22organic%22}',
# #     'analytics_token': '4b32e595-40c4-5177-2adc-aa9a47532e57',
# #     '_yngt_iframe': '1',
# #     '_ga': 'GA1.1.884159319.1728120711',
# #     '_yngt': '827c7225-2f74-4a7f-8102-835c065feade',
# #     '_clck': '1cq7k8k%7C2%7Cfpr%7C0%7C1739',
# #     'lux_uid': '172855493554431450',
# #     'analytics_session_token': 'eeeee76e-c5fd-6a22-ac2d-4794e4c7fabc',
# #     'yektanet_session_last_activity': '10/10/2024',
# #     'last-night': '1',
# #     'last-date': '1403-7-19-5',
# #     'XSRF-TOKEN': 'eyJpdiI6ImlyWEZMNVoraStUSy85bnVZUlZrdHc9PSIsInZhbHVlIjoiQnliaEx5bENyL3ZKZjlkUGVGdXRjQlJud2U3M2k0cUs1UWI3SEtQSTFYV05MQ0V6R083d251UEphOXBWdWoyTlF0OS9rM0RNZlZIbU5xZ2NWbnpacUxsaGpVNFZHRDlwTWZJalB0dU15MmU1Uy90KzdqT1ZJT29qMVlWSjI2QmQiLCJtYWMiOiI3ZTRkNTAzNWNjNjJhMWZiOGZmN2ZmNzg0NDY2YWFiZjQzNGU2OWI4NzU0YTBlY2I5YTZmNThmZTA2NTc1N2I0IiwidGFnIjoiIn0%3D',
# #     'akamt24_session': 'eyJpdiI6ImhEb3BKc1l2NDJxcDlLdGhzclMya0E9PSIsInZhbHVlIjoic1RNbTBZNSt0eWEwd2RFMFVuWENyK3pPREN5OG9VQytCdnpWbFJBd0wvSnBhODdZWkV4cTZRMll3OVptelRtbFRhVHVZb0tCaGoxcVM5cFhkeDNpVWZOQkt0aEd0bVE0VFBLdXQ2TEFacEgzeEs2UFBpdTF2d1BQajM2RVp4UkEiLCJtYWMiOiJjNGRlY2IxNzE4ZDIyZDBkY2IwZjU4YzQ3Njk3MDQyZDI0YTU1MTAxMjUyZDkwOTEwNTBjMWM5MTdiNjI3NTA1IiwidGFnIjoiIn0%3D',
# #     '_ga_J1CW707DTW': 'GS1.1.1728554953.2.1.1728556944.46.0.280067752',
# # }
# #
# # headers = {
# #     'accept': 'application/json, text/plain, */*',
# #     'accept-language': 'en-US,en;q=0.9',
# #     # 'cookie': '_gcl_au=1.1.4506529.1728120708; analytics_campaign={%22source%22:%22google%22%2C%22medium%22:%22organic%22}; analytics_token=4b32e595-40c4-5177-2adc-aa9a47532e57; _yngt_iframe=1; _ga=GA1.1.884159319.1728120711; _yngt=827c7225-2f74-4a7f-8102-835c065feade; _clck=1cq7k8k%7C2%7Cfpr%7C0%7C1739; lux_uid=172855493554431450; analytics_session_token=eeeee76e-c5fd-6a22-ac2d-4794e4c7fabc; yektanet_session_last_activity=10/10/2024; last-night=1; last-date=1403-7-19-5; XSRF-TOKEN=eyJpdiI6ImlyWEZMNVoraStUSy85bnVZUlZrdHc9PSIsInZhbHVlIjoiQnliaEx5bENyL3ZKZjlkUGVGdXRjQlJud2U3M2k0cUs1UWI3SEtQSTFYV05MQ0V6R083d251UEphOXBWdWoyTlF0OS9rM0RNZlZIbU5xZ2NWbnpacUxsaGpVNFZHRDlwTWZJalB0dU15MmU1Uy90KzdqT1ZJT29qMVlWSjI2QmQiLCJtYWMiOiI3ZTRkNTAzNWNjNjJhMWZiOGZmN2ZmNzg0NDY2YWFiZjQzNGU2OWI4NzU0YTBlY2I5YTZmNThmZTA2NTc1N2I0IiwidGFnIjoiIn0%3D; akamt24_session=eyJpdiI6ImhEb3BKc1l2NDJxcDlLdGhzclMya0E9PSIsInZhbHVlIjoic1RNbTBZNSt0eWEwd2RFMFVuWENyK3pPREN5OG9VQytCdnpWbFJBd0wvSnBhODdZWkV4cTZRMll3OVptelRtbFRhVHVZb0tCaGoxcVM5cFhkeDNpVWZOQkt0aEd0bVE0VFBLdXQ2TEFacEgzeEs2UFBpdTF2d1BQajM2RVp4UkEiLCJtYWMiOiJjNGRlY2IxNzE4ZDIyZDBkY2IwZjU4YzQ3Njk3MDQyZDI0YTU1MTAxMjUyZDkwOTEwNTBjMWM5MTdiNjI3NTA1IiwidGFnIjoiIn0%3D; _ga_J1CW707DTW=GS1.1.1728554953.2.1.1728556944.46.0.280067752',
# #     'priority': 'u=1, i',
# #     'referer': 'https://www.eghamat24.com/KishHotels/DaryoshHotel.html',
# #     'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
# #     'sec-ch-ua-mobile': '?0',
# #     'sec-ch-ua-platform': '"Windows"',
# #     'sec-fetch-dest': 'empty',
# #     'sec-fetch-mode': 'cors',
# #     'sec-fetch-site': 'same-origin',
# #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
# #     'x-xsrf-token': 'eyJpdiI6ImlyWEZMNVoraStUSy85bnVZUlZrdHc9PSIsInZhbHVlIjoiQnliaEx5bENyL3ZKZjlkUGVGdXRjQlJud2U3M2k0cUs1UWI3SEtQSTFYV05MQ0V6R083d251UEphOXBWdWoyTlF0OS9rM0RNZlZIbU5xZ2NWbnpacUxsaGpVNFZHRDlwTWZJalB0dU15MmU1Uy90KzdqT1ZJT29qMVlWSjI2QmQiLCJtYWMiOiI3ZTRkNTAzNWNjNjJhMWZiOGZmN2ZmNzg0NDY2YWFiZjQzNGU2OWI4NzU0YTBlY2I5YTZmNThmZTA2NTc1N2I0IiwidGFnIjoiIn0=',
# # }
# #
# # params = {
# #     'property_id': '384',
# #     'check_in': '2024-10-16',
# #     'length_of_stay': '3',
# # }
# #
# # response = requests.get('https://www.eghamat24.com/property-rooms/list-view', params=params, cookies=cookies, headers=headers)