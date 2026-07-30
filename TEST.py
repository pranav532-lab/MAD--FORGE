import requests

API_KEY = "e12d923d58499a8e2237a9fa95e20ba914ff6398"

url = "https://google.serper.dev/search"

payload = {
    "q": "digital marketing agencies chennai"
}

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

response = requests.post(
    url,
    json=payload,
    headers=headers
)

print(response.status_code)
print(response.json())