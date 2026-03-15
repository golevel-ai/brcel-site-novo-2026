#!/usr/bin/env python3
"""Sync remote image assets into the local project.

This script is meant to mirror the remote assets used by the public demo at
https://ex-coders.com/html/pubzi/index.html?storefront=envato-elements.

It scans the local HTML files to find references to image assets (png/jpg/svg/webp/gif)
and downloads those files from the remote demo site into the same relative path
within this repo (overwriting existing files).

Usage:
  python3 sync_images_from_remote.py

Configuration:
  - BASE_URL: remote base URL for the demo site (must end with a slash)
  - LOCAL_ROOT: path to the local "Buyer files" directory (where HTML lives)

Note: this script only downloads image assets referenced directly by the HTML.
To fetch images referenced inside CSS, run it again after downloading CSS or add
additional parsing logic.
"""

import argparse
import os
import re
import sys
from typing import Optional, Set
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Remote demo site base URL (must end with '/')
BASE_URL = "https://ex-coders.com/html/pubzi/"
# Local root where HTML/assets live
LOCAL_ROOT = os.path.join(os.path.dirname(__file__), "..")

IMG_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp"}

HTML_EXTENSIONS = {".html", ".htm"}

IMG_SRC_RE = re.compile(r'<img\s+[^>]*?src=[\'\"]([^\'\"]+)[\'\"]', re.IGNORECASE)
CSS_URL_RE = re.compile(r'url\(\s*[\'\"]?([^\'\"\)]+)[\'\"]?\s*\)', re.IGNORECASE)


def find_local_html_files(root: str):
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in HTML_EXTENSIONS:
                yield os.path.join(dirpath, fn)


def extract_image_paths_from_html(html: str) -> Set[str]:
    paths = set()
    for match in IMG_SRC_RE.finditer(html):
        paths.add(match.group(1))

    # also consider CSS links (so we can pull CSS if desired)
    for match in re.finditer(r'<link[^>]+href=[\'\"]([^\'\"]+)[\'\"]', html, re.IGNORECASE):
        paths.add(match.group(1))

    # inlined styles
    for match in CSS_URL_RE.finditer(html):
        paths.add(match.group(1))

    return paths


def is_image_path(path: str) -> bool:
    lower = path.lower()
    return any(lower.endswith(ext) for ext in IMG_EXTENSIONS)


def normalize_path(path: str) -> str:
    # Keep only urls with relative paths (no protocol) and starting with assets/
    # If they start with '/', strip it so we can join under base.
    if path.startswith("//"):
        return ""  # skip protocol-relative
    if re.match(r"https?://", path):
        return ""  # skip absolute URLs
    if path.startswith("/"):
        path = path.lstrip("/")
    return path


def download_url(url: str, retries: int = 3, pause_sec: float = 0.2) -> Optional[bytes]:
    for attempt in range(1, retries + 1):
        try:
            req = Request(url, headers={
                "User-Agent": "Mozilla/5.0",
                "Connection": "close",
            })
            with urlopen(req, timeout=30) as response:
                return response.read()
        except HTTPError as e:
            print(f"⚠️ HTTP error for {url}: {e.code} {e.reason}")
            return None
        except URLError as e:
            print(f"⚠️ URL error for {url} (attempt {attempt}/{retries}): {e}")
        except Exception as e:
            print(f"⚠️ Error downloading {url} (attempt {attempt}/{retries}): {e}")
        if attempt < retries:
            import time

            time.sleep(pause_sec)
    return None


def main():
    parser = argparse.ArgumentParser(description="Sync image assets from remote demo site.")
    parser.add_argument("--base", default=BASE_URL, help="Remote base URL (must end with /)")
    parser.add_argument("--root", default=LOCAL_ROOT, help="Local root folder of the project")
    parser.add_argument("--dry-run", action="store_true", help="List downloads without writing files")
    args = parser.parse_args()

    base_url = args.base
    root = os.path.abspath(args.root)

    print(f"Scanning HTML files under: {root}")
    all_paths = set()
    for html_file in find_local_html_files(root):
        with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
            contents = f.read()
        paths = extract_image_paths_from_html(contents)
        for p in paths:
            norm = normalize_path(p)
            if not norm:
                continue
            if is_image_path(norm):
                all_paths.add(norm)

    if not all_paths:
        print("No image paths found in HTML files.")
        return 0

    print(f"Found {len(all_paths)} referenced image paths.")
    downloaded = 0
    skipped = 0

    for rel_path in sorted(all_paths):
        if not is_image_path(rel_path):
            continue
        remote_url = urljoin(base_url, rel_path)
        local_path = os.path.join(root, rel_path.replace("/../", "/"))
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        print(f"-> {rel_path}")
        if args.dry_run:
            continue
        data = download_url(remote_url)
        if data is None:
            skipped += 1
            continue
        with open(local_path, "wb") as f:
            f.write(data)
        downloaded += 1

    print(f"Downloaded: {downloaded}, skipped: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
