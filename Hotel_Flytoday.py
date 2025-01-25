
# ============== crawl flytoday ===============
#---- hotel
import requests

headers = {
    'accept': '*/*',
    'accept-language': 'fa-IR',
    'authorization': 'Bearer null',
    'cache-control': 'max-age=0',
    'content-type': 'application/json',
    'origin': 'https://www.flytoday.ir',
    'priority': 'u=1, i',
    'referer': 'https://www.flytoday.ir/',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'x-app': 'www.flytoday.ir',
    'x-path': 'https://www.flytoday.ir/hotel/search?&regionCode=178267&checkIn=2024-10-23&checkOut=2024-10-27&adt[0]=1&chd[0]=0&chdAges[0]=&dateLang=fa&countryCode=TR',
    # 'x-token': '36366e744c6e7577642b43706e794876357a714141494b39544f3843634f73513677697a2b654a676269714d71506c78475679354c6d61577752697172527636',
}

json_data = {
    'checkIn': '2024-10-27',
    'checkOut': '2024-10-30',
    'hotelId': None,
    'occupancies': [
        {
            'adultCount': 1,
            'childCount': 0,
            'childAges': [],
        },
    ],
    'dateLang': 'fa',
    'NationalityId': 'IR',
    # 'countryCode': 'TR',
    'countryCode': 'AE',
    'cityName': '',
    'hotelName': '',
    'key': '',
    'isJalali': True,
    'isDomestic': False,
    'regionCode': '1079',   # bayad hatman dorost shavad!!!
}

response = requests.post('https://api.flytoday.ir/api/V1/hotel/Availability', headers=headers, json=json_data)

import json
json_data=json.loads(response.text)

lst_hotels=list()
hotel_items=json_data['pricedItineraries']
for item in hotel_items:
    hotel = {}
    hotel['hotel_name']=item['hotelInfo']['name']
    hotel['hotel_star']=''
    hotel['min_price']=item['totalPrice']
    hotel['provider']='FlyToday'
    hotel['rooms']=[]
    for room in item['rooms']:
        roomItem={}
        roomItem['name']=room['name']
        roomItem['price']=hotel['min_price']
        roomItem['provider']='FlyToday'
        hotel['rooms'].append(roomItem)
    lst_hotels.append(hotel)
print('asd')


print('asdasd')
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"checkIn":"2024-10-23","checkOut":"2024-10-27","hotelId":null,"occupancies":[{"adultCount":1,"childCount":0,"childAges":[]}],"dateLang":"fa","NationalityId":"IR","countryCode":"TR","cityName":"","hotelName":"","key":"","isJalali":true,"isDomestic":false,"regionCode":"178267"}'
#response = requests.post('https://api.flytoday.ir/api/V1/hotel/Availability', headers=headers, data=data)


