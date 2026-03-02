from flask import Flask, request, jsonify, render_template
from urllib.parse import urlparse, quote_plus
from datetime import datetime

app = Flask(__name__)

APP_NAME = "ShopIQ"
VERSION = "2.0"


@app.route("/")
def home():
    return render_template("index.html")


def extract_product_name(url):
    try:
        parsed = urlparse(url)
        path = parsed.path
        parts = path.split("/")

        for part in parts:
            if "-" in part and not part.lower().startswith("dp"):
                return part.replace("-", " ")

        return parts[-1]
    except Exception:
        return "Unknown Product"


def generate_platform_data(product_name):
    encoded_name = quote_plus(product_name)

    return {
        "Amazon": {
            "price": None,
            "rating": None,
            "url": f"https://www.amazon.in/s?k={encoded_name}&tag=YOURTAG"
        },
        "Flipkart": {
            "price": None,
            "rating": None,
            "url": f"https://www.flipkart.com/search?q={encoded_name}"
        },
        "Croma": {
            "price": None,
            "rating": None,
            "url": f"https://www.croma.com/searchB?q={encoded_name}"
        }
    }


@app.route("/compare", methods=["GET"])
def compare():
    link = request.args.get("link")

    if not link:
        return jsonify({
            "success": False,
            "error": "Product link is required"
        }), 400

    product_name = extract_product_name(link)
    platforms = generate_platform_data(product_name)

    return jsonify({
        "success": True,
        "app": APP_NAME,
        "version": VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "product": {
            "name": product_name,
            "original_link": link
        },
        "platforms": platforms
    })


if __name__ == "__main__":
    app.run(debug=True)