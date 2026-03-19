from flask import Flask, render_template, request
import urllib.parse
import os

app = Flask(__name__)

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

        # simple keyword (temporary MVP)
        query = "product"

        if "amazon" in product_link.lower():
            query = "amazon product"
        elif "flipkart" in product_link.lower():
            query = "flipkart product"
        elif "croma" in product_link.lower():
            query = "croma product"

        search_query = urllib.parse.quote(query)

        links = {
            "Amazon": f"https://www.amazon.in/s?k={search_query}",
            "Flipkart": f"https://www.flipkart.com/search?q={search_query}",
            "Croma": f"https://www.croma.com/search/?text={search_query}"
        }

        return render_template("compare.html", links=links)

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


# RENDER FIX
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)