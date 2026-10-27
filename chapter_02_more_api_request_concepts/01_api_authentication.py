"""
Chapter 2 - Lesson 1: API Authentication

Covers:
  - why APIs need authentication (401 Unauthorized vs 200 OK)
  - Basic authentication using the `auth` argument
  - what Basic auth really sends (base64 is NOT encryption)
  - API key / token authentication via query parameter and via header

The DataCamp "album API" only exists inside the course platform, so this script
uses httpbin.org, a public service built for testing HTTP requests:
  /basic-auth/<user>/<password>  -> 200 if credentials match, else 401
  /bearer                        -> 200 if an Authorization: Bearer header is sent
  /get                           -> echoes the query parameters it receives

Never hardcode real credentials. Read them from environment variables instead.
"""

import base64
import os

import requests

BASE_URL = os.environ.get("AUTH_DEMO_BASE_URL", "https://httpbin.org")

# Demo credentials (httpbin accepts whatever user/password are in the URL).
# For a real API, set these as environment variables, e.g. in Git Bash:
#   export API_USERNAME="me"; export API_PASSWORD="secret"; export API_KEY="abc123"
USERNAME = os.environ.get("API_USERNAME", "user")
PASSWORD = os.environ.get("API_PASSWORD", "passwd")
API_KEY = os.environ.get("API_KEY", "demo-token-123")


# --------------------------------------------------------------------------
# 1. No authentication -> 401
# --------------------------------------------------------------------------
def get_without_auth(url: str) -> requests.Response:
    """A protected resource with no credentials returns 401 Unauthorized."""
    return requests.get(url)


# --------------------------------------------------------------------------
# 2. Basic authentication
# --------------------------------------------------------------------------
def get_with_basic_auth(url: str, username: str, password: str) -> requests.Response:
    """Pass a (username, password) tuple; requests encodes it and adds the header."""
    return requests.get(url, auth=(username, password))


def build_basic_auth_header(username: str, password: str) -> dict:
    """
    What requests does for you: base64-encode 'username:password' and put it
    in the Authorization header.
    """
    credentials = f"{username}:{password}".encode("utf-8")
    encoded = base64.b64encode(credentials).decode("utf-8")
    return {"Authorization": f"Basic {encoded}"}


def decode_basic_auth_header(header_value: str) -> str:
    """Base64 is two-way: anyone who sees the header can decode it."""
    encoded = header_value.removeprefix("Basic ")
    return base64.b64decode(encoded).decode("utf-8")


# --------------------------------------------------------------------------
# 3. API key / token authentication
# --------------------------------------------------------------------------
def get_with_key_as_param(url: str, api_key: str) -> requests.Response:
    """Option 1: send the key as a query parameter via `params`."""
    return requests.get(url, params={"access_token": api_key})


def get_with_key_in_header(url: str, api_key: str) -> requests.Response:
    """
    Option 2 (usually preferred): send the key in an Authorization header.
    requests has no shortcut for this, so we build the header ourselves.
    The exact format ("Bearer ...", "Token ...") depends on the API docs.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    return requests.get(url, headers=headers)


if __name__ == "__main__":
    basic_url = f"{BASE_URL}/basic-auth/{USERNAME}/{PASSWORD}"

    print("--- No credentials ---")
    print("Status:", get_without_auth(basic_url).status_code)  # 401

    print("\n--- Basic auth (auth=(user, pass)) ---")
    resp = get_with_basic_auth(basic_url, USERNAME, PASSWORD)
    print("Status:", resp.status_code)  # 200
    print("Body  :", resp.json())

    print("\n--- Basic auth with wrong password ---")
    print("Status:", get_with_basic_auth(basic_url, USERNAME, "wrong").status_code)  # 401

    print("\n--- What Basic auth really sends ---")
    header = build_basic_auth_header(USERNAME, PASSWORD)
    print("Header :", header)
    print("Decoded:", decode_basic_auth_header(header["Authorization"]))

    print("\n--- API key as query parameter ---")
    resp = get_with_key_as_param(f"{BASE_URL}/get", API_KEY)
    print("Final URL:", resp.url)

    print("\n--- API key in Authorization header ---")
    print("No header :", get_without_auth(f"{BASE_URL}/bearer").status_code)  # 401
    resp = get_with_key_in_header(f"{BASE_URL}/bearer", API_KEY)
    print("With token:", resp.status_code, resp.json())  # 200
    