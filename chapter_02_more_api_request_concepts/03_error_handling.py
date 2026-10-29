"""
Chapter 2 - Lesson 3: Error handling

Covers:
  - 4XX (client) vs 5XX (server) error status codes
  - checking status codes manually
  - ConnectionError for failures before a response exists
  - raise_for_status() and HTTPError
  - combining both in one try/except

httpbin.org's /status/<code> endpoint returns whatever status code we ask for,
which makes it ideal for practising error handling.
"""

import os

import requests

BASE_URL = os.environ.get("ERR_DEMO_BASE_URL", "https://httpbin.org")

# An address nothing listens on, so the request fails before reaching a server
UNREACHABLE_URL = "http://127.0.0.1:9"


# --------------------------------------------------------------------------
# 1. Classifying error status codes
# --------------------------------------------------------------------------
def classify_status(code: int) -> str:
    """Tell apart success, client errors (4XX) and server errors (5XX)."""
    if code == 429:
        return "client error: too many requests, slow down (rate limiting)"
    if 400 <= code < 500:
        return "client error: fix the request (headers, auth, URL...)"
    if 500 <= code < 600:
        return "server error: not our fault, but our code must cope with it"
    return "no error"


# --------------------------------------------------------------------------
# 2. Simple approach: check the status code manually
# --------------------------------------------------------------------------
def get_checking_status_code(url: str):
    """Works for error responses, but misses failures with no response at all."""
    response = requests.get(url)
    if response.status_code >= 400:
        print(f"  Error {response.status_code}: {classify_status(response.status_code)}")
        return None
    return response


# --------------------------------------------------------------------------
# 3. Better: ConnectionError + raise_for_status()
# --------------------------------------------------------------------------
def safe_get(url: str):
    """
    Combine both checks:
      - ConnectionError: the request never reached the server (no response)
      - HTTPError: raised by raise_for_status() for any 4XX/5XX response
    Returns the response on success, or None after reporting the problem.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raises HTTPError for 4XX and 5XX
    except requests.exceptions.ConnectionError as err:
        print("  Connection error (no response received):", type(err).__name__)
        return None
    except requests.exceptions.HTTPError as err:
        code = err.response.status_code
        print(f"  HTTP error {code}: {classify_status(code)}")
        return None
    return response


if __name__ == "__main__":
    print("--- Classifying status codes ---")
    for code in (200, 401, 404, 429, 500, 502, 504):
        print(f"  {code}: {classify_status(code)}")

    print("\n--- Manual status code check ---")
    for code in (200, 404, 500):
        print(f"GET /status/{code}")
        result = get_checking_status_code(f"{BASE_URL}/status/{code}")
        print("  ->", "OK" if result is not None else "failed")

    print("\n--- raise_for_status() + ConnectionError ---")
    for label, url in [
        ("success (200)", f"{BASE_URL}/status/200"),
        ("not found (404)", f"{BASE_URL}/status/404"),
        ("too many requests (429)", f"{BASE_URL}/status/429"),
        ("server error (500)", f"{BASE_URL}/status/500"),
        ("unreachable server", UNREACHABLE_URL),
    ]:
        print(f"Case: {label}")
        result = safe_get(url)
        print("  ->", "got a response" if result is not None else "handled the error")