import logging
from random import choice

import requests
from flask import Flask, jsonify, request

from plugins import load_tunnels

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize tunnels from configuration
tunnels = load_tunnels()


@app.route("/proxy", methods=["POST"])
def proxy_request():
    """
    Endpoint that accepts request details and makes a request to the provided URL
    with the specified headers and user agent, then returns the HTML response.

    Expected JSON payload:
    {
        "url": "https://example.com",
        "headers": {
            "Accept-Language": "en-US,en;q=0.9",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            ...
        },
        "strategy": "sequential", or "random"
    }
    """
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Check if required fields are present
        if not data or "url" not in data:
            return jsonify({"error": "URL is required"}), 400

        # Extract request parameters
        url = data["url"]
        headers = data.get("headers", {})
        strategy = data.get("strategy", "sequential")

        logger.info(f"Proxying request to: {url}")

        html = None
        available_tunnels = tunnels.copy()
        if strategy == "sequential":
            i = 0
            while html is None and i < len(available_tunnels):
                tunnel = available_tunnels[i]
                print(f"Using tunnel: {tunnel}")
                response = tunnel.make_request(url, headers)
                if response["status_code"] == 200:
                    html = response["html"]
                i += 1

        elif strategy == "random":
            tunnel = choice(available_tunnels)
            available_tunnels.remove(tunnel)
            print(f"Tunnel: {tunnel}")

            response = tunnel.make_request(url, headers)
            html = response["html"] if response["status_code"] == 200 else None
        else:
            return jsonify({"error": "Invalid strategy"}), 400

        if html is None:
            return jsonify({"error": "All tunnels failed"}), 503

        return jsonify(html)

    except requests.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route("/")
def index():
    """Simple index page with usage instructions"""
    return """
    <html>
        <head>
            <title>Trottola</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                pre {
                    background-color: #f4f4f4;
                    padding: 10px;
                    border-radius: 4px;
                    overflow-x: auto;
                }
                code {
                    background-color: #f4f4f4;
                    padding: 2px 4px;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <h1>Trottola</h1>
            <p>This service allows you to make HTTP requests to a specified URL with custom headers and user agents.</p>

            <h2>Usage</h2>
            <p>Send a POST request to <code>/proxy</code> with a JSON payload:</p>
            <pre>
{
    "url": "https://example.com",
    "headers": {
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36".
        ...
    },
    "strategy": "sequential", or "random"
}
            </pre>

            <h2>Response</h2>
            <p>The service will return a JSON response with:</p>
            <ul>
                <li><code>status_code</code>: HTTP status code of the response</li>
                <li><code>headers</code>: Headers from the response</li>
                <li><code>html</code>: HTML content of the response</li>
            </ul>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
