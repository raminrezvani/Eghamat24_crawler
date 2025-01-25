# new ONMe
# import requests
# res=requests.get('https://booking-dp.lastminute.de/s/hdp/search?destination=139497&datefrom=2024-10-22&dateto=2024-10-24&origin=IKA&search_mode=DP&sort=recommended&source=csw&bf_subsource=S07HPV10S07RR01&businessProfileId=HOLIDAYSBOOKINGDE_PROMO2&adults=2&search_id=j3tg1krchirjv0bsv2&vc_searchId=110102423')
#
#
#




# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"pricingSourceType":0,"adultCount":1,"childCount":0,"infantCount":0,"travelPreference":{"cabinType":"Y","maxStopsQuantity":"All","airTripType":"OneWay"},"originDestinationInformations":[{"departureDateTime":"2024-11-03","destinationLocationCode":"DXB","destinationType":"City","originLocationCode":"MHD","originType":"City"}],"isJalali":true}'
#response = requests.post('https://api.flytoday.ir/api/V1/flight/search', headers=headers, data=data)








import requests
res=requests.get('https://www.trivago.com/en-US/lm/hotels-paris-france?search=200-22235;dr-20241103-20241104')

# fp=open('res.html','w',encoding='utf8')
# fp.write(res.text)
# fp.close()
# print('asd')


from selenium import webdriver
from selenium.webdriver.common.by import By



#================== Read for each property_id ============
driver=webdriver.Chrome()

import time
# while(True):
driver.get('https://booking-dp.lastminute.de/s/hdp/search?destination=TAG_MAIORCA&datefrom=2024-10-22&dateto=2024-10-24&origin=IKA&search_mode=DP&sort=recommended&source=widget_openx_map&bf_subsource=S07HPV10S07RR01&businessProfileId=HOLIDAYSBOOKINGDE_PROMO2&adults=2&search_id=lis4ngypiifhoucrui&bfSubSource=S01RRV10S10RR01&vc_searchId=108403792')
time.sleep(2)

#====== parse results
from lxml import etree
from io import StringIO
parser=etree.HTMLParser()
htmlparser=etree.parse(StringIO(driver.page_source),parser=parser)

lst_packages=htmlparser.xpath('//div[@data-testid="card-container"]')
lst_hotelNames=htmlparser.xpath('//div[@data-testid="card-container"]/a[1]/div[2]/img/@alt')


lst_prices_hotels=[a.xpath('a[2]/div[2]/div[2]//text()') for a in lst_packages]
lst_hotels=[a.xpath('a[1]/div[2]/img/@alt') for a in lst_packages]




lst_hotelNames=htmlparser.xpath('//div[@data-testid="card-container"]/a[2]/div[2]/div[2]//text()')


