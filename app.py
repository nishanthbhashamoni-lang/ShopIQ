from flask import Flask, request, jsonify
from urllib.parse import urlparse, quote_plus
from datetime import datetime

app = Flask(__name__)

APP_NAME = "ShopIQ"
VERSION = "1.0"


# Home route
@app.route("/")
def home():
    return jsonify({
        "app": APP_NAME,
        "version": VERSION,
        "status": "running"
    })


# Extract product name from URL
def extract_product_name(url):
    parsed = urlparse(url)
    path = parsed.path
    parts = path.split("/")

    for part in parts:
        if "-" in part and not part.lower().startswith("dp"):
            return part.replace("-", " ")

    return parts[-1]


# Generate affiliate-ready search links
def generate_search_links(product_name):
    encoded_name = quote_plus(product_name)

    # Replace YOURTAG with real affiliate tag later
    amazon_url = f"https://www.amazon.in/s?k={encoded_name}&tag=YOURTAG"
    flipkart_url = f"https://www.flipkart.com/search?q={encoded_name}"

    return {
        "amazon": amazon_url,
        "flipkart": flipkart_url
    }


# Compare route
@app.route("/compare", methods=["GET"])
def compare():
    link = request.args.get("link")

    if not link:
        return jsonify({"error": "Product link is required"}), 400

    product_name = extract_product_name(link)

    search_links = generate_search_links(product_name)

    response = {
        "app": APP_NAME,
        "version": VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "product": {
            "original_link": link,
            "name": product_name
        },
        "comparison_links": search_links,
        "note": "Prices and availability may vary on platform."
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)