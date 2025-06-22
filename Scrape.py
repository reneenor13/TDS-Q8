import httpx
from lxml import html
import json
from datetime import datetime, timezone

def scrape_discourse_topics(base_url: str, category_path: str = "/c", max_topics: int = 10):
    """
    Scrapes the titles and URLs of the latest topics from a Discourse category page.

    Args:
        base_url (str): Base URL of the Discourse forum (e.g., "https://discourse.example.com").
        category_path (str): Path to the category to scrape (default is "/c" for categories).
        max_topics (int): Maximum number of topics to scrape.

    Returns:
        list of dict: List of topics with title, url, and scraped_at timestamp.
    """
    url = f"{base_url}{category_path}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; DiscourseScraper/1.0)"}

    try:
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except httpx.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return []

    tree = html.fromstring(response.text)
    topics = []

    # CSS selectors depend on the Discourse theme; this is a common selector for topic links
    topic_elements = tree.cssselect("a.topic-title")

    for topic_el in topic_elements[:max_topics]:
        title = topic_el.text_content().strip()
        relative_url = topic_el.get("href")
        full_url = f"{base_url}{relative_url}" if relative_url.startswith("/") else relative_url

        topics.append({
            "title": title,
            "url": full_url,
            "scraped_at": datetime.now(timezone.utc).isoformat()
        })

    return topics


if __name__ == "__main__":
    # Example usage
    forum_url = "https://discourse.onlinedegree.iitm.ac.in"
    category = "/c/courses/tds-kb/34"

    data = scrape_discourse_topics(forum_url, category, max_topics=10)

    # Save to JSON file with timestamp in filename
    filename = f"discourse_topics_{date
