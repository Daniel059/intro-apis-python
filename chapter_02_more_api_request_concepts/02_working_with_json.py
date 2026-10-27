"""
Chapter 2 - Lesson 2: Working with structured data (JSON)

Covers:
  - encoding / decoding JSON with the built-in `json` package
  - requesting JSON with the Accept header and `response.json()`
  - sending JSON with the `json=` argument (vs `data=`)

Uses JSONPlaceholder, a free fake REST API that returns JSON and echoes back
whatever JSON we POST (without saving it).
"""

import json
import os

import requests

BASE_URL = os.environ.get("JSON_DEMO_BASE_URL", "https://jsonplaceholder.typicode.com")


# --------------------------------------------------------------------------
# 1. Python <-> JSON with the json package
# --------------------------------------------------------------------------
def encode_to_json(obj) -> str:
    """Encoding: Python object -> JSON string (json.dumps)."""
    return json.dumps(obj)


def decode_from_json(json_text: str):
    """Decoding: JSON string -> Python object (json.loads)."""
    return json.loads(json_text)


# --------------------------------------------------------------------------
# 2. Requesting JSON data
# --------------------------------------------------------------------------
def get_post_as_json(post_id: int):
    """
    Ask for JSON with the Accept header, then decode it with response.json().
    Without the header, a server may answer in another format (e.g. plain text).
    """
    headers = {"Accept": "application/json"}
    response = requests.get(f"{BASE_URL}/posts/{post_id}", headers=headers)
    print("Raw JSON text :", response.text[:80].replace("\n", " "), "...")
    return response.json()  # -> Python dict


# --------------------------------------------------------------------------
# 3. Sending JSON data
# --------------------------------------------------------------------------
def create_playlist_like_resource(playlist: dict) -> requests.Response:
    """
    `json=` encodes the dict to a JSON string AND sets
    Content-Type: application/json automatically.
    """
    return requests.post(f"{BASE_URL}/posts", json=playlist)


def create_with_data_argument(playlist: dict) -> requests.Response:
    """For contrast: `data=` sends form-encoded data, not JSON."""
    return requests.post(f"{BASE_URL}/posts", data=playlist)


if __name__ == "__main__":
    album = {
        "id": 1,
        "title": "Greatest Hits",
        "artist": "The Examples",
        "tracks": ["Intro", "Song A", "Song B"],
    }

    print("--- Encode / decode ---")
    as_text = encode_to_json(album)
    print("JSON string :", as_text)
    print("Type        :", type(as_text).__name__)
    back = decode_from_json(as_text)
    print("Back to dict:", back == album, type(back).__name__)

    print("\n--- Request JSON ---")
    post = get_post_as_json(1)
    print("Decoded type  :", type(post).__name__)
    print("Title         :", post["title"])

    print("\n--- Send JSON with json= ---")
    playlist = {"name": "Road trip", "tracks": ["Song A", "Song B"], "public": True}
    resp = create_playlist_like_resource(playlist)
    print("Status        :", resp.status_code)
    print("Content-Type  :", resp.request.headers["Content-Type"])  # application/json
    print("Request body  :", resp.request.body)
    print("Server echoed :", resp.json())

    print("\n--- For contrast: data= ---")
    resp = create_with_data_argument({"name": "Road trip", "public": "true"})
    print("Content-Type  :", resp.request.headers["Content-Type"])
    print("Request body  :", resp.request.body)