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

# Interact with the page (e.g., find an element)
element = driver.find_element(By.XPATH, '//div[contains(@class,"calendar-event-history")]')

for i in range(0,4):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.find_element(By.XPATH,'//li[@class="more"]').click()
    time.sleep(2)

lst_element_tr = element.find_elements(By.XPATH, '//table[contains(@class,"calendar-event__history")]/tbody/tr')

# for tr in lst_element_tr:
#     date=tr.find_elements(By.XPATH,'td')[0].text
#     actual = tr.find_elements(By.XPATH, 'td')[1].text
#     forecast = tr.find_elements(By.XPATH, 'td')[2].text
#     previous = tr.find_elements(By.XPATH, 'td')[3].text

# Define the CSV file name
csv_filename = "data.csv"

# Open the CSV file in write mode
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(["Date", "Actual", "Forecast", "Previous"])

    # Iterate over table rows and write to CSV
    for tr in lst_element_tr:
        date = tr.find_elements(By.XPATH, 'td')[0].text
        actual = tr.find_elements(By.XPATH, 'td')[1].text
        forecast = tr.find_elements(By.XPATH, 'td')[2].text
        previous = tr.find_elements(By.XPATH, 'td')[3].text

        writer.writerow([date, actual, forecast, previous])

print(f"Data successfully written to {csv_filename}")


print(element.text)



# Close the browser
driver.quit()
