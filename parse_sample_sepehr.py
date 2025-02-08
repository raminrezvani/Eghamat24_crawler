from lxml import etree
from io import StringIO
from bs4 import BeautifulSoup

with open('sepehr_sample.html','r',encoding='utf8') as f:
    htmlText=f.read()
    parser=etree.HTMLParser()
    html_parsed=etree.parse(StringIO(htmlText),parser=parser)

    soup = BeautifulSoup(htmlText, 'html.parser')
    hotels = soup.select("table.Table03:has(tr.header)")

    for hotel in hotels:
        appended_item = {
            "hotel_name": hotel.select_one("tr.header td:nth-child(1)").text.strip(),
            "hotel_star": hotel.select_one('img[alt*="ستاره"]').get('alt').replace('ستاره','').replace('هتل','').strip(),
            "min_price": None,
            "rooms": [],
            "provider": ""
        }
        hotel_star = hotel.select_one('img[alt*="ستاره"]').get('alt').replace('ستاره','').replace('هتل','').strip()

        print(hotel_star)



