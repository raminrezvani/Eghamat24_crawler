#------------
import os
import threading
import queue
import time
import json
import itertools
import requests
import redis
from flask import Flask, jsonify, request
from concurrent.futures import ThreadPoolExecutor, Future

# تنظیم عنوان ترمینال
os.system("title Distribute Requests")

app = Flask(__name__)

# اتصال به Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# کلیدها برای ذخیره‌سازی در Redis
REDIS_KEY = "global_requests_list"
REDIS_DELAY_KEY = "priority_delays"
redis_client.delete(REDIS_KEY)
redis_client.delete(REDIS_DELAY_KEY)


# تنظیمات نخ‌ها
NUM_THREADS_PER_QUEUE = 1000
MAX_PRIORITY = 10

# تعریف صف‌های اولویت
priority_queues = {i: queue.Queue() for i in range(1, MAX_PRIORITY + 1)}
general_queue = queue.Queue()

# تخصیص تعداد نخ‌های مختلف برای هر صف
executors = {
    1: ThreadPoolExecutor(max_workers=10000),
    2: ThreadPoolExecutor(max_workers=1),
}
executors.update({i: ThreadPoolExecutor(max_workers=1) for i in range(3, MAX_PRIORITY + 1)})
general_executor = ThreadPoolExecutor(max_workers=1)  # صف عمومی

# مقداردهی اولیه تأخیرها در Redis
redis_client.delete(REDIS_DELAY_KEY)
redis_client.set(REDIS_DELAY_KEY, json.dumps({str(i): 0 for i in range(1, MAX_PRIORITY + 1)}))

# شرط برای هماهنگ‌سازی پردازش‌ها
condition = threading.Condition()


class ExeRequest:
    def __init__(self, method, url, params=None, cookies=None, headers=None, data=None, json=None):
        self.url = url
        self.params = params
        self.cookies = cookies
        self.headers = headers
        self.method = method.lower()
        self.data = data
        self.json = json
        self.future = Future()

    def execute(self):
        """اجرای درخواست HTTP"""
        if self.method == "get":
            response = requests.get(self.url, params=self.params, cookies=self.cookies, headers=self.headers,
                                    data=self.data, json=self.json)
        elif self.method == "post":
            response = requests.post(self.url, params=self.params, cookies=self.cookies, headers=self.headers,
                                     data=self.data, json=self.json)
        else:
            response = None

        if response:
            self.future.set_result(response)


def get_priority(timestamp):
    with condition:
        data = redis_client.get(REDIS_KEY)
        global_requests_list = json.loads(data) if data else []

        global_requests_list = sorted(set(global_requests_list + [timestamp]))

        redis_client.set(REDIS_KEY, json.dumps(global_requests_list))

        priority_mapping = {t: min(i + 1, MAX_PRIORITY) for i, t in enumerate(global_requests_list)}

        return priority_mapping[timestamp]


def update_priority_delays(priority, delay):
    """به‌روزرسانی مقدار تأخیر هر صف در Redis"""
    data = redis_client.get(REDIS_DELAY_KEY)
    delays = json.loads(data) if data else {}
    delays[str(priority)] = delay
    redis_client.set(REDIS_DELAY_KEY, json.dumps(delays))


MAX_PRIORITY = 5  # تعداد سطوح اولویت
priority_queues = {p: queue.Queue() for p in range(1, MAX_PRIORITY + 1)}
executors = {p: ThreadPoolExecutor(max_workers=2) for p in range(1, MAX_PRIORITY + 1)}




