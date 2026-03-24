from flask import Flask, render_template, request
import urllib.parse
import os
import requests

app = Flask(__name__)

# 🔥 RapidAPI config (abhi blank rakho ya baad me add karo)
API_KEY = "YOUR_API_KEY_HERE"
API_HOST = "real-time-product-search.p.rapidapi.com"


# HOME
@app.route("/")
def home():
    return render_template("index.html")


# COMPARE
@app.route("/compare", methods=["GET", "POST"])
def compare():
    if request.method == "POST":
        product_link = request.form.get("product")

        if not product_link:
            return "No product link provided"

        # 🔥 PRODUCT NAME EXTRACT
        try:
            query = product_link.split("/")[-1]
            query = query.split("?")[0]
            query = query.replace("-", " ").replace("%20", " ")
        except:
            query = "product"

        if len(query) < 3:
            query = "product"

        search_query = urllib.parse.quote(query)

        # 🔥 AFFILIATE / SEARCH LINKS
        links = {
            "Amazon": f"https://www.amazon.in/s?k={search_query}",
            "Flipkart": f"https://www.flipkart.com/search?q={search_query}",
            "Croma": f"https://www.croma.com/search/?text={search_query}"
        }

        # 🔥 API PRICE DATA (optional)
        prices = {}

        try:
            url = "https://real-time-product-search.p.rapidapi.com/search"
            querystring = {"q": query, "country": "in"}

            headers = {
                "X-RapidAPI-Key": API_KEY,
                "X-RapidAPI-Host": API_HOST
            }

            response = requests.get(url, headers=headers, params=querystring, timeout=5)
            data = response.json()

            if "data" in data and len(data["data"]) > 0:
                product = data["data"][0]

                price_value = product.get("price", None)

                prices = {
                    "Amazon": price_value,
                    "Flipkart": price_value,
                    "Croma": price_value
                }

        except:
            prices = {}

        # 🔥 TABLE DATA (FOR UI)
        comparison = [
            {
                "platform": "Amazon",
                "price": prices.get("Amazon"),
                "rating": 4.3,
                "reviews": 1200,
                "best": True
            },
            {
                "platform": "Flipkart",
                "price": prices.get("Flipkart"),
                "rating": 4.2,
                "reviews": 900,
                "best": False
            },
            {
                "platform": "Croma",
                "price": prices.get("Croma"),
                "rating": 4.1,
                "reviews": 500,
                "best": False
            }
        ]

        return render_template(
            "compare.html",
            links=links,
            prices=prices,
            query=query,
            comparison=comparison
        )

    return render_template("compare.html", links=None)


# CONTACT
@app.route("/contact")
def contact():
    return render_template("contact.html")


# PRIVACY
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# DISCLOSURE
@app.route("/disclosure")
def disclosure():
    return render_template("disclosure.html")


# 🚨 RENDER SAFE RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)