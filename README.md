# Introduction to APIs in Python

My learning journey through DataCamp's **Introduction to APIs in Python** course, with notes, code snippets and runnable scripts for every chapter.

> **Status:** Chapter 1 in progress

## Table of Contents

- [Introduction to APIs in Python](#introduction-to-apis-in-python)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
  - [Course Introduction](#course-introduction)
    - [What is an API?](#what-is-an-api)
    - [Web APIs, clients and servers](#web-apis-clients-and-servers)
    - [Types of Web APIs](#types-of-web-apis)
    - [urllib vs requests](#urllib-vs-requests)
  - [Chapter 1: Making API Requests with Python](#chapter-1-making-api-requests-with-python)
  - [Chapter 2: More API Request Concepts](#chapter-2-more-api-request-concepts)
  - [Acknowledgements](#acknowledgements)

## Project Structure

```
intro-apis-python/
├── README.md
├── requirements.txt
├── .gitignore
└── chapter_01_making_api_requests/
    └── 01_urllib_vs_requests.py
```

## Getting Started

```bash
git clone https://github.com/Daniel059/intro-apis-python.git
cd intro-apis-python
python -m venv .venv
source .venv/bin/activate      # Windows PowerShell: .venv\Scripts\activate
pip install -r requirements.txt
python chapter_01_making_api_requests/01_urllib_vs_requests.py
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
```# Introduction to APIs in Python

My learning journey through DataCamp's **Introduction to APIs in Python** course, with notes, code snippets and runnable scripts for every chapter.

> **Status:** Chapter 1 in progress (lessons 1-2 done)

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
└── chapter_01_making_api_requests/
    ├── 01_urllib_vs_requests.py
    └── 02_anatomy_of_a_request.py
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

*Coming next:* creating and deleting resources, headers and status codes.

## Chapter 2: More API Request Concepts

*Coming later:* authentication (Basic, API key), JSON handling, error handling, rate limits.

## Acknowledgements
Course: [Introduction to APIs in Python](https://campus.datacamp.com/courses/introduction-to-apis-in-python/making-api-requests-with-python) by Chris Ramakers on DataCamp.

Full code: [`01_urllib_vs_requests.py`](chapter_01_making_api_requests/01_urllib_vs_requests.py)

> The course uses a hosted music catalog API that only works inside DataCamp, so the scripts here use [JSONPlaceholder](https://jsonplaceholder.typicode.com) as a public stand-in.

## Chapter 1: Making API Requests with Python

*Coming next:* using `requests`, anatomy of a request, HTTP verbs, URL parameters, creating/deleting resources, headers and status codes.

## Chapter 2: More API Request Concepts

*Coming later:* authentication (Basic, API key), JSON handling, error handling, rate limits.

## Acknowledgements
Course: [Introduction to APIs in Python](https://campus.datacamp.com/courses/introduction-to-apis-in-python/making-api-requests-with-python) by Chris Ramakers on DataCamp.