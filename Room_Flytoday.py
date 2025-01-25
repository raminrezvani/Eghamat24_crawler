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
    'x-path': 'https://www.flytoday.ir/hotel/search/hotelavailability?hotelId=367271&regionCode=178267&checkIn=2024-11-06&checkOut=2024-11-10&adt[0]=1&chd[0]=0&chdAges[0]=&dateLang=fa&countryCode=TR',
    'x-token': '71446672666d62566145347978696477434a556461416762615935774c4267474d5066505533312f595a3733777a636534487846514536724573527830666743',
    'x-token': '71446672666d62566145347978696477434a556461416762615935774c4267474d5066505533312f595a3733777a636534487846514536724573527830666743',
}

json_data = {
    'hotelSearchId': 58321122,
    # 'hotelSearchId': 58322669,
    'language': 'Fa',
}

response = requests.post('https://api.flytoday.ir/api/v1/Hotel/RoomInfo', headers=headers, json=json_data)

print(response)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"hotelSearchId":58321122,"language":"Fa"}'
#response = requests.post('https://api.flytoday.ir/api/v1/Hotel/RoomInfo', headers=headers, data=data)