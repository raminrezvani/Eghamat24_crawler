# from selenium import webdriver
# driver = webdriver.Chrome()
# driver.get('https://www.forexfactory.com')

#---------------------------------------- OK hast ================
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
# Create an undetected Chrome driver instance
options = uc.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode (no GUI)
options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
options.add_argument('--no-sandbox')  # Avoids sandbox errors
options.add_argument('--disable-dev-shm-usage')  # Avoids shared memory errors

# Launch the browser
driver = uc.Chrome(options=options)

# Open a website
driver.get('https://www.forexfactory.com/calendar/1-us-federal-funds-rate')

# Wait for the page to load
time.sleep(2)






#----------------- crawl news --------
def crawl_news(driver):


    def next_more(driver):
        j = 0
        while (True):
            try:
                if (j >= 10):
                    break
                first = 0
                endd = 500 * j
                driver.execute_script(f"window.scrollTo({first}, {endd});")
                driver.find_elements(By.XPATH, '//li[@class="more"]')[1].click()
                break
            except:
                j = j + 1

    lst_dic_history = {}
    for i in range(0, 4):
        element=driver.find_elements(By.XPATH,'//ul[@class="body flexposts"]/li')



        for news in element:
            try:
                news_title = news.find_element(By.XPATH, './/span[@class="flexposts__title title"]').text
                news_story = news.find_element(By.XPATH, './/div[@class="flexposts__storydisplay-info"]').text

                # news_new=news.find_element(By.XPATH, './/p[@class="flexposts__preview"]').text

                lst_dic_history[news_title]=news_story
            except:
                continue

        next_more(driver)
        time.sleep(2)

    # Define CSV filename
    csv_filename = "news_data.csv"

    # Open CSV file in write mode
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header row
        writer.writerow(["Title", "Story"])

        # Iterate over news elements and write data
        for news_title,news_story in lst_dic_history.items():
            writer.writerow([news_title, news_story])

    print(f"News data successfully written to {csv_filename}")




def crawl_hitsory(driver):

    def next_more(driver):
        j = 0
        while (True):
            try:
                if (j >= 10):
                    break
                first = 0
                endd = 500 * j
                driver.execute_script(f"window.scrollTo({first}, {endd});")
                driver.find_element(By.XPATH, '//li[@class="more"]').click()
                break
            except:
                j = j + 1

    # Interact with the page (e.g., find an element)
    element = driver.find_element(By.XPATH, '//div[contains(@class,"calendar-event-history")]')

    lst_dic_history={}
    for i in range(0,4):
        lst_element_tr = element.find_elements(By.XPATH, '//table[contains(@class,"calendar-event__history")]/tbody/tr')
        while(True):
            try:
                for tr in lst_element_tr:
                    dic={}
                    dic['date'] = tr.find_elements(By.XPATH, 'td')[0].text
                    try:
                        dic['actual'] = tr.find_elements(By.XPATH, 'td')[1].text
                    except:
                        dic['actual']='None'
                    try:
                        dic['forecast'] = tr.find_elements(By.XPATH, 'td')[2].text
                    except:
                        dic['forecast']='None'
                    try:
                        dic['previous'] = tr.find_elements(By.XPATH, 'td')[3].text
                    except:
                        dic['previous']='None'
                    lst_dic_history[dic['date']]=dic
                break
            except:
                time.sleep(2)

        print(f'length of history crawled== {len(lst_dic_history)}')
        next_more(driver)
        time.sleep(2)

    # Define the CSV file name
    csv_filename = "history_data.csv"

    # Open the CSV file in write mode
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["Date", "Actual", "Forecast", "Previous"])


        # Iterate over table rows and write to CSV
        for tr in lst_dic_history.values():
            date = tr['date']
            actual = tr['actual']
            forecast = tr['forecast']
            previous = tr['previous']

            writer.writerow([date, actual, forecast, previous])

    print(f"Data successfully written to {csv_filename}")



crawl_hitsory(driver)
crawl_news(driver)

# Close the browser
driver.quit()
