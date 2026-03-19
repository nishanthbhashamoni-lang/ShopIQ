from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/compare", methods=["GET", "POST"])
def compare():
    if request.method == "POST":
        product_link = request.form.get("product")

        # dummy prices (abhi ke liye)
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

    # agar direct /compare open kare
    return render_template("compare.html", prices=None)