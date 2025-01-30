from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import datetime
import threading
import time

# تنظیمات کروم برای Performance Logging
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--remote-debugging-port=9222")  # فعال کردن دیباگینگ
chrome_options.add_experimental_option("detach", True)  # باز نگه داشتن مرورگر

# فعال‌سازی لاگ‌های Performance
capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

# ایجاد مرورگر با تنظیمات Performance Logging
driver = webdriver.Chrome(service=Service(), options=chrome_options, desired_capabilities=capabilities)

# دیکشنری برای مدیریت تب‌ها و Threadها
tabs_threads = {}

# تابع لاگ‌گیری درخواست‌های شبکه‌ای برای هر تب
def log_network_requests(tab_id):
    try:
        print(f"Monitoring started for Tab ID: {tab_id}")
        while True:
            logs = driver.get_log("performance")
            for entry in logs:
                log = json.loads(entry["message"])["message"]
                if log["method"] == "Network.requestWillBeSent":
                    request = log["params"]["request"]
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] Tab ID: {tab_id} | URL: {request['url']} | Method: {request['method']}")
            time.sleep(1)
    except Exception as e:
        print(f"Error in Tab {tab_id}: {e}")

try:
    # باز کردن تب اولیه
    driver.get("https://example.com")
    print("مرورگر باز است و در حال مانیتورینگ تمام تب‌ها...")

    while True:
        # دریافت تمام تب‌های باز
        all_tabs = driver.window_handles

        # ایجاد Thread برای تب‌های جدید
        for tab_id in all_tabs:
            if tab_id not in tabs_threads:
                print(f"Starting logging thread for Tab ID: {tab_id}")
                thread = threading.Thread(target=log_network_requests, args=(tab_id,))
                thread.daemon = True
                thread.start()
                tabs_threads[tab_id] = thread

        time.sleep(2)

except KeyboardInterrupt:
    print("برنامه با درخواست شما متوقف شد.")

finally:
    print("مرورگر باز خواهد ماند.")
