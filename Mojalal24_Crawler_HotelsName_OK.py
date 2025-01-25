from selenium import webdriver
from selenium.webdriver.common.by import By

driver=webdriver.Chrome()
import time
# while(True):
driver.get('https://www.mojalal24.ir')

driver.find_element(By.XPATH,'//*[@id="dplLoginMode"]/option[2]').click()
driver.find_element(By.XPATH,'//*[@id="txtUsername"]').clear()
driver.find_element(By.XPATH,'//*[@id="txtUsername"]').send_keys('mojalal')
driver.find_element(By.XPATH,'//*[@id="txtPassword"]').clear()
driver.find_element(By.XPATH,'//*[@id="txtPassword"]').send_keys('@MST8451030yf')
# time.sleep(2)
# #== ETELAATE BONYADI
# driver.find_element(By.XPATH,'//*[@id="Form1"]/table/tbody/tr/td/table[2]/tbody/tr[3]/td[2]/a').click()
#
# #== click on hotel
# driver.find_element(By.XPATH,'//*[@id="Header1_li2"]/a').click()
input('Go to Hotel page?')
page_source=driver.page_source
from io import StringIO
from lxml import etree
parser=etree.HTMLParser()
htmlparsed=etree.parse(StringIO(page_source),parser=parser)

HotelRooms=list()
#=== hotel items
hotel_rows=htmlparsed.xpath('//tr[@bgcolor]')

for hotelrow in hotel_rows:
    try:
        hotel={}
        hotel['hotelname']=hotelrow.xpath('td[1]')[0].text.replace('\xa0','').replace('!','').strip()

        print(hotel['hotelname'])

        # if(hotel['hotelname']=='.هتل زنده رود اصفهان'):
        #     print('asd')
        hotel['destination']=hotelrow.xpath('td[2]')[0].text.replace('\xa0','').replace('!','').strip()
        hotel['roomHref']='https://www.mojalal24.ir/Systems/FA/Inventory/'+hotelrow.xpath('td[3]/a[text()="انواع اتاق"]/@href')[0]

        hotel['starHref']='https://www.mojalal24.ir/Systems/FA/Inventory/'+hotelrow.xpath('td[3]/a[text()="ویرایش"]/@href')[0]

        hotel['rooms']=[]
        HotelRooms.append(hotel)
    except:
        print(f'Error hotelrow -->  f{hotel["hotelname"]}')


for hotel in HotelRooms:
    try:

        roomHref=hotel['roomHref']

        # if (roomHref=="https://mojalal24.ir/Systems/FA/Inventory/HotelsEdit.aspx?HID=1644&Hotel_Name=.%D9%87%D8%AA%D9%84%20%D8%B2%D9%86%D8%AF%D9%87%20%D8%B1%D9%88%D8%AF%20%D8%A7%D8%B5%D9%81%D9%87%D8%A7%D9%86"):
        #     print('sada')

        driver.get(roomHref)
        page_source=driver.page_source
        htmlparsed = etree.parse(StringIO(page_source), parser=parser)

        lst_rooms = htmlparsed.xpath('//tr[@bgcolor]/td[1]/text()')
        lst_rooms=[a.replace('\n','').strip() for a in lst_rooms]
        hotel['rooms']=lst_rooms
    except:
        print(f'Error room -->  f{roomHref}')


#== get hotel stars
for hotel in HotelRooms:
    try:
        starHref=hotel['starHref']
        driver.get(starHref)
        page_source=driver.page_source
        htmlparsed = etree.parse(StringIO(page_source), parser=parser)
        star=htmlparsed.xpath('//select[@id="dplHotelClass"]/option[@selected="selected"]')[0].get('value')
        hotel['star']=star
    except:
        print(f'error {hotel["hotelname"]}')

import json
json_data=json.dumps(HotelRooms)
with open('HotelRooms_Mojalal24_withStars20.json','w',encoding='utf-8') as fp:
    fp.write(json_data)


# #
# import json
# with open('HotelRooms_Mojalal24_withStars1.json', 'r', encoding='utf-8') as json_file:
#     HotelRooms = json.load(json_file)
#


