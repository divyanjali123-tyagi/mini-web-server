# 🌐 Mini Web Server (Built from Scratch)

A simple HTTP web server built from scratch using only Python's
built-in `socket` library — no Flask, no Django, no frameworks.

## What it does
- Listens for HTTP requests on port 8080
- Parses raw GET requests manually
- Serves HTML files from disk
- Returns 404 for missing files

## What I learned
- How HTTP requests and responses are structured
- How TCP sockets work (bind, listen, accept, send)
- How a browser and server actually communicate
- The difference between a port and an IP address

## How to run
python server.py
Then open http://127.0.0.1:8080 in your browser.

## Tech used
- Python 3
- Built-in socket module only (zero external libraries)
