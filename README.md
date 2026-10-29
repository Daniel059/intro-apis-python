# Introduction to APIs in Python

My study notes and practice code from DataCamp's *Introduction to APIs in Python* course. Each lesson has a short write-up here and a runnable script in the repo. The notes are in my own words, and the code is rewritten to run against free public APIs so anyone can try it.

**Status:** course completed ✅

## Contents

- [Introduction to APIs in Python](#introduction-to-apis-in-python)
  - [Contents](#contents)
  - [What's in this repo](#whats-in-this-repo)
  - [Setup](#setup)
  - [Chapter 1: Making API requests](#chapter-1-making-api-requests)
    - [1. The big picture](#1-the-big-picture)
    - [2. URLs, query parameters and HTTP verbs](#2-urls-query-parameters-and-http-verbs)
    - [3. Headers and status codes](#3-headers-and-status-codes)
  - [Chapter 2: Going further](#chapter-2-going-further)
    - [4. Authentication](#4-authentication)
    - [5. Working with JSON](#5-working-with-json)
    - [6. Handling errors](#6-handling-errors)
  - [Wrap-up: a reusable API helper](#wrap-up-a-reusable-api-helper)
  - [Cheat sheet](#cheat-sheet)
  - [Mistakes to avoid](#mistakes-to-avoid)
  - [What I'd like to learn next](#what-id-like-to-learn-next)
  - [Credits](#credits)

## What's in this repo

```
intro-apis-python/
├── README.md
├── requirements.txt
├── .gitignore
├── chapter_01_making_api_requests/
│   ├── 01_urllib_vs_requests.py
│   ├── 02_anatomy_of_a_request.py
│   └── 03_headers_and_status_codes.py
├── chapter_02_more_api_request_concepts/
│   ├── 01_api_authentication.py
│   ├── 02_working_with_json.py
│   └── 03_error_handling.py
└── final_wrap_up/
    └── api_client.py
```

**A note on the APIs used:** the course relies on a music API that only runs inside DataCamp's platform. I swapped in [JSONPlaceholder](https://jsonplaceholder.typicode.com) (fake posts, safe to POST/PUT/DELETE) and [httpbin.org](https://httpbin.org) (built for testing auth and status codes). Both are public and need no signup.

## Setup

```bash
git clone https://github.com/Daniel059/intro-apis-python.git
cd intro-apis-python

python -m venv .venv
source .venv/bin/activate        # PowerShell: .venv\Scripts\activate
pip install -r requirements.txt

python chapter_01_making_api_requests/01_urllib_vs_requests.py
```

Every script is standalone, so run any of them directly.

---

## Chapter 1: Making API requests

### 1. The big picture

An **API** (Application Programming Interface) is an agreed set of rules that lets one program ask another for data or actions. A **web API** does this over HTTP: a *client* sends a request and a *server* sends back a response.

Three styles come up most often:

| Style | Where you'll see it |
|-------|---------------------|
| **SOAP** | Older enterprise systems with strict contracts |
| **REST** | The everyday default for web services (and the focus of this course) |
| **GraphQL** | Apps that want to ask for exactly the fields they need |

Python offers two ways to make requests. `urllib` is built in but takes several steps (open, read, decode). `requests` does the same job in one line, so that's what I use from here on.

```python
# urllib: open -> read bytes -> decode
import urllib.request
with urllib.request.urlopen(url) as resp:
    text = resp.read().decode("utf-8")

# requests: one call
import requests
text = requests.get(url).text
```

📄 Code: [`01_urllib_vs_requests.py`](chapter_01_making_api_requests/01_urllib_vs_requests.py)

### 2. URLs, query parameters and HTTP verbs

A URL has five parts. Using `https://jsonplaceholder.typicode.com:443/posts?userId=1`:

| Part | Example | What it tells us |
|------|---------|------------------|
| Protocol | `https` | How to talk to the server |
| Domain | `jsonplaceholder.typicode.com` | Which server |
| Port | `443` | Which door on that server (80 for HTTP and 443 for HTTPS are the defaults) |
| Path | `/posts` | Which resource |
| Query | `userId=1` | Extra filters or options |

**Query parameters:** rather than gluing strings together, hand `requests` a dictionary and it builds the query string for you.

```python
response = requests.get(f"{BASE_URL}/posts", params={"userId": 1})
print(response.url)   # .../posts?userId=1
```

**HTTP verbs:** these say *what to do* with the resource. If you think of an API as a database, they map neatly onto CRUD:

| Verb | Database-style thinking | `requests` call |
|------|-------------------------|-----------------|
| GET | Read a record | `requests.get(url)` |
| POST | Insert a new record | `requests.post(url, data=...)` |
| PUT | Overwrite an existing record | `requests.put(url, data=...)` |
| DELETE | Remove a record | `requests.delete(url)` |

There are nine verbs in total, but these four cover most REST work.

📄 Code: [`02_anatomy_of_a_request.py`](chapter_01_making_api_requests/02_anatomy_of_a_request.py)

### 3. Headers and status codes

Requests and responses are both made of three parts: a **start line**, **headers**, and an optional **body**.

```
GET /posts/1 HTTP/1.1            <- request line
Accept: application/json        <- header

HTTP/1.1 200 OK                  <- status line
Content-Type: application/json   <- header
{"id": 1, ...}                   <- body
```

**Headers** are `key: value` pairs that carry metadata. The nice trick is *content negotiation*: the client says what it can read (`Accept`), and the server states what it actually sent (`Content-Type`).

```python
response = requests.get(url, headers={"Accept": "application/json"})
print(response.headers["Content-Type"])
print(response.headers.get("X-Missing"))   # None instead of an error
```

**Status codes** tell us how the server handled the request:

| Range | Meaning |
|-------|---------|
| 1xx | Informational |
| 2xx | Success (`200 OK`) |
| 3xx | Redirection |
| 4xx | Client error (`404 Not Found`) |
| 5xx | Server error (`500 Internal Server Error`) |

```python
if response.status_code == requests.codes.ok:      # 200, no need to memorise it
    ...
print(requests.codes.not_found)                    # 404
```

📄 Code: [`03_headers_and_status_codes.py`](chapter_01_making_api_requests/03_headers_and_status_codes.py)

---

## Chapter 2: Going further

### 4. Authentication

Protected APIs answer anonymous requests with **401 Unauthorized**. Send valid credentials and you get a normal **200**. Four common approaches:

| Method | In short |
|--------|----------|
| Basic | Username and password. Simple, but weak on its own |
| API key / token | A secret string sent with each request |
| JWT | A token that expires and can carry extra info |
| OAuth 2.0 | Delegated access without handing over your password |

The API's documentation says which one to use. I practised the first two.

**Basic auth:** pass a tuple and `requests` builds the header.

```python
requests.get(url, auth=("user", "passwd"))
```

The header is just `username:password` run through base64, which is *encoding*, not encryption. Anyone who intercepts it can read it, which is why Basic auth should only ever go over HTTPS. The script shows how to build and decode the header by hand.

**API key / token:** two options, and the header is usually preferred.

```python
# 1. query parameter
requests.get(url, params={"access_token": api_key})

# 2. Authorization header
requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
```

> 🔐 Keep secrets out of Git. Read them with `os.environ.get("API_KEY")`; `.env` files are already in `.gitignore`.

📄 Code: [`01_api_authentication.py`](chapter_02_more_api_request_concepts/01_api_authentication.py)

### 5. Working with JSON

Real data has structure (an album has a title, an artist and a list of tracks), so APIs usually exchange **JSON**. Other formats you may run into are XML, CSV and YAML.

Python's built-in `json` module converts both ways:

```python
import json
text = json.dumps({"title": "Demo", "tracks": [1, 2]})   # dict -> JSON string
data = json.loads(text)                                   # JSON string -> dict
```

With `requests` you rarely need to do that by hand:

```python
# Receiving
data = requests.get(url, headers={"Accept": "application/json"}).json()

# Sending: json= encodes the body AND sets Content-Type: application/json
requests.post(url, json={"name": "Road trip", "public": True})
```

`data=` and `json=` are not interchangeable. `data=` sends form-style `key=value&...` text, while `json=` sends real JSON.

📄 Code: [`02_working_with_json.py`](chapter_02_more_api_request_concepts/02_working_with_json.py)

### 6. Handling errors

Calls over a network fail in three different ways, and each needs a different response:

| Failure | What happens | Typical cause |
|---------|--------------|---------------|
| No response at all | `ConnectionError` is raised | No internet, wrong host, server down |
| 4xx response | Our request was wrong | Bad URL, missing auth, too many requests (429) |
| 5xx response | The server struggled | Overload, misconfiguration (500, 502, 504) |

Checking `status_code` by hand covers the last two. `raise_for_status()` turns them into an `HTTPError`, so one `try/except` handles everything:

```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.ConnectionError:
    print("Couldn't reach the server")
except requests.exceptions.HTTPError as err:
    print("Server said:", err.response.status_code)
```

`timeout=10` is my own addition. Without it, a request to an unresponsive server can wait forever.

📄 Code: [`03_error_handling.py`](chapter_02_more_api_request_concepts/03_error_handling.py)

---

## Wrap-up: a reusable API helper

To tie everything together, [`final_wrap_up/api_client.py`](final_wrap_up/api_client.py) wraps the lessons into a single function, `request_json()`. It:

- accepts any HTTP verb, query parameters and a JSON body
- adds an `Accept` header, plus a Bearer token if `API_TOKEN` is set
- uses a timeout, then handles connection errors, timeouts and HTTP errors
- returns decoded JSON, or `None` if something went wrong

```python
posts = request_json("GET", "/posts", params={"userId": 1})
created = request_json("POST", "/posts", json_body={"title": "Hello", "userId": 1})
missing = request_json("GET", "/posts/99999")   # prints "HTTP 404", returns None
```

## Cheat sheet

```python
requests.get(url, params={...}, headers={...}, auth=(user, pw), timeout=10)
requests.post(url, json={...})      # create (JSON body)
requests.put(url, json={...})       # update
requests.delete(url)                # remove

r.status_code        # 200, 404, ...
r.headers            # response headers
r.text               # raw body as text
r.json()             # body decoded to Python
r.url                # final URL, including query string
r.request.headers    # the headers we actually sent
r.raise_for_status() # raise HTTPError on 4xx/5xx
```

## Mistakes to avoid

- Committing API keys or passwords to GitHub
- Forgetting `timeout` and letting a script hang
- Using `data=` when the API expects JSON (use `json=`)
- Assuming a response is fine without checking the status code
- Only handling HTTP errors and forgetting connection errors

## What I'd like to learn next

- Pagination, for APIs that return results in pages
- Rate limiting and retrying politely after a 429
- OAuth 2.0 and JWT authentication
- Pulling API data into a pipeline (extract, transform, load)

## Credits

Course: [Introduction to APIs in Python](https://www.datacamp.com/courses/introduction-to-apis-in-python) on DataCamp, taught by Chris Ramakers. Notes and code in this repo are my own write-up and practice.