import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}


IMPORTANT_PAGES = [
    "",
    "/contact",
    "/contact-us",
    "/about",
    "/about-us",
    "/services",
    "/solutions",
    "/team",
    "/our-team",
    "/careers"
]


EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

PHONE_REGEX = (
    r"(?:\+?\d{1,3}[-.\s]?)?"
    r"(?:\(?\d{2,5}\)?[-.\s]?)?"
    r"\d{3,5}[-.\s]?\d{3,5}"
)


SOCIAL_DOMAINS = [
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "x.com",
    "youtube.com"
]


def scrape_website(website):

    scraped_data = {
        "website": website,
        "title": "",
        "meta_description": "",
        "headings": [],
        "text": "",
        "emails": [],
        "phone_numbers": [],
        "addresses": [],
        "social_links": [],
        "links": []
    }

    visited = set()

    for page in IMPORTANT_PAGES:

        url = urljoin(website, page)

        if url in visited:
            continue

        visited.add(url)

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # -----------------------
            # Title
            # -----------------------

            if not scraped_data["title"] and soup.title:
                scraped_data["title"] = soup.title.get_text(strip=True)

            # -----------------------
            # Meta Description
            # -----------------------

            meta = soup.find("meta", attrs={"name": "description"})

            if meta and not scraped_data["meta_description"]:
                scraped_data["meta_description"] = meta.get("content", "")

            # -----------------------
            # Headings
            # -----------------------

            for tag in soup.find_all(["h1", "h2", "h3"]):

                heading = tag.get_text(" ", strip=True)

                if heading:
                    scraped_data["headings"].append(heading)

            # -----------------------
            # Paragraph Text
            # -----------------------

            for p in soup.find_all("p"):

                paragraph = p.get_text(" ", strip=True)

                if paragraph:
                    scraped_data["text"] += paragraph + "\n"

            # -----------------------
            # Emails
            # -----------------------

            emails = re.findall(
                EMAIL_REGEX,
                soup.get_text(" ")
            )

            scraped_data["emails"].extend(emails)

            # -----------------------
            # Phone Numbers
            # -----------------------

            phones = re.findall(
                PHONE_REGEX,
                soup.get_text(" ")
            )

            scraped_data["phone_numbers"].extend(phones)

            # -----------------------
            # Links
            # -----------------------

            for link in soup.find_all("a", href=True):

                href = urljoin(url, link["href"])

                scraped_data["links"].append(href)

                lower = href.lower()

                for social in SOCIAL_DOMAINS:

                    if social in lower:
                        scraped_data["social_links"].append(href)

            # -----------------------
            # Address (very basic)
            # -----------------------

            address_keywords = [
                "address",
                "location",
                "office"
            ]

            for element in soup.find_all(["p", "div", "span"]):

                text = element.get_text(" ", strip=True)

                if any(keyword in text.lower() for keyword in address_keywords):

                    if len(text) < 300:
                        scraped_data["addresses"].append(text)

        except Exception:

            continue

    # -----------------------
    # Remove Duplicates
    # -----------------------

    scraped_data["headings"] = list(set(scraped_data["headings"]))
    scraped_data["emails"] = list(set(scraped_data["emails"]))
    scraped_data["phone_numbers"] = list(set(scraped_data["phone_numbers"]))
    scraped_data["addresses"] = list(set(scraped_data["addresses"]))
    scraped_data["social_links"] = list(set(scraped_data["social_links"]))
    scraped_data["links"] = list(set(scraped_data["links"]))

    return scraped_data