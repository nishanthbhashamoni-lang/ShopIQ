from flask import Flask, render_template, request
import random

app = Flask(__name__)

def extract_product_name(link):
    try:
        name = link.split("/")[-1]
        name = name.replace("-", " ")
        return name.upper()
    except:
        return "Sample Product"

def generate_comparison():
    platforms = ["Amazon", "Flipkart", "Croma"]
    data = []

    for platform in platforms:
        price = random.randint(45000, 55000)
        rating = round(random.uniform(4.0, 4.8), 1)
        reviews = random.randint(1000, 20000)

        data.append({
            "platform": platform,
            "price": price,
            "rating": rating,
            "reviews": reviews
        })

    best_price = min(item["price"] for item in data)

    for item in data:
        item["best"] = item["price"] == best_price

    return data

@app.route("/", methods=["GET", "POST"])
def home():
    comparison = None
    product_name = None

    if request.method == "POST":
        link = request.form.get("link")
        product_name = extract_product_name(link)
        comparison = generate_comparison()

    return render_template("index.html",
                           comparison=comparison,
                           product_name=product_name)

if __name__ == "__main__":
    app.run(debug=True)