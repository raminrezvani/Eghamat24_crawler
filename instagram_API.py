# URL ALIIIIIIIIIIII (ba graphql)
#https://stackoverflow.com/questions/49265339/instagram-a-1-url-not-working-anymore-problems-with-graphql-query-to-get-da
#https://stackoverflow.com/questions/49265339/instagram-a-1-url-not-working-anymore-problems-with-graphql-query-to-get-da
#https://stackoverflow.com/questions/49265339/instagram-a-1-url-not-working-anymore-problems-with-graphql-query-to-get-da
#https://stackoverflow.com/questions/49265339/instagram-a-1-url-not-working-anymore-problems-with-graphql-query-to-get-da
#https://stackoverflow.com/questions/49265339/instagram-a-1-url-not-working-anymore-problems-with-graphql-query-to-get-da
#https://stackoverflow.com/questions/49265339/instagram-a-1-url-not-working-anymore-problems-with-graphql-query-to-get-da
#https://stackoverflow.com/questions/48495648/how-do-i-get-the-next-page-of-data-from-a-instagram-tag-look-up
#**************************************************************************************
#**************************************************************************************
#**************************************************************************************
#**************************************************************************************
import sys

import pymongo
import datetime
import base64
from persiantools.jdatetime import JalaliDate
myclient2 = pymongo.MongoClient('mongodb://45.149.76.168:13667')
mydb2 = myclient2["Jalali_Project"]
# mycol_write = mydb2["Instagram_Hashtags_1403"]
# mycol_write_posts = mydb2["Posts_Hashtags_1403"]
mycol_write_posts = mydb2["Posts_Hashtags_poleTabiat"]






#https://storiknow.com/get-instagram-posts-by-tag-name/
#https://stackoverflow.com/questions/43655098/how-to-get-all-instagram-posts-by-hashtag-with-the-api-not-only-the-posts-of-my
#https://api.data365.co/v1.1/instagram/docs#section/Authentication/accessTokenAuthorization
#https://magento.stackexchange.com/questions/311011/get-all-post-from-instagram-based-on-some-hash-tags

# https://storiknow.com/get-instagram-posts-by-tag-name/
# https://storiknow.com/get-instagram-posts-by-tag-name/
# https://storiknow.com/get-instagram-posts-by-tag-name/
# https://storiknow.com/get-instagram-posts-by-tag-name/


import requests
from bson.json_util import dumps
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
class driver_status:

    status=0
    driver=[]
    def __init__(self):
        self.driver=[]
        options = Options()
        #options.add_argument('--headless')
        #options.add_argument('--no-sandbox')
        #options.add_argument("--log-level=3")


        chrome_prefs = {}

        #options.experimental_options["prefs"] = chrome_prefs

        #chrome_prefs["profile.default_content_settings"] = {"images": 2}

        #chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}



        # PROXY = get_proxy(mycol_write)
        # PROXY = '190.96.103.169:999'
        # print(PROXY)
        # options.add_argument('--proxy-server=http://%s' % PROXY)

        import undetected_chromedriver as uc
        driver = uc.Chrome()
        # driver.get('https://my.alpariforex.org/fa/platforms/webterminal_mt4/')

        # driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)


        # driver = webdriver.Chrome('chromedriver.exe', chrome_options=options,service_log_path='NUL')

        # driver.set_page_load_timeout(30)

        self.status = 0
        self.driver=driver
        self.driver.delete_all_cookies()
    # def get_url(url):

    def restart(self):
        # self.driver.delete_all_cookies()
        self.driver.quit()
        self.driver=[]
        options = Options()
        #options.add_argument('--headless')
        #options.add_argument("--log-level=3")
        #options.add_argument('--no-sandbox')

        # PROXY = get_proxy(mycol_write)
        # PROXY = '190.96.103.169:999'
        # print(PROXY)
        # options.add_argument('--proxy-server=http://%s' % PROXY)


        # driver = webdriver.Chrome('chromedriver.exe', chrome_options=options,service_log_path='NUL')
        driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
        # driver.set_page_load_timeout(30)
        self.status=0
        self.driver=driver

    def login_instagram(self):
        while(True):
            try:
                self.driver.get('https://www.instagram.com/?hl=en')
                time.sleep(5)
                self.driver.find_element_by_xpath('//input[@name="username"]').send_keys('urbanspace1401')
                self.driver.find_element_by_xpath('//input[@name="password"]').send_keys('urban135792468')
                self.driver.find_element_by_xpath('//button[@type="submit"]').click()

                break
            except:

                continue

