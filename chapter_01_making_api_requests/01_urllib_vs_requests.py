"""
Chapter 1 - Lesson 1: Introduction to APIs.
Compare urllib (standard library) with requests (third-party) for a simple GET.

Note: the DataCamp course uses its own hosted "music catalog" API. That API only
works inside the course platform, so BASE_URL below points to a free public
practice API (JSONPlaceholder). Swap BASE_URL if you have another REST API.
"""

import urllib.request

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"
ENDPOINT = "/posts"  # the course uses something like /albums
URL = f"{BASE_URL}{ENDPOINT}"


def fetch_with_urllib(url: str) -> str:
    """GET using urllib: send request, read bytes, decode to text."""
    with urllib.request.urlopen(url) as response:  # 1. send the request
        raw_bytes = response.read()                # 2. read the response body
    return raw_bytes.decode("utf-8")               # 3. decode bytes -> str


def fetch_with_requests(url: str) -> str:
    """GET using requests: reading and decoding are handled for us."""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    urllib_data = fetch_with_urllib(URL)
    requests_data = fetch_with_requests(URL)

    print("urllib   ->", urllib_data[:150], "...")
    print("requests ->", requests_data[:150], "...")
    print("Same content?", urllib_data == requests_data)