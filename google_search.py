import requests

from database import website_exists

API_KEY = "YOUR_SERPER_API_KEY"

URL = "https://google.serper.dev/search"

BLOCKED_DOMAINS = [
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "youtube.com",
    "reddit.com",
    "justdial.com",
    "indiamart.com",
]


def search_google(search_queries):

    new_websites = []
    seen = set()

    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    for query in search_queries["queries"]:

        try:
            response = requests.post(
                URL,
                headers=headers,
                json={"q": query},
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

        except Exception as e:
            print(f"Search failed for query: {query}")
            print(e)
            continue

        organic_results = data.get("organic", [])

        for item in organic_results[:5]:

            website = item.get("link")

            if not website:
                continue

            if any(domain in website.lower() for domain in BLOCKED_DOMAINS):
                continue

            if website in seen:
                continue

            seen.add(website)

            if website_exists(website):
                continue

            new_websites.append({
                "search_query": query,
                "title": item.get("title", ""),
                "website": website,
                "snippet": item.get("snippet", "")
            })

    return new_websites