#
# def process_queues():
#     """پردازش درخواست‌ها از بالاترین اولویت به پایین‌ترین، با توقف کامل برای هر صف پس از خالی شدن"""
#
#     empty_counts = {p: 0 for p in range(1, MAX_PRIORITY + 1)}  # شمارنده خالی بودن هر صف
#     queue_was_non_empty = {p: False for p in range(1, MAX_PRIORITY + 1)}  # بررسی داشتن درخواست
#
#     current_priority = 1  # شروع پردازش از صف ۱
#
#     while current_priority <= MAX_PRIORITY:
#         # ثبت اینکه صف موردنظر حداقل یک‌بار درخواست داشته است
#         if not queue_was_non_empty[current_priority] and not priority_queues[current_priority].empty():
#             queue_was_non_empty[current_priority] = True
#
#         # اگر این صف قبلاً درخواست داشته و حالا خالی شده است
#         if queue_was_non_empty[current_priority] and priority_queues[current_priority].empty():
#             if empty_counts[current_priority] < 2:
#                 print(f"🔴 صف {current_priority} خالی شد! توقف برای ۱۰ ثانیه...")
#                 time.sleep(10)  # توقف ۱۰ ثانیه‌ای
#                 empty_counts[current_priority] += 1
#                 continue  # بازگشت به ابتدای حلقه برای توقف دوم
#             else:
#                 print(f"✅ دو بار توقف برای صف {current_priority} انجام شد. رفتن به صف بعدی...")
#                 current_priority += 1  # رفتن به صف بعدی
#                 continue
#
#         else:
#             empty_counts[current_priority] = 0  # اگر صف مجدداً درخواست دریافت کرد، شمارنده ریست شود
#
#         # پردازش درخواست‌های صف جاری
#         try:
#             request_obj = priority_queues[current_priority].get(block=False)
#             executors[current_priority].submit(request_obj.execute)
#         except queue.Empty:
#             pass  # اگر صف خالی بود، ادامه حلقه را انجام بده
#
#         time.sleep(1)  # جلوگیری از اجرای بی‌نهایت سریع حلقه
#
#     print("🎯 همه صف‌ها پردازش شدند و هیچ درخواست دیگری باقی نمانده است!")


def process_queues():
    """پردازش درخواست‌ها از بالاترین اولویت به پایین‌ترین با کنترل تأخیر برای صف ۱"""

    empty_1_count = 0  # شمارش تعداد دفعات خالی بودن صف ۱
    queue_1_was_non_empty = False  # بررسی اینکه آیا صف ۱ درخواست داشته است
    skip_lower_priorities_until = None  # زمان پایان ممنوعیت پردازش صف‌های پایین‌تر

    while True:
        # ثبت اینکه صف ۱ حداقل یکبار درخواست داشته است
        if not queue_1_was_non_empty and not priority_queues[1].empty():
            queue_1_was_non_empty = True

        # اگر صف ۱ خالی شد، اجرای صف‌های دیگر را به مدت ۱۰ ثانیه متوقف کن
        if queue_1_was_non_empty and priority_queues[1].empty():
            if empty_1_count < 2:
                skip_lower_priorities_until = time.time() + 5  # تنظیم زمان توقف پردازش
                empty_1_count += 1
                continue  # بازگشت به ابتدای حلقه بدون پردازش صف‌های دیگر
            else:
                print('Other requeetst')
        else:
            empty_1_count = 0  # اگر صف ۱ دوباره درخواست داشته باشد، شمارنده ریست شود

        # اگر هنوز در زمان تأخیر هستیم، فقط صف ۱ پردازش شود
        if skip_lower_priorities_until and time.time() < skip_lower_priorities_until:
            priority_range = [1]  # فقط صف ۱ را پردازش کن
        else:
            priority_range = range(1, MAX_PRIORITY + 1)  # همه صف‌ها پردازش شوند
            skip_lower_priorities_until = None  # حذف محدودیت بعد از پایان تأخیر

        # پردازش از بالاترین اولویت تا پایین‌ترین
        for priority in priority_range:
            try:
                request_obj = priority_queues[priority].get(block=False)
                update_priority_delays(priority, 0)  # ریست کردن تأخیر صف پس از پردازش
                executors[priority].submit(request_obj.execute)
                break  # پس از پردازش یک درخواست، از حلقه خارج شود
            except queue.Empty:
                if priority == MAX_PRIORITY:
                    time.sleep(1)  # اگر همه صف‌ها خالی بودند، کمی صبر کند



@app.route('/remoteRequest', methods=['GET'])
def remote_request():
    """مسیر API برای دریافت درخواست و قرار دادن در صف مربوطه"""
    url = request.args.get('url', '')
    params = json.loads(request.args.get('params', '{}'))
    cookies = json.loads(request.args.get('cookies', '{}'))
    headers = json.loads(request.args.get('headers', '{}'))
    method = request.args.get('method', 'GET')
    data = json.loads(request.args.get('data', '{}')) if method == "post" else None
    json_data = json.loads(request.args.get('json', '{}')) if method == "post" else None

    timestamp = float(request.args.get('priorityTimestamp', time.time()))
    priority = get_priority(timestamp)

    exe_request = ExeRequest(method, url, params, cookies, headers, data, json_data)
    priority_queues[priority].put(exe_request)

    print(f"Queued Task with Priority {priority}")

    result = exe_request.future.result()
    return jsonify({'status_code': result.status_code, 'text': result.text, 'cookies': result.cookies.get_dict()})


