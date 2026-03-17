from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/compare", methods=["POST"])
def compare():

    product_link = request.form.get("product")

    # demo prices
    prices = {
        "Amazon": random.randint(500,2000),
        "Flipkart": random.randint(500,2000),
        "Croma": random.randint(500,2000)
    }

    best_price = min(prices.values())

    return render_template(
        "compare.html",
        product_link=product_link,
        prices=prices,
        best_price=best_price
    )


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
    app.run(debug=True)