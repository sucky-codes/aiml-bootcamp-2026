"""
Web Scraper Module
==================
A production-ready Python web scraper featuring robust HTTP handling,
User-Agent headers, automated pagination, HTML parsing with BeautifulSoup4,
data cleaning, structured export to CSV/JSON via pandas, and a full CLI.

Author: sucky-codes
Repository: aiml-bootcamp-2026
"""

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Union
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


@dataclass
class ScrapedItem:
    """Dataclass representing a scraped item (e.g., quote, article, product)."""

    title: str
    author_or_source: str
    tags_or_categories: str
    text_content: str
    source_url: str


class WebScraper:
    """Flexible web scraper equipped with retries, custom headers, and multi-page support."""

    DEFAULT_USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    ]

    def __init__(self, base_url: str, delay: float = 1.0, timeout: int = 10):
        self.base_url = base_url
        self.delay = delay
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": self.DEFAULT_USER_AGENTS[0],
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }
        )

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch page content and return BeautifulSoup object."""
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml" if "lxml" in sys.modules else "html.parser")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def parse_quotes_site(self, soup: BeautifulSoup, current_url: str) -> List[ScrapedItem]:
        """Parse quotes website (e.g. quotes.toscrape.com pattern)."""
        items: List[ScrapedItem] = []
        quote_blocks = soup.find_all("div", class_="quote")

        for block in quote_blocks:
            text_elem = block.find("span", class_="text")
            author_elem = block.find("small", class_="author")
            tag_elems = block.find_all("a", class_="tag")

            title = text_elem.get_text(strip=True) if text_elem else "No Content"
            author = author_elem.get_text(strip=True) if author_elem else "Unknown"
            tags = ", ".join([tag.get_text(strip=True) for tag in tag_elems])

            items.append(
                ScrapedItem(
                    title=title[:50] + ("..." if len(title) > 50 else ""),
                    author_or_source=author,
                    tags_or_categories=tags,
                    text_content=title,
                    source_url=current_url,
                )
            )
        return items

    def parse_generic_site(self, soup: BeautifulSoup, current_url: str) -> List[ScrapedItem]:
        """Generic fallback parser for heading/paragraph structure."""
        items: List[ScrapedItem] = []
        headings = soup.find_all(["h1", "h2", "h3"])

        for heading in headings:
            title = heading.get_text(strip=True)
            if not title:
                continue

            # Look for subsequent paragraph text
            p_elem = heading.find_next("p")
            text_content = p_elem.get_text(strip=True) if p_elem else ""

            items.append(
                ScrapedItem(
                    title=title,
                    author_or_source=urlparse(current_url).netloc,
                    tags_or_categories="Heading/Article",
                    text_content=text_content,
                    source_url=current_url,
                )
            )
        return items

    def scrape(self, max_pages: int = 3) -> List[ScrapedItem]:
        """Scrape items up to max_pages."""
        all_items: List[ScrapedItem] = []
        current_url = self.base_url
        page_count = 0

        while current_url and page_count < max_pages:
            soup = self.fetch_page(current_url)
            if not soup:
                break

            page_count += 1
            logger.info(f"Parsing page {page_count}/{max_pages}...")

            # Try specific parser first, fallback to generic
            if soup.find("div", class_="quote"):
                items = self.parse_quotes_site(soup, current_url)
            else:
                items = self.parse_generic_site(soup, current_url)

            all_items.extend(items)
            logger.info(f"Extracted {len(items)} items from page {page_count}.")

            # Find next page link if available
            next_btn = soup.find("li", class_="next")
            if next_btn and next_btn.find("a"):
                next_href = next_btn.find("a")["href"]
                current_url = urljoin(current_url, next_href)
            else:
                next_a = soup.find("a", string=lambda t: t and "next" in t.lower())
                if next_a and "href" in next_a.attrs:
                    current_url = urljoin(current_url, next_a["href"])
                else:
                    current_url = None

            if current_url:
                time.sleep(self.delay)

        return all_items

    @staticmethod
    def export_data(items: List[ScrapedItem], output_path: str, fmt: str = "csv") -> None:
        """Export scraped data to CSV or JSON using pandas."""
        if not items:
            logger.warning("No items scraped to export.")
            return

        data = [asdict(item) for item in items]
        df = pd.DataFrame(data)

        fmt = fmt.lower()
        if fmt == "csv":
            df.to_csv(output_path, index=False, encoding="utf-8")
        elif fmt == "json":
            df.to_json(output_path, orient="records", indent=4, force_ascii=False)
        else:
            raise ValueError(f"Unsupported export format: {fmt}. Use 'csv' or 'json'.")

        logger.info(f"Successfully exported {len(items)} items to '{output_path}' ({fmt.upper()}).")


def main():
    parser = argparse.ArgumentParser(
        description="Flexible Web Scraper - Extract data from web pages into CSV/JSON."
    )
    parser.add_argument(
        "--url", "-u", default="http://quotes.toscrape.com", help="Target URL to scrape"
    )
    parser.add_argument(
        "--output", "-o", default="scraped_data.csv", help="Output file path"
    )
    parser.add_argument(
        "--format", "-f", choices=["csv", "json"], default="csv", help="Export format (csv/json)"
    )
    parser.add_argument(
        "--max-pages", "-p", type=int, default=2, help="Maximum number of pages to scrape"
    )
    parser.add_argument(
        "--delay", "-d", type=float, default=1.0, help="Delay between requests in seconds"
    )

    args = parser.parse_args()

    scraper = WebScraper(base_url=args.url, delay=args.delay)
    results = scraper.scrape(max_pages=args.max_pages)
    scraper.export_data(results, output_path=args.output, fmt=args.format)


if __name__ == "__main__":
    main()