# راه‌اندازی نخ‌های پردازش
threading.Thread(target=process_queues, daemon=True).start()

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1])  # دریافت پورت از آرگومان‌های خط فرمان
    app.run(host='0.0.0.0', port=port)


#_------------------








# import os
# import threading
# import queue
# import time
# import json
# import itertools
# import requests
# from flask import Flask, jsonify, request
# from concurrent.futures import ThreadPoolExecutor, Future
#
# # تنظیم عنوان ترمینال
# os.system("title Distribute Requests")
#
# app = Flask(__name__)
#
# # تعداد نخ‌های اختصاصی برای هر اولویت
# NUM_THREADS_PER_QUEUE = 1000
#
# # تعریف 10 صف اولویت و یک صف عمومی
# priority_queues = {i: queue.Queue() for i in range(1, 12)}
# general_queue = queue.Queue()
#
# # پردازشگرهای اختصاصی برای هر صف اولویت
# # executors = {i: ThreadPoolExecutor(max_workers=NUM_THREADS_PER_QUEUE) for i in range(1, 11)}
# # general_executor = ThreadPoolExecutor(max_workers=500)  # صف عمومی
#
#
# # تخصیص تعداد نخ‌های مختلف برای هر صف
# executors = {
#     1: ThreadPoolExecutor(max_workers=10000),  # اولویت 1 → 1000 نخ
#     2: ThreadPoolExecutor(max_workers=1000),   # اولویت 2 → 100 نخ
# }
# executors.update({i: ThreadPoolExecutor(max_workers=10) for i in range(3, 11)})  # بقیه صف‌ها → 1 نخ
# general_executor = ThreadPoolExecutor(max_workers=10)  # صف عمومی
#
#
#
#
# # شرط برای هماهنگ‌سازی پردازش‌ها
# condition = threading.Condition()
#
# class ExeRequest:
#     def __init__(self, method, url, params=None, cookies=None, headers=None, data=None, json=None):
#         self.url = url
#         self.params = params
#         self.cookies = cookies
#         self.headers = headers
#         self.method = method.lower()  # تبدیل به حروف کوچک برای یکپارچگی
#         self.data = data
#         self.json = json
#         self.future = Future()  # برای ذخیره نتیجه
#
#     def execute(self):
#         """اجرای درخواست HTTP"""
#         if self.method == "get":
#             response = requests.get(self.url, params=self.params, cookies=self.cookies, headers=self.headers,
#                                     data=self.data, json=self.json)
#         elif self.method == "post":
#             response = requests.post(self.url, params=self.params, cookies=self.cookies, headers=self.headers,
#                                      data=self.data, json=self.json)
#         else:
#             response = None
#
#         if response:
#             self.future.set_result(response)  # تنظیم نتیجه بدون نیاز به انتظار
#
#
# def process_queue(priority):
#     """پردازش درخواست‌ها برای یک صف خاص"""
#     while True:
#         try:
#             # print(f'----priority --- {priority}')
#             if (priority!= 1):
#                 time.sleep(priority)
#
#                 time.sleep(10)
#                 continue
#
#
#             else:
#                 ''
#
#             print(f'bardashttt az {priority}')
#
#             try:
#                 request_obj = priority_queues[priority].get(block=False)  # جلوگیری از قفل شدن در صورت خالی بودن صف
#             except queue.Empty:
#                 print(f'Empty queue {priority}')
#
#                 # time.sleep(priority+2)  # Wait before retrying
#                 continue  # Restart loop
#
#
#             # اجرای درخواست بدون انتظار برای نتیجه
#             executors[priority].submit(request_obj.execute)  # بدون .result()
#         except Exception as e:
#             print(e)
#
#
#         # result = executors[priority].submit(request_obj.execute).result()
#         # if result:
#         #     request_obj.future.set_result(result)
#
# def process_general_queue():
#     """پردازش درخواست‌های صف عمومی"""
#     while True:
#         time.sleep(5)
#
#         request_obj = general_queue.get()
#         general_executor.submit(request_obj.execute)
#
#         # if result:
#         #     request_obj.future.set_result(result)
#
#
#
# # مقداردهی اولیه شمارنده برای مرتب‌سازی درخواست‌ها
# task_counter = itertools.count()
#
# priority_mapping = {}  # جدول نگاشت تایم‌استمپ به اولویت
# priority_counter = 1  # شروع اولویت از 1 تا 10
# max_priority = 10  # حداکثر مقدار اولویت قبل از رفتن به صف عمومی
#
#
#
# import redis
# import json
# import threading
#
# # Connect to Redis
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
#
# # Key to store the list in Redis
# REDIS_KEY = "global_requests_list"
# MAX_PRIORITY = 10
# condition = threading.Condition()
# redis_client.delete(REDIS_KEY)
# def get_priority(timestamp):
#     with condition:  # Ensure thread safety
#         # Retrieve the current list from Redis
#         data = redis_client.get(REDIS_KEY)
#         global_requests_list = json.loads(data) if data else []
#
#         # Convert list to a set to remove duplicates, then back to a list
#         global_requests_list = list(set(global_requests_list))
#
#         # Add the new timestamp
#         global_requests_list.append(timestamp)
#
#         # Convert to set again to remove duplicates, then back to a sorted list
#         global_requests_list = sorted(set(global_requests_list))
#
#         # Update Redis with the new sorted list
#         redis_client.set(REDIS_KEY, json.dumps(global_requests_list))
#
#         # Compute priority
#         priority_mapping = {t: min(i + 1, MAX_PRIORITY) for i, t in enumerate(global_requests_list)}
#
#         return priority_mapping[timestamp]
#
#
# #
# # def get_priority(timestamp):
# #     global priority_counter
# #
# #     with condition:  # اطمینان از ایمنی در برابر دسترسی همزمان
# #         if timestamp in priority_mapping:
# #             return priority_mapping[timestamp]  # بازگرداندن اولویت ذخیره‌شده
# #
# #         # تعیین اولویت جدید
# #         priority = priority_counter
# #         priority_mapping[timestamp] = priority  # ذخیره در مپینگ
# #
# #         # افزایش مقدار اولویت، و چرخش بین 1 تا max_priority
# #         priority_counter = priority_counter + 1 if priority_counter < max_priority else 11
# #
# #         return priority
#
#
# @app.route('/remoteRequest', methods=['GET'])
# def remote_request():
#     """مسیر API برای دریافت درخواست و قرار دادن در صف مربوطه"""
#     url = request.args.get('url', '')
#     params = json.loads(request.args.get('params', '{}'))
#     cookies = json.loads(request.args.get('cookies', '{}'))
#     headers = json.loads(request.args.get('headers', '{}'))
#     method = request.args.get('method', 'GET')
#     data = json.loads(request.args.get('data', '{}')) if method == "post" else None
#     json_data = json.loads(request.args.get('json', '{}')) if method == "post" else None
#
#     # استخراج و مپ کردن تایم‌استمپ به اولویت
#     timestamp = float(request.args.get('priorityTimestamp', time.time()))
#     priority=get_priority(timestamp)
#
#     # ایجاد یک شیء درخواست
#     exe_request = ExeRequest(method, url, params, cookies, headers, data, json_data)
#
#     # اضافه کردن درخواست به صف مربوطه
#     if priority <= 10:
#         priority_queues[priority].put(exe_request)
#     else:
#         general_queue.put(exe_request)
#
#     print(f"Queued Task with Priority {priority}")
#
#     # منتظر اجرا شدن درخواست و دریافت نتیجه
#     result = exe_request.future.result()
#     print(f'status_code === {result.status_code}')
#     return jsonify({
#         'status_code': result.status_code,
#         'text': result.text,
#         'cookies': result.cookies.get_dict()
#     })
#
# # راه‌اندازی نخ‌های پردازش برای 10 صف اولویت
# for i in range(1, 12):
#     threading.Thread(target=process_queue, args=(i,), daemon=True).start()
#
# # راه‌اندازی نخ پردازش صف عمومی
# threading.Thread(target=process_general_queue, daemon=True).start()
#
# if __name__ == '__main__':
#     import sys
#     port = int(sys.argv[1])  # دریافت پورت از آرگومان‌های خط فرمان
#     # port=6000
#     app.run(host='0.0.0.0', port=port)
#
