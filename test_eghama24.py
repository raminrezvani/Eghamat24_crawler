import requests


def test_fetch_hotels(target='MHD', startdate='2024-10-16', stay='3'):
    # url = 'http://127.0.0.1:5000/fetch_hotels'
    url = 'http://45.149.76.168:8022/fetch_hotels'
    params = {
        'target': target,
        'startdate': startdate,
        'stay': stay
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Response JSON:")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")


if __name__ == '__main__':
    test_fetch_hotels()