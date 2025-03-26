import requests

# Basic call with required parameters
# response = requests.get(
#     "http://localhost:5001/booking_tours",
#     params={
#         "start_date": "2025-04-01",
#         "night_count": 3
#     }
# )
# print(response.json())


# Basic call with required parameters
response = requests.get(
    "http://localhost:5021/jimbo_tours",
    params={
        "start_date": "2025-04-05",
        "night_count": 3
    }
)
print(response.json())


# # Full call with all parameters
# response = requests.get(
#     "http://localhost:5001/booking_tours",
#     params={
#         "start_date": "2025-04-01",
#         "night_count": 3,
#         "adults": "2",
#         "source": "MHD",
#         "target": "KIH"
#     }
# )
# print(response.json())