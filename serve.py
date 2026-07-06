#!/usr/bin/env python3
"""Serve the blog locally for testing."""
import http.server
import socketserver

PORT = 8000
DIRECTORY = "docs"


def main() -> None:
    handler = lambda *args: http.server.SimpleHTTPRequestHandler(
        *args, directory=DIRECTORY
    )
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
