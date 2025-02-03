import requests
from concurrent.futures import ThreadPoolExecutor

# with open('lst_proxy.txt','r',encoding='utf8') as f:
#     lst=f.read()
#     lst=lst.split('\n')


# Load proxies from file
with open('lst_proxy.txt', 'r', encoding='utf8') as f:
    lst = f.read().splitlines()  # Removes trailing newlines

# Test URL
test_url = "https://www.eghamat24.ir"  # This returns your public IP, useful for testing

def check_proxy(proxy):
    """Function to check if a proxy is working"""
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",  # Change to https if needed
    }
    try:
        response = requests.get(test_url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            print(f"✅ Working proxy: {proxy}")

            ress=requests.get('https://www.eghamat24.com/search/Kish/03-11-18/3',proxies=proxies)
            with open('res.html', 'w', encoding='utf8') as f:
                f.write(ress.text)
                f.close()
            return proxy  # Return working proxy
    except requests.RequestException:
        print(f"❌ Failed proxy: {proxy}")
    return None

# Use ThreadPoolExecutor to check proxies concurrently
with ThreadPoolExecutor(max_workers=100) as executor:
    valid_proxies = list(filter(None, executor.map(check_proxy, lst)))

# Save valid proxies
if valid_proxies:
    with open('valid_proxies.txt', 'w', encoding='utf8') as f:
        f.write("\n".join(valid_proxies))
    print("✅ Valid proxies saved to valid_proxies.txt")
else:
    print("❌ No valid proxies found.")

#
#
proxies = {
    # "http": "157.254.53.50:80",
    "https": f"http://180.210.89.215:3128",

}

url = 'https://www.eghamat24.ir'
response = requests.get(url, proxies=proxies)

response = requests.get(url)
#
#
#
# if res.status_code==200:
#     print('asdasdasd')
#
