# import requests
# import json
#
# url = "http://127.0.0.1/booking_hotels"
# params = {
#     "start_date": "2025-02-1",
#     "end_date": "2025-02-15",
#     "adults": "2",
#     "target": "Paris",
#     "isAnalysis": "true",
#     "hotelstarAnalysis": json.dumps([5, 4])  # Converting list to JSON string
# }
#
# response = requests.get(url, params=params)
# print(response.json())  # Assuming the response is in JSON format

import requests
from datetime import datetime,timedelta

def get_all_hotels():
    cookies = {
        'analytics_token': '2465e1bc-33f5-7784-f08e-5eccdb9e84e3',
        '_yngt': 'aeb2eaa1-a6d0-499c-8163-3177517509f8',
        '_ga': 'GA1.2.613783467.1735571929',
        '_ga_N9ZBHQ0R9X': 'GS1.1.1737471427.4.0.1737471427.60.0.0',
        '_gid': 'GA1.2.1474142608.1739037498',
        'analytics_session_token': '19821ea4-a664-96b3-0688-6c856d79d96c',
        'yektanet_session_last_activity': '2/9/2025',
        '_yngt_iframe': '1',
        '_dc_gtm_UA-174237991-1': '1',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        # 'cookie': 'analytics_token=2465e1bc-33f5-7784-f08e-5eccdb9e84e3; _yngt=aeb2eaa1-a6d0-499c-8163-3177517509f8; _ga=GA1.2.613783467.1735571929; _ga_N9ZBHQ0R9X=GS1.1.1737471427.4.0.1737471427.60.0.0; _gid=GA1.2.1474142608.1739037498; analytics_session_token=19821ea4-a664-96b3-0688-6c856d79d96c; yektanet_session_last_activity=2/9/2025; _yngt_iframe=1; _dc_gtm_UA-174237991-1=1',
        'origin': 'https://www.booking.ir',
        'priority': 'u=1, i',
        'referer': 'https://www.booking.ir/fa/hotel/iran/kish/?i=2025-02-12&o=2025-02-15&r=1&n=&d=1640809&a=2&c=0',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    json_data = {
        'isStaticPage': False,
        'checkIn': '2025-02-12T00:00:00',
        'checkOut': '2025-02-15T00:00:00',
        'systemType': None,
        'room': 1,
        'nationality': 'IR',
        'sessionId': '21264d8317b949c4b91959a8095c4055',
        'highLightedHotels': [],
        'destinations': {
            'id': '1640809',
        },
        'occupancies': [
            {
                'adult': 2,
                'childs': 0,
                'ages': [],
            },
        ],
    }



    t1=datetime.now()
    response = requests.post('https://www.booking.ir/v3/hotelbooking/search/', cookies=cookies, headers=headers, json=json_data)

    t2=datetime.now()
    spend=(t2-t1).total_seconds()
    print(f'Spend time == {spend}')

def get_rooms_oneHotel():
    import requests

    cookies = {
        'analytics_token': '2465e1bc-33f5-7784-f08e-5eccdb9e84e3',
        '_yngt': 'aeb2eaa1-a6d0-499c-8163-3177517509f8',
        '_ga': 'GA1.2.613783467.1735571929',
        '_ga_N9ZBHQ0R9X': 'GS1.1.1737471427.4.0.1737471427.60.0.0',
        '_gid': 'GA1.2.1474142608.1739037498',
        'analytics_session_token': '19821ea4-a664-96b3-0688-6c856d79d96c',
        'yektanet_session_last_activity': '2/9/2025',
        '_yngt_iframe': '1',
        '_dc_gtm_UA-174237991-1': '1',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        # 'cookie': 'analytics_token=2465e1bc-33f5-7784-f08e-5eccdb9e84e3; _yngt=aeb2eaa1-a6d0-499c-8163-3177517509f8; _ga=GA1.2.613783467.1735571929; _ga_N9ZBHQ0R9X=GS1.1.1737471427.4.0.1737471427.60.0.0; _gid=GA1.2.1474142608.1739037498; analytics_session_token=19821ea4-a664-96b3-0688-6c856d79d96c; yektanet_session_last_activity=2/9/2025; _yngt_iframe=1; _dc_gtm_UA-174237991-1=1',
        'origin': 'https://www.booking.ir',
        'priority': 'u=1, i',
        'referer': 'https://www.booking.ir/fa/hotel/iran/kish/kish-abadgaran/?i=2025-02-12&o=2025-02-15&r=1&n=&d=1644043&a=2&c=0',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    json_data = {
        'isStaticPage': False,
        'checkIn': '2025-02-12T00:00:00',
        'checkOut': '2025-02-15T00:00:00',
        'systemType': None,
        'room': 1,
        'nationality': 'IR',
        'sessionId': '17d51830a9dc448bb3e3143273380e1e',
        'highLightedHotels': [],
        'destinations': {
            'id': '1644043',
        },
        'occupancies': [
            {
                'adult': 2,
                'childs': 0,
                'ages': [],
            },
        ],
    }
    t1=datetime.now()

    response = requests.post('https://www.booking.ir/v3/hotelbooking/search/', cookies=cookies, headers=headers,
                             json=json_data)
    t2=datetime.now()
    spend=(t2-t1).total_seconds()
    print(f'Spend time == {spend}')


#-----------
import json
with open('Booking_hotel_info.json', 'r') as f:
    a = f.read()
    hotels = json.loads(a)


#_---------
get_rooms_oneHotel()
get_all_hotels()



