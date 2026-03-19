from flask import Flask, render_template, request
import random
import os

app = Flask(__name__)

# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# COMPARE PAGE
@app.route("/compare", methods=["GET", "POST"])
def compare():
    if request.method == "POST":
        product_link = request.form.get("product")

        if not product_link:
            return "No product link provided"

        # dummy prices (for now)
        prices = {
            "Amazon": random.randint(500, 2000),
            "Flipkart": random.randint(500, 2000),
            "Croma": random.randint(500, 2000)
        }

        best_price = min(prices.values())

        return render_template(
            "compare.html",
            prices=prices,
            best_price=best_price,
            product_link=product_link
        )

    # agar user direct /compare open kare
    return render_template("compare.html", prices=None)


# CONTACT PAGE
@app.route("/contact")
def contact():
    return render_template("contact.html")


# PRIVACY PAGE
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# DISCLOSURE PAGE
@app.route("/disclosure")
def disclosure():
    return render_template("disclosure.html")


# 🚨 IMPORTANT FOR RENDER (PORT FIX)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)