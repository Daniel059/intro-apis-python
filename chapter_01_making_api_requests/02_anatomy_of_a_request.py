"""
Chapter 1 - Lesson 2: The basic anatomy of an API request.

Covers:
  - the 5 components of a URL (protocol, domain, port, path, query)
  - query parameters via the `params` argument
  - the 4 key HTTP verbs: GET, POST, PUT, DELETE
  - sending data with the `data` argument

Uses JSONPlaceholder (a free fake REST API). It accepts POST/PUT/DELETE but
does not really save anything, which makes it safe for practice.
"""

from urllib.parse import urlparse

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# --------------------------------------------------------------------------
# 1. Dissecting a URL
# --------------------------------------------------------------------------
def dissect_url(url: str) -> dict:
    """Split a URL into its main components."""
    parsed = urlparse(url)
    return {
        "protocol": parsed.scheme,
        "domain": parsed.hostname,
        # if no port is written, HTTP defaults to 80 and HTTPS to 443
        "port": parsed.port or (443 if parsed.scheme == "https" else 80),
        "path": parsed.path,
        "query": parsed.query,
    }


# --------------------------------------------------------------------------
# 2. Query parameters
# --------------------------------------------------------------------------
def get_posts_by_user_manual(user_id: int) -> requests.Response:
    """Works, but we build the query string by hand."""
    return requests.get(f"{BASE_URL}/posts?userId={user_id}")


def get_posts_by_user(user_id: int) -> requests.Response:
    """Better: let requests build the query string from a dictionary."""
    params = {"userId": user_id}
    return requests.get(f"{BASE_URL}/posts", params=params)


# --------------------------------------------------------------------------
# 3. HTTP verbs
# --------------------------------------------------------------------------
def read_post(post_id: int) -> requests.Response:
    """GET: read a resource."""
    return requests.get(f"{BASE_URL}/posts/{post_id}")


def create_post(title: str, body: str, user_id: int) -> requests.Response:
    """POST: create a resource."""
    new_post = {"title": title, "body": body, "userId": user_id}
    return requests.post(f"{BASE_URL}/posts", data=new_post)


def update_post(post_id: int, title: str, body: str, user_id: int) -> requests.Response:
    """PUT: update (replace) a resource."""
    updated_post = {"id": post_id, "title": title, "body": body, "userId": user_id}
    return requests.put(f"{BASE_URL}/posts/{post_id}", data=updated_post)


def delete_post(post_id: int) -> requests.Response:
    """DELETE: remove a resource."""
    return requests.delete(f"{BASE_URL}/posts/{post_id}")


if __name__ == "__main__":
    print("--- URL components ---")
    example = "https://jsonplaceholder.typicode.com:443/posts?userId=1"
    for part, value in dissect_url(example).items():
        print(f"{part:>8}: {value}")

    print("\n--- Query parameters ---")
    resp = get_posts_by_user(1)
    print("Final URL:", resp.url)  # requests built ?userId=1 for us
    print("Posts returned:", len(resp.json()))

    print("\n--- GET ---")
    print(read_post(1).status_code)

    print("\n--- POST ---")
    resp = create_post("My first post", "Learning APIs", user_id=1)
    print(resp.status_code, resp.json())

    print("\n--- PUT ---")
    resp = update_post(1, "Updated title", "Updated body", user_id=1)
    print(resp.status_code, resp.json())

    print("\n--- DELETE ---")
    resp = delete_post(1)
    print(resp.status_code, resp.text)