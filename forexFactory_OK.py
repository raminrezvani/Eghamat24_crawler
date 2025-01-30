# from selenium import webdriver
# driver = webdriver.Chrome()
# driver.get('https://www.forexfactory.com')

#---------------------------------------- OK hast ================
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Create an undetected Chrome driver instance
options = uc.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode (no GUI)
options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
options.add_argument('--no-sandbox')  # Avoids sandbox errors
options.add_argument('--disable-dev-shm-usage')  # Avoids shared memory errors

# Launch the browser
driver = uc.Chrome(options=options)

# Open a website
driver.get('https://www.example.com')

# Wait for the page to load
time.sleep(2)

# Interact with the page (e.g., find an element)
element = driver.find_element(By.XPATH, '//*[@id="element_id"]')
print(element.text)

# Close the browser
driver.quit()
