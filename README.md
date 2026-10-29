# Introduction to APIs in Python

My learning journey through DataCamp's **Introduction to APIs in Python** course, with notes, code snippets and runnable scripts for every chapter.

> **Status:** Chapter 1 lessons 1-3 done; Chapter 2 in progress (lessons 1-3 done)

## Table of Contents

1. [Project Structure](#project-structure)
2. [Getting Started](#getting-started)
3. [Course Introduction](#course-introduction)
4. [Chapter 1: Making API Requests with Python](#chapter-1-making-api-requests-with-python)
5. [Chapter 2: More API Request Concepts](#chapter-2-more-api-request-concepts)

## Project Structure

```
intro-apis-python/
├── README.md
├── requirements.txt
├── .gitignore
├── chapter_01_making_api_requests/
│   ├── 01_urllib_vs_requests.py
│   ├── 02_anatomy_of_a_request.py
│   └── 03_headers_and_status_codes.py
└── chapter_02_more_api_request_concepts/
    ├── 01_api_authentication.py
    ├── 02_working_with_json.py
    └── 03_error_handling.py
```

## Getting Started

```bash
git clone https://github.com/Daniel059/intro-apis-python.git
cd intro-apis-python
python -m venv .venv
source .venv/bin/activate      # Windows PowerShell: .venv\Scripts\activate
pip install -r requirements.txt
python chapter_01_making_api_requests/01_urllib_vs_requests.py
python chapter_01_making_api_requests/02_anatomy_of_a_request.py
python chapter_01_making_api_requests/03_headers_and_status_codes.py
python chapter_02_more_api_request_concepts/01_api_authentication.py
python chapter_02_more_api_request_concepts/02_working_with_json.py
python chapter_02_more_api_request_concepts/03_error_handling.py
```

## Course Introduction

### What is an API?
**API** = *Application Programming Interface*: a set of rules that lets two systems communicate to exchange or manipulate data. We rarely touch APIs directly (we use UIs), but they are everywhere. Example: clicking "Send" in an email app makes it call an API on the email server.

### Web APIs, clients and servers
Web APIs let two applications communicate over a network using **HTTP**, the same protocol browsers use. A **client** sends a request; the **server** sends back a response.

```
Client  ── HTTP request ──▶  Server
Client  ◀─ HTTP response ──  Server
```

### Types of Web APIs

| Type | Characteristics | Typical use |
|------|-----------------|-------------|
| **SOAP** | Formal, strict protocols, robust | Enterprise applications |
| **REST** | Simple, scalable, easy to integrate (most popular) | General web services |
| **GraphQL** | Precise, flexible queries; minimal data transfer | Performance-sensitive apps |

This course focuses on **REST**.

### urllib vs requests

- `urllib` ships with Python and is powerful, but needs more steps.
- `requests` is a third-party package that does the same with far less code.

```python
# urllib: send, read, decode
import urllib.request

with urllib.request.urlopen(url) as response:
    data = response.read().decode("utf-8")
print(data)
```

```python
# requests: one call, text is already decoded
import requests

response = requests.get(url)
print(response.text)
```

Full code: [`01_urllib_vs_requests.py`](chapter_01_making_api_requests/01_urllib_vs_requests.py)

> The course uses a hosted music catalog API that only works inside DataCamp, so the scripts here use [JSONPlaceholder](https://jsonplaceholder.typicode.com) as a public stand-in.

## Chapter 1: Making API Requests with Python

### Lesson 2: The basic anatomy of an API request

#### What is a URL?
A URL is a structured address pointing to a specific resource. Analogy: a REST API is an office building, each resource is an office unit, and the URL is the address of one unit.

#### The 5 components of a URL

```
https://jsonplaceholder.typicode.com:443/posts?userId=1
\___/   \__________________________/ \_/ \____/ \______/
protocol          domain             port  path    query
```

| Component | Analogy | Role |
|-----------|---------|------|
| **Protocol** | Walking or driving | How we travel to the destination (`http`, `https`) |
| **Domain** | Street address of the building | Identifies the API server on the internet |
| **Port** | The building entrance | Default ports: `80` (HTTP) and `443` (HTTPS) |
| **Path** | The specific office unit | Location of the resource on the server |
| **Query** | "Take the elevator" | Extra instructions for the request |

```python
from urllib.parse import urlparse

parsed = urlparse("https://jsonplaceholder.typicode.com:443/posts?userId=1")
print(parsed.scheme, parsed.hostname, parsed.port, parsed.path, parsed.query)
```

#### Query parameters with `requests`
You can append them to the URL string, but the better way is the `params` argument, which takes a dictionary (one key/value pair per parameter).

```python
# Manual (works, but clumsy)
requests.get("https://jsonplaceholder.typicode.com/posts?userId=1")

# Better: pass a dictionary
params = {"userId": 1}
response = requests.get("https://jsonplaceholder.typicode.com/posts", params=params)
print(response.url)  # .../posts?userId=1
```

#### HTTP verbs
There are 9 HTTP verbs, but for simple REST APIs these 4 matter most:

| Verb | Action | Mailbox analogy | `requests` function |
|------|--------|-----------------|---------------------|
| **GET** | Read a resource | Look in the mailbox without taking anything | `requests.get()` |
| **POST** | Create a resource | Drop a new package in the mailbox | `requests.post()` |
| **PUT** | Update a resource | Replace a package already in the mailbox | `requests.put()` |
| **DELETE** | Remove a resource | Empty the mailbox | `requests.delete()` |

#### Sending data with POST and PUT
Just like `params` sets query parameters, the `data` argument carries the data to create or update a resource. DELETE needs no data.

```python
new_post = {"title": "My first post", "body": "Learning APIs", "userId": 1}

requests.post(f"{BASE_URL}/posts", data=new_post)        # create
requests.put(f"{BASE_URL}/posts/1", data=new_post)       # update
requests.delete(f"{BASE_URL}/posts/1")                   # delete
```

Full code: [`02_anatomy_of_a_request.py`](chapter_01_making_api_requests/02_anatomy_of_a_request.py)

> JSONPlaceholder accepts POST, PUT and DELETE but doesn't actually store changes, so it's safe to practise on.

### Lesson 3: Headers and status codes

#### Request and response message anatomy
Request and response messages share the same structure of three parts:

1. **Start-line**: the *request-line* in a request (request type such as `GET` or `POST`, plus the path) or the *status-line* in a response (a three-digit status code and a status message)
2. **Headers**: key-value pairs describing the message or data
3. **Body**: the data being sent or received

```
GET /posts/1 HTTP/1.1            <- request-line
Accept: application/json         <- header
                                 <- (no body for GET)

HTTP/1.1 200 OK                  <- status-line
Content-Type: application/json   <- header
{ "id": 1, ... }                 <- body
```

#### Status codes
There are over 70 status codes, grouped into five categories:

| Range | Category |
|-------|----------|
| 1xx | Informational |
| 2xx | Success |
| 3xx | Redirection |
| 4xx | Client error |
| 5xx | Server error |

The three most important to remember:

| Code | Meaning |
|------|---------|
| `200 OK` | The server processed the request correctly |
| `404 Not Found` | The requested resource doesn't exist |
| `500 Internal Server Error` | An error occurred on the server |

Full list: [MDN status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

#### Headers
Headers are key-value pairs separated by a colon (`key: value`). The key is case-insensitive. They describe things like the type of content being sent or when a resource was last modified.

**Content negotiation:** client and server agree on a format using headers. The client sends `Accept` to say what it can handle, and the server replies with `Content-Type` to say what it actually sent.

#### Headers with `requests`

```python
# Send request headers with the headers parameter (a dictionary)
headers = {"Accept": "application/json"}
response = requests.get(url, headers=headers)

# Read response headers: response.headers is a dictionary-like object
print(response.headers["Content-Type"])      # square brackets
print(response.headers.get("Content-Type"))  # .get() returns None if missing
```

#### Status codes with `requests`

```python
response = requests.get(url)
print(response.status_code)  # e.g. 200

# requests.codes is a lookup object so you don't need to memorise numbers
if response.status_code == requests.codes.ok:
    print("Success")

print(requests.codes.not_found)  # 404
```

Full code: [`03_headers_and_status_codes.py`](chapter_01_making_api_requests/03_headers_and_status_codes.py)

*Coming next:* exercises on response codes, request/response headers and handling content-type errors.

## Chapter 2: More API Request Concepts

### Lesson 1: API Authentication

#### Why authenticate?
APIs often hold private or sensitive data, so they require clients to prove who they are. Without credentials, a protected API answers with **`401 Unauthorized`**. Once the request identifies us, the server responds normally with **`200 OK`**.

#### Authentication methods

| Method | How it works | Notes |
|--------|--------------|-------|
| **Basic** | Username and password | Simplest, but least secure: credentials are only base64-encoded, not encrypted |
| **API key / token** | A unique key or token attached to every request | Simple, but a risk if the key is compromised |
| **JWT** (JSON Web Token) | Like an API key, but with a limited lifespan and can carry extra encoded data, such as user info | Expires automatically |
| **OAuth 2.0** | Framework for fine-grained access without sharing credentials | Most comprehensive |

Which method to use depends on the API server, so check the API's documentation. This lesson covers Basic and API key authentication with `requests`.

#### Basic authentication
Basic auth sends an `Authorization` header with a base64-encoded `username:password`. Base64 is a two-way encoding that anyone can decode, so it adds **no security** on its own. With `requests` you don't build the header yourself: pass a tuple to the `auth` argument.

```python
response = requests.get(url, auth=("username", "password"))
print(response.status_code)  # 200 if the credentials are valid, 401 if not
```

What `requests` does behind the scenes:

```python
import base64

credentials = base64.b64encode(b"username:password").decode("utf-8")
headers = {"Authorization": f"Basic {credentials}"}
```

#### API key / token authentication
There are two common ways to send the token:

```python
# Option 1: as a query parameter
response = requests.get(url, params={"access_token": api_key})

# Option 2 (usually preferred): in an Authorization header
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(url, headers=headers)
```

`requests` has no built-in helper for the header option, so we add it ourselves with `headers`. The exact header format (`Bearer ...`, `Token ...`) comes from the API's documentation.

> **Security tip:** never hardcode real passwords or keys in your code or commit them to GitHub. Read them from environment variables (`os.environ.get("API_KEY")`) instead. The `.gitignore` in this repo already excludes `.env` files.

Full code: [`01_api_authentication.py`](chapter_02_more_api_request_concepts/01_api_authentication.py)

> The course's album API only works inside DataCamp, so the script uses [httpbin.org](https://httpbin.org), a public testing service, as a stand-in.

### Lesson 2: Working with structured data (JSON)

#### Why structured data?
Simple APIs can return plain, unstructured text (like song lyrics). Complex things like music albums have several properties (ID, title, artist, list of tracks), so they need a structured format.

#### JSON
**JSON** (JavaScript Object Notation) is the most common web API format: lightweight, natively supported by many languages, and readable by both humans and machines. It is one kind of **content type** (also called mime-type or media-type). Others you may meet: XML, CSV and YAML.

#### From Python to JSON and back
- **Encoding**: Python object -> JSON string, so it can be transmitted safely
- **Decoding**: JSON string -> Python object

```python
import json

album = {"id": 1, "title": "Greatest Hits", "tracks": ["Intro", "Song A"]}

json_text = json.dumps(album)       # encode: dict -> str
python_obj = json.loads(json_text)  # decode: str -> dict
```

| Function | Direction |
|----------|-----------|
| `json.dumps()` | Python object -> JSON string |
| `json.loads()` | JSON string -> Python object |

#### Requesting JSON data
Without extra headers a server may reply in plain text. Adding an `Accept: application/json` header asks for JSON. `response.text` holds the raw JSON text, and `response.json()` decodes it into a Python object.

```python
headers = {"Accept": "application/json"}
response = requests.get(url, headers=headers)

print(response.text)      # raw JSON string
data = response.json()    # decoded into a Python dict
print(data["title"])
```

#### Sending JSON data
Pass the object with the `json=` argument. `requests` encodes it to JSON **and** adds the `Content-Type: application/json` header automatically.

```python
playlist = {"name": "Road trip", "tracks": ["Song A", "Song B"], "public": True}

response = requests.post(url, json=playlist)
print(response.request.headers["Content-Type"])  # application/json
print(response.request.body)                     # the encoded JSON
```

`data=` vs `json=`: `data=` sends form-encoded data (`name=Road+trip&...`) with a different content type, so use `json=` when the API expects JSON.

Full code: [`02_working_with_json.py`](chapter_02_more_api_request_concepts/02_working_with_json.py)

### Lesson 3: Error handling

Things can go wrong when talking to a web API over the internet, so our code should handle failures gracefully.

#### Error status codes
A `4XX` or `5XX` status code in the response signals a problem.

| Range | Meaning | Cause | Who fixes it |
|-------|---------|-------|--------------|
| **4XX** | Client error: the request could not be handled | Wrong header, failed authentication, bad URL | The client, by fixing the request |
| **5XX** | Server error: the server acknowledged the request but struggled | Server overload, configuration errors | Not the client, but our code should handle it to avoid bugs |

Common examples:

| Code | Meaning | What to do |
|------|---------|------------|
| `401` | Protected resource, we need to authenticate | Add authentication to the request |
| `404` | Resource doesn't exist on the server | Fix the URL or resource |
| `429` | Too many requests | Add a rate limiter to spread requests over a longer period |
| `500` | Internal Server Error (catch-all) | Handle gracefully |
| `502`, `504` | Server infrastructure problems | Handle gracefully |

#### Handling errors
**Simple approach:** check the status code.

```python
response = requests.get(url)
if response.status_code >= 400:
    print("Something went wrong:", response.status_code)
```

This is oversimplified. A request can fail *before* reaching the server, in which case there is no response and no status code. `requests` raises a `ConnectionError` instead, which we catch with `try/except`. A proper solution combines both checks.

#### `raise_for_status()`
Call it right after sending the request. Any 4XX or 5XX response then raises an `HTTPError`.

```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.ConnectionError:
    print("Could not reach the server")
except requests.exceptions.HTTPError as err:
    print("HTTP error:", err.response.status_code)
```

> `timeout=10` isn't in the lesson, but it is good practice: without it, a request can wait indefinitely for a server that never answers.

Full code: [`03_error_handling.py`](chapter_02_more_api_request_concepts/03_error_handling.py)

*Coming later:* respecting API rate limits.

## Acknowledgements
Course: [Introduction to APIs in Python](https://campus.datacamp.com/courses/introduction-to-apis-in-python/making-api-requests-with-python) by Chris Ramakers on DataCamp.