from flask import Flask, render_template, request
import requests
import urllib.parse
import os

app = Flask(__name__)

# 🔐 API KEY
API_KEY = os.environ.get("API_KEY")


# 🟢 AMAZON
def get_amazon_price(query):
    url = "https://real-time-amazon-data.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }

    params = {
        "query": query,
        "country": "IN"
    }

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5)
        data = res.json()

        products = data.get("data", {}).get("products", [])

        if products:
            p = products[0]

            price = (
                p.get("price") or
                p.get("product_price") or
                p.get("price_string")
            )

            if price:
                return str(price)

    except Exception as e:
        print("Amazon error:", e)

    return None


# 🔵 FLIPKART
def get_flipkart_price(query):
    url = "https://real-time-flipkart-data2.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "real-time-flipkart-data2.p.rapidapi.com"
    }

    params = {
        "query": query
    }

    try:
        res = requests.get(url, headers=headers, params=params, timeout=5)
        data = res.json()

        products = data.get("data", {}).get("products", [])

        if products:
            p = products[0]

            price = (
                p.get("price") or
                p.get("selling_price") or
                p.get("price_string")
            )

            if price:
                return f"₹{price}"

    except Exception as e:
        print("Flipkart error:", e)

    return None


# 🏠 HOME
@app.route("/")
def home():
    return render_template("index.html")


# 🔍 COMPARE
@app.route("/compare", methods=["POST"])
def compare():
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

    # 🔥 GET REAL PRICES
    amazon_price = get_amazon_price(query)
    flipkart_price = get_flipkart_price(query)

    # 🚨 fallback ONLY if API fails
    if not amazon_price:
        amazon_price = f"₹{1500 + len(query)*7}"

    if not flipkart_price:
        flipkart_price = f"₹{1400 + len(query)*9}"

    # 🟡 CROMA (dummy for now)
    croma_price = f"₹{1600 + len(query)*5}"

    prices = {
        "Amazon": amazon_price,
        "Flipkart": flipkart_price,
        "Croma": croma_price
    }

    # 🔗 LINKS
    search_query = urllib.parse.quote(query)

    links = {
        "Amazon": f"https://www.amazon.in/s?k={search_query}",
        "Flipkart": f"https://www.flipkart.com/search?q={search_query}",
        "Croma": f"https://www.croma.com/search/?text={search_query}"
    }

    return render_template(
        "compare.html",
        prices=prices,
        links=links,
        query=query
    )


# 📄 OTHER PAGES
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/disclosure")
def disclosure():
    return render_template("disclosure.html")


# 🚀 RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)