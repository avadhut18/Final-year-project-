import requests
from bs4 import BeautifulSoup


def scrape_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        return soup.get_text(separator="\n", strip=True)[:5000]
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return "Failed to scrape content."
