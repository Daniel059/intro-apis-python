"""
Chapter 1 - Lesson 3: Headers and status codes.

Covers:
  - request/response message anatomy (start-line, headers, body)
  - sending request headers (content negotiation with `Accept`)
  - reading response headers (`Content-Type`)
  - reading status codes and using the `requests.codes` lookup object
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# The five status-code categories
STATUS_CATEGORIES = {
    1: "Informational",
    2: "Success",
    3: "Redirection",
    4: "Client error",
    5: "Server error",
}


# --------------------------------------------------------------------------
# 1. Request headers (content negotiation)
# --------------------------------------------------------------------------
def get_json_with_accept_header(url: str) -> requests.Response:
    """Tell the server we can accept a JSON response via the Accept header."""
    headers = {"Accept": "application/json"}
    return requests.get(url, headers=headers)


# --------------------------------------------------------------------------
# 2. Response headers
# --------------------------------------------------------------------------
def describe_response_headers(response: requests.Response) -> None:
    """Show the headers the server sent back."""
    print("Content-Type (square brackets):", response.headers["Content-Type"])
    # .get() is safer: returns None instead of raising KeyError if missing
    print("Content-Type (.get)           :", response.headers.get("Content-Type"))
    print("Missing header (.get)         :", response.headers.get("X-Not-There"))
    print("Total headers received        :", len(response.headers))


# --------------------------------------------------------------------------
# 3. Status codes
# --------------------------------------------------------------------------
def categorise_status(code: int) -> str:
    """Return the category name for a status code (e.g. 404 -> Client error)."""
    return STATUS_CATEGORIES.get(code // 100, "Unknown")


def check_status(response: requests.Response) -> None:
    """Compare a response's status code using the requests.codes lookup."""
    code = response.status_code
    print(f"Status: {code} ({categorise_status(code)})")

    if code == requests.codes.ok:  # 200
        print("OK: the server processed the request correctly")
    elif code == requests.codes.not_found:  # 404
        print("Not Found: that resource does not exist")
    elif code == requests.codes.internal_server_error:  # 500
        print("Server error: something went wrong on the server")


if __name__ == "__main__":
    print("--- Request headers + response headers ---")
    resp = get_json_with_accept_header(f"{BASE_URL}/posts/1")
    print("Request headers sent:", resp.request.headers.get("Accept"))
    describe_response_headers(resp)

    print("\n--- Status code: existing resource ---")
    check_status(resp)

    print("\n--- Status code: missing resource ---")
    missing = requests.get(f"{BASE_URL}/posts/99999")
    check_status(missing)

    print("\n--- requests.codes lookup ---")
    print("requests.codes.not_found             =", requests.codes.not_found)
    print("requests.codes.ok                    =", requests.codes.ok)
    print("requests.codes.internal_server_error =", requests.codes.internal_server_error)