# dr = driver_status()
# dr.login_instagram()

import undetected_chromedriver as uc
driver = uc.Chrome()
driver.get('https://www.instagram.com/?hl=en')
#
# # driver = webdriver.Chrome()
# while (True):
#     try:
#         driver.get('https://www.instagram.com/?hl=en')
#         time.sleep(5)
#         # driver.find_element_by_xpath('//input[@name="username"]').send_keys('raminrezvani_insta3@yahoo.com')
#         # driver.find_element_by_xpath('//input[@name="password"]').send_keys('6jIfYo63raminrezvani')
#
#         # driver.find_element_by_xpath('//input[@name="username"]').send_keys('webjar20')
#         # driver.find_element_by_xpath('//input[@name="password"]').send_keys('webjar2020')
#
#         # driver.find_element_by_xpath('//input[@name="username"]').send_keys('Web.jar')
#         # driver.find_element_by_xpath('//input[@name="password"]').send_keys('10203040')
#
#         # driver.find_element_by_xpath('//input[@name="username"]').send_keys('Web_jar')
#         # driver.find_element_by_xpath('//input[@name="password"]').send_keys('50607080')
#
#         # driver.find_element_by_xpath('//input[@name="username"]').send_keys('sky11875')
#         # driver.find_element_by_xpath('//input[@name="password"]').send_keys('webjar123')
#
#         # reactivate amad ===> refresh konid faghat (ya dobare roye URL enter konid!)
#
#
#
#         driver.find_element_by_xpath('//button[@type="submit"]').click()
#         break
#     except:
#         continue

responsee=input('is SignedIn???')

#===========================
def insert_intoDatabase(post_url,
                        post_image_url,
                        post_caption,
                        post_datetime,
                        post_owner_id,
                        post_is_video,
                        post_count_preview,
                        post_count_comment,
                        post_count_likes,
                        hashtag ,all_existing_posts):


    img_content = ''
    try:
        # img_content = base64.b64encode(requests.get(post_image_url).content)


        mycol_write_posts.update({'post_url': post_url},
                                 {'$setOnInsert': {'post_caption': post_caption,
                                                   'post_date': str(JalaliDate.fromtimestamp(post_datetime)),
                                                   'post_url': post_url,
                                                   'post_owner_id': post_owner_id,
                                                   'post_is_video': post_is_video,
                                                   'post_count_preview': post_count_preview,
                                                   'post_count_comment': post_count_comment,
                                                   'post_count_likes': post_count_likes,

                                                   'post_image_url': post_image_url,
                                                   'post_image_content': img_content,
                                                   'post_location': '',
                                                   'post_hashtags': '',
                                                   'initial_hashtag': hashtag
                                                   }}, True)
        print(post_url + '_____' + 'Is Fetched!!!!')
        all_existing_posts.append(post_url)
    except:
        print('no- Image' + '====== ' + post_url)
        ''


