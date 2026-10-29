"""
Final wrap-up: a small reusable API helper that combines the whole course.

Brings together:
  - HTTP verbs (GET / POST / PUT / DELETE)       -> Chapter 1
  - query params, headers, status codes          -> Chapter 1
  - token authentication via headers             -> Chapter 2
  - JSON in and out                              -> Chapter 2
  - ConnectionError / HTTPError handling         -> Chapter 2

Usage:
    python final_wrap_up/api_client.py
Optional: export API_TOKEN="your-token" to send an Authorization header.
"""

import os
from typing import Any, Optional

import requests

BASE_URL = os.environ.get("CLIENT_DEMO_BASE_URL", "https://jsonplaceholder.typicode.com")
API_TOKEN = os.environ.get("API_TOKEN")  # never hardcode secrets
DEFAULT_TIMEOUT = 10  # seconds


def request_json(
    method: str,
    endpoint: str,
    params: Optional[dict] = None,
    json_body: Optional[dict] = None,
    token: Optional[str] = API_TOKEN,
) -> Optional[Any]:
    """
    Send a request and return the decoded JSON, or None if anything went wrong.

    method     : "GET", "POST", "PUT" or "DELETE"
    endpoint   : path such as "/posts/1"
    params     : query parameters (dict)
    json_body  : data to send as JSON (dict)
    token      : optional API token, sent as a Bearer header
    """
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.request(
            method.upper(),
            f"{BASE_URL}{endpoint}",
            params=params,
            json=json_body,
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print(f"[{method} {endpoint}] could not reach the server")
        return None
    except requests.exceptions.Timeout:
        print(f"[{method} {endpoint}] request timed out")
        return None
    except requests.exceptions.HTTPError as err:
        print(f"[{method} {endpoint}] HTTP {err.response.status_code}")
        return None

    # Some successful responses (e.g. DELETE) may have an empty body
    return response.json() if response.content else {}


if __name__ == "__main__":
    print("GET with query params:")
    posts = request_json("GET", "/posts", params={"userId": 1})
    print("  posts for user 1:", len(posts) if posts is not None else "failed")

    print("POST with JSON body:")
    created = request_json("POST", "/posts", json_body={"title": "Hello", "body": "API", "userId": 1})
    print("  created:", created)

    print("PUT:")
    updated = request_json("PUT", "/posts/1", json_body={"id": 1, "title": "New", "body": "Text", "userId": 1})
    print("  updated:", updated)

    print("DELETE:")
    print("  deleted:", request_json("DELETE", "/posts/1"))

    print("Missing resource (404 handled gracefully):")
    print("  result:", request_json("GET", "/posts/99999"))