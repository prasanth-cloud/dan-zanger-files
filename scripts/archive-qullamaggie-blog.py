#!/usr/bin/env python3
"""
Archives blog posts from qullamaggie.com with text content and embedded images.
Saves each post as a markdown file with downloaded images.
"""

import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "charts" / "qullamaggie" / "blog"
IMAGES_DIR = OUTPUT_DIR / "images"
BASE_URL = "https://qullamaggie.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def fetch(url):
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp


def get_post_links():
    """Discover blog post URLs from the main page and archives."""
    links = set()
    for page_url in [BASE_URL, f"{BASE_URL}/blog", f"{BASE_URL}/archives"]:
        try:
            soup = BeautifulSoup(fetch(page_url).text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                full = urljoin(BASE_URL, href)
                if BASE_URL in full and full != BASE_URL and "/page/" not in full:
                    links.add(full)
        except Exception as e:
            print(f"  Skipping {page_url}: {e}")
    return sorted(links)


def download_image(img_url, post_slug):
    """Download image and return local relative path."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{post_slug}_{Path(urlparse(img_url).path).name}"
    filepath = IMAGES_DIR / filename
    if filepath.exists():
        return f"images/{filename}"
    try:
        resp = requests.get(img_url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        filepath.write_bytes(resp.content)
    except Exception:
        return img_url
    return f"images/{filename}"


def archive_post(url):
    """Download a single blog post as markdown with images."""
    slug = urlparse(url).path.strip("/").replace("/", "_") or "index"
    output_file = OUTPUT_DIR / f"{slug}.md"
    if output_file.exists():
        return

    try:
        soup = BeautifulSoup(fetch(url).text, "html.parser")
    except Exception as e:
        print(f"  Failed: {url} - {e}")
        return

    title_tag = soup.find("h1") or soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else slug

    article = soup.find("article") or soup.find("main") or soup.find("div", class_="post")
    if not article:
        article = soup.body

    for img in article.find_all("img", src=True):
        img_url = urljoin(url, img["src"])
        local_path = download_image(img_url, slug)
        img["src"] = local_path

    text = article.get_text("\n", strip=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(f"# {title}\n\nSource: {url}\n\n---\n\n{text}\n")

    print(f"  Archived: {title}")
    time.sleep(1)


def main():
    print("Discovering blog posts...")
    links = get_post_links()
    print(f"Found {len(links)} links to archive")

    for url in links:
        archive_post(url)

    print(f"\nBlog archived to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
