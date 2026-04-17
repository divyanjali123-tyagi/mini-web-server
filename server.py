import socket
import os
import threading

HOST = "127.0.0.1"
PORT = 8080

# MIME types — tells browser what kind of file is being sent
MIME_TYPES = {
    ".html": "text/html",
    ".css":  "text/css",
    ".js":   "application/javascript",
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".ico":  "image/x-icon",
    ".txt":  "text/plain",
}

def read_file(filename):
    try:
        with open(filename, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None

def get_mime_type(filename):
    # Get file extension e.g. ".html" from "index.html"
    ext = os.path.splitext(filename)[1]
    return MIME_TYPES.get(ext, "application/octet-stream")

def log_request(address, method, path, status):
    # Print to terminal AND save to a log file
    log_line = f"{address[0]} | {method} {path} | {status}"
    print(f"📥 {log_line}")
    with open("requests.log", "a") as f:
        f.write(log_line + "\n")

def handle_request(request_data, client_address):
    try:
        first_line = request_data.split("\n")[0]
        method = first_line.split(" ")[0]
        path   = first_line.split(" ")[1]
    except IndexError:
        return b"HTTP/1.1 400 Bad Request\r\n\r\n"

    if path == "/":
        path = "/index.html"

    filename = path[1:]  # remove leading "/"
    content  = read_file(filename)

    if content:
        mime_type = get_mime_type(filename)
        status    = "200 OK"
        response  = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: {mime_type}\r\n"
            f"Content-Length: {len(content)}\r\n"
            "\r\n"
        ).encode() + content
    else:
        status       = "404 Not Found"
        error_page   = read_file("404.html")
        body         = error_page if error_page else b"<h1>404 - Page Not Found</h1>"
        response     = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
        ).encode() + body

    log_request(client_address, method, path, status)
    return response

def handle_client(client_socket, client_address):
    """Each user gets their own thread — handles multiple users at once"""
    try:
        request_data = client_socket.recv(1024).decode(errors="ignore")
        if request_data:
            response = handle_request(request_data, client_address)
            client_socket.sendall(response)
    finally:
        client_socket.close()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"✅ Server running at http://{HOST}:{PORT}")
    print("Open your browser and go to http://127.0.0.1:8080")
    print("Logs are saved to requests.log")
    print("Press Ctrl+C to stop.\n")

    while True:
        client_socket, client_address = server_socket.accept()
        # 🔧 Each connection runs in its own thread
        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )
        thread.daemon = True
        thread.start()

run_server()