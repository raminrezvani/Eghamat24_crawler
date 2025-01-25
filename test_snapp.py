import requests
import requests
url = 'http://45.149.76.168:5004/SnappTrip_Hotelrooms'
params = {
    'date_from': '2024-11-05',
    'date_to': '2024-11-08',
    'city_id': '6326',
}

# city_id='6326'
# date_from='2024-11-08'
# date_to='2024-11-11'
# lst_hotels=[]


response = requests.get(url, params=params)
print('asd')

import json
json.loads(response.text)
