#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from bs4 import BeautifulSoup
import pathlib
import urllib.parse
import logging_config
import requests

HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,it-IT;q=0.8,it;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.splunk.com/en_us/download/universal-forwarder.html?locale=en_us",
    "sec-ch-ua": '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
}


def download_file(url: str) -> pathlib.Path:
    filename = pathlib.Path(urllib.parse.urlparse(url).path).name
    downloaded_bytes = 0
    try:
        logging_config.logger.info(f"[NET] Starting download: {url}")
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(filename, "wb") as file_handle:
                for chunk in response.iter_content(chunk_size=8192):
                    file_handle.write(chunk)
                    downloaded_bytes += len(chunk)
                    logging_config.logger.debug(
                        f"[NET] Bytes downloaded: {downloaded_bytes}"
                    )
        logging_config.logger.info(f"[NET] Download complete: {filename}")
    except requests.RequestException as e:
        logging_config.logger.error(
            f"[NET] Download failed for {filename}. Details: {e}"
        )
        raise
    return pathlib.Path(filename).absolute()


def fetch_latest_splunk_url() -> str:
    logging_config.logger.info(
        "[NET] Fetching latest Splunk Universal Forwarder URL..."
    )
    response = requests.get(
        "https://www.splunk.com/en_us/download/universal-forwarder.html?locale=en_us",
        headers=HEADERS,
    )

    soup = BeautifulSoup(response.text, "html.parser")
    tag = soup.select_one('a[data-arch="x86_64"][data-filename$=".tgz"]')

    if tag and "data-link" in tag.attrs:
        found_url = str(tag["data-link"])
        logging_config.logger.info(f"[NET] Found URL: {found_url}")
        return found_url

    logging_config.logger.error("[NET] Could not find download link in page.")
    raise ValueError("Download link not found.")
