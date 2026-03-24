from flask import Flask, render_template, request
import urllib.parse
import requests
import os

app = Flask(__name__)

API_KEY = "afea838a8bmshe9ad263202583ecp198ed5jsnef25381c1cba"   # 👈 yaha paste kar

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/compare", methods=["GET", "POST"])
def compare():
    if request.method == "POST":
        product_link = request.form.get("product")

        if not product_link:
            return "No product link provided"

        # 🔥 PRODUCT NAME CLEAN EXTRACTION
        try:
            query = product_link.split("/")[-1]
            query = query.split("?")[0]
            query = query.replace("-", " ").replace("%20", " ")
        except:
            query = "product"

        if len(query) < 3:
            query = "product"

        search_query = urllib.parse.quote(query)

        links = {
            "Amazon": f"https://www.amazon.in/s?k={search_query}",
            "Flipkart": f"https://www.flipkart.com/search?q={search_query}",
            "Croma": f"https://www.croma.com/search/?text={search_query}"
        }

        prices = {}

        try:
            url = "https://real-time-product-search.p.rapidapi.com/search"

            querystring = {
                "q": query,
                "country": "in"
            }

            headers = {
                "X-RapidAPI-Key": API_KEY,
                "X-RapidAPI-Host": "real-time-product-search.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            print("FULL API:", data)  # 🔍 DEBUG

            if "data" in data and len(data["data"]) > 0:
                product = data["data"][0]

                # 🔥 MULTIPLE PRICE FALLBACKS
                price = (
                    product.get("offer", {}).get("price")
                    or product.get("price")
                    or product.get("min_price")
                    or "N/A"
                )

                prices = {
                    "Amazon": price,
                    "Flipkart": price,
                    "Croma": price
                }

        except Exception as e:
            print("API ERROR:", e)
            prices = {}

        return render_template(
            "compare.html",
            links=links,
            prices=prices,
            query=query
        )

    return render_template("compare.html", links=None)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/disclosure")
def disclosure():
    return render_template("disclosure.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)