import threading
def parse_json_res(json_res,all_existing_posts,hashtag):
    stop=0
    # each section (row) === 3 media
    aa=json_res['data']['hashtag']['edge_hashtag_to_media']['edges']
    lst_thread=list()
    for row in aa:
        row=row['node']
        post_url='https://www.instagram.com/p/'+row['shortcode']+'/'

        if (post_url not in all_existing_posts):

            try:
                post_caption=row['edge_media_to_caption']['edges'][0]['node']['text']
                post_datetime=row['taken_at_timestamp']
                post_image_url=row['display_url']
                post_count_likes=row['edge_liked_by']['count']
                post_count_preview=row['edge_media_preview_like']['count']
                post_count_comment=row['edge_media_to_comment']['count']
                post_owner_id=row['owner']['id']
                post_is_video=row['is_video']

                # insert into database
                # import threading
                post_datetime_jalali=str(JalaliDate.fromtimestamp(post_datetime))
                if (JalaliDate.fromisoformat(post_datetime_jalali)<JalaliDate.fromisoformat('1401-05-01')):
                    print('post_datetime_jalali=== '+post_datetime_jalali)
                    stop=1
                    # break


                thh=threading.Thread(target=insert_intoDatabase, args=(post_url,
                                    post_image_url,
                                    post_caption,
                                    post_datetime,
                                    post_owner_id,
                                    post_is_video,
                                    post_count_preview,
                                    post_count_comment,
                                    post_count_likes,
                                    hashtag,all_existing_posts), daemon=True)
                lst_thread.append(thh)
                #
                # insert_intoDatabase(post_url,
                #                     post_image_url,
                #                     post_caption,
                #                     post_datetime,
                #                     post_owner_id,
                #                     post_is_video,
                #                     post_count_preview,
                #                     post_count_comment,
                #                     post_count_likes,
                #                     hashtag,all_existing_posts)


            except Exception as e:
                print(post_url +'___error____')
                continue
    for th in lst_thread:
        th.start()
    for th in lst_thread:
        th.join()

        # print(post_url)
    print('Total_Ids=== '+str(len(all_existing_posts)))
    end_cursor=json_res['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
    has_next_page=json_res['data']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
    all_post_in_hashtag=json_res['data']['hashtag']['edge_hashtag_to_media']['count']

    #
    #     all_three_media=row['node']['medias']
    #     for media in all_three_media:
    #         post_code=media['media']['code']
    #         post_url='https://www.instagram.com/p/'+post_code
    #         if (post_url not in list_id):
    #             print('new_ID_dound')
    #             list_id.append(post_url)
    #         print(post_url)
    # next_max_id=json_res['data']['recent']['next_max_id']

    return end_cursor,stop
print('finish')

#=============================
s=requests.session()
# url='https://www.instagram.com/explore/tags/selfie/?__a=1&max_id=2704522950881857598_7498816728'

next_max_id=''

# get all_existing_posts

# hashtag='پل_طبیعت'
# hashtag='تئاتر_شهر'

# hashtag='پل_طبیعت_تهران'
# hashtag='تئاترشهر'
# hashtag='خیابان_سی_تیر'
# hashtag='پارک_آب_و_آتش'
# hashtag='آب_و_آتش'
# hashtag='دریاچه_چیتگر'


# hashtag='چیتگر'
# hashtag='برج_میلاد'
# hashtag='برج_میلاد_تهران'
#hashtag='پل_طبیعت'
# hashtag='پل_طبیعت_تهران'
# hashtag='باغ_کتاب_تهران'
# hashtag='تئاتر_شهر'
# hashtag='سی_تیر'
# hashtag='خیابان_سی_تیر'
# hashtag='خیابان_انقلاب'
# hashtag='خیابان_ولیعصر'
# hashtag='رستوران'


lst_all_hashtags=list()
lst_all_hashtags.append('پل_طبیعت')  # baraye 1401-05-01 ok shod
# lst_all_hashtags.append('تئاتر_شهر')  # baraye 1401-05-01 ok shod
lst_all_hashtags.append('پل_طبیعت_تهران')  #??????
# lst_all_hashtags.append('تئاترشهر')  # ????
# lst_all_hashtags.append('خیابان_سی_تیر') # baraye 1401-05-01 ok shod
# lst_all_hashtags.append('پارک_آب_و_آتش')  #  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('آب_و_آتش')
# lst_all_hashtags.append('دریاچه_چیتگر')
# lst_all_hashtags.append('چیتگر')
# lst_all_hashtags.append('برج_میلاد')
# lst_all_hashtags.append('برج_میلاد_تهران')
# lst_all_hashtags.append('پل_طبیعت_تهران')
# lst_all_hashtags.append('باغ_کتاب_تهران')
# lst_all_hashtags.append('سی_تیر')
# lst_all_hashtags.append('خیابان_انقلاب')
# lst_all_hashtags.append('خیابان_ولیعصر')
# lst_all_hashtags.append('رستوران')



# lst_all_hashtags.append('چیتگر')    #  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('دریاچه_چیتگر') #  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('پل_طبیعت')#  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('پل_طبیعت_تهران')#  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('تئاتر_شهر')#  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('سی_تیر')) #  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('خیابان_سی_تیر') #  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('خیابان_انقلاب') #  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('بولوار_کشاورز')  # NADARAD! POST NADARAD!
# lst_all_hashtags.append('میدان_مشق')  #  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('باغ_ملی') #  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('میدان_آزادی')   # baraye 1401-05-01 ok shod
# lst_all_hashtags.append('میدان_ولیعصر')#  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('بازار_بزرگ_تهران')#  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('بازار_تجریش')#  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('ایران_مال')#  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('باملند')#  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('باملند_تهران') ##  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('پالادیوم')#  baraye 1401-05-01 ok shod
#lst_all_hashtags.append('دربند')#  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('توچال_تهران') #  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('باغ_فردوس')#  baraye 1401-05-01 ok shod
# lst_all_hashtags.append('پارک_آب_و_آتش')#  baraye 1401-05-01 ok shod


#=== New Hashtag 1403 ===
# lst_all_hashtags.append('بازار_بزرگ')
# lst_all_hashtags.append('بازار_بزرگ_تهران')
# lst_all_hashtags.append('سی_تیر')
# lst_all_hashtags.append('بولوار_کشاورز')
# lst_all_hashtags.append('پارک_آب_و_آتش')
# lst_all_hashtags.append('آب_و_آتش')





#  ========== Address  ==================
#https://carloshenriquereis-17318.medium.com/how-to-get-data-from-a-public-instagram-profile-edc6704c9b45
#https://carloshenriquereis-17318.medium.com/how-to-get-data-from-a-public-instagram-profile-edc6704c9b45
#https://carloshenriquereis-17318.medium.com/how-to-get-data-from-a-public-instagram-profile-edc6704c9b45




tedad_pages_crawled=50
for hashtag_get in lst_all_hashtags:
    temp_list = mycol_write_posts.find({'initial_hashtag': hashtag_get}, {'post_url': 1})
    all_existing_posts = json.loads(dumps(temp_list))

    tedad = 0
    end_cursor='XXXXXXXX'
    while(True):
        try:

            # url='https://www.instagram.com/explore/tags/پل_طبیعت/?__a=1'
            # if (next_max_id!=''):
            #     url=url+'&max_id='+next_max_id


            url='https://www.instagram.com/graphql/query/?query_hash=298b92c8d7cad703f7565aa892ede943&' \
                'variables={"tag_name":"'+hashtag_get+'","first":1000,"after":"XXXXXXXX"}'

            'https://www.instagram.com/graphql/query/?query_hash=298b92c8d7cad703f7565aa892ede943&variables={"tag_name":"پل","first":1000,"after":"XXXXXXXX"}'
            url=url.replace('XXXXXXXX',end_cursor)
            driver.get(url)
            time.sleep(2)
            # aa=driver.find_element_by_xpath('html/body').text
            aa=driver.find_element(By.XPATH,'html/body').text
            json_res=json.loads(aa)

            end_cursor,stop=parse_json_res(json_res,all_existing_posts,hashtag_get)
            # if (stop==1):   # when data<1401-05-01
            #     break
            tedad=tedad+1
            print(str(tedad))

            if (tedad>tedad_pages_crawled):
                print(hashtag_get+' ___- '+str(tedad)+'___ is cralwed!!!')

                newHashtag = input('Insert New Hashtag ...')
                print('New hashtag is crawling.....')
                hashtag_get=newHashtag
                temp_list = mycol_write_posts.find({'initial_hashtag': hashtag_get}, {'post_url': 1})
                all_existing_posts = json.loads(dumps(temp_list))

                tedad = 0
                end_cursor = 'XXXXXXXX'


                # break
            time.sleep(5)
        except Exception as e:
            print('!!!!!!---- Erroe' + 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + '\n')
            print(str(e))
            newHashtag=input('error occured! _ solve it?? (current hashtag (enter) / newHashtag( insert NewHashtag)')
            if (newHashtag=='no'):
                break


            if (len(newHashtag)>2):
                print('New hashtag is crawling.....')
                hashtag_get=newHashtag
                temp_list = mycol_write_posts.find({'initial_hashtag': hashtag_get}, {'post_url': 1})
                all_existing_posts = json.loads(dumps(temp_list))

                tedad = 0
                end_cursor = 'XXXXXXXX'

            time.sleep(2)
            continue

        # data=res.split('{"data":')[1]
        # data=data.split('</pre>')[0]
    # json_res=json.loads(data)


print('finish')