from flask import *
import psycopg2, os
import json

app = Flask(__name__)

# DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(os.environ.get("DATABASE_URL"))


def insert_survey_responses(customer, breeder, rating, recommend, comments):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO survey_responses (customer, breeder, rating, recommend, comments) VALUES (%s, %s, %s, %s, %s)",
        (customer, breeder, rating, recommend, comments),
    )
    conn.commit()
    cur.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/survey", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        customer = request.form.get("customer")
        breeder = request.form.get("breeder")
        rating = request.form.get("rating")
        recommend = request.form.get("recommend")
        comments = request.form.get("comments")
        print(customer, breeder, rating, recommend, comments)
        if customer == "" or breeder == "":
            return render_template(
                "survey.html", message="Please enter required fields"
            )
        else:
            insert_survey_responses(customer, breeder, rating, recommend, comments)
            return render_template("thanks.html", breeder=breeder)
    return render_template("survey.html")


@app.route("/decline")
def decline():
    return render_template("decline.html")


@app.route("/thanks", methods=["POST"])
def thanks():
    customer = request.form.get("customer")
    breeder = request.form.get("breeder")
    rating = request.form.get("rating")
    comments = request.form.get("comments")

    # ... process form data and render the /thanks template with the customer, breeder, rating, and comments variables
    return render_template(
        "thanks.html",
        customer=customer,
        breeder=breeder,
        rating=rating,
        comments=comments,
    )


# @app.route("/api/facts", methods=["GET"])
# def get_random_fact():
#     return jsonify({"id": 1, "source": " my brain", "content": "Husky is cute"})


# @app.route("/api/facts", methods=["POST"])
# def new_fact():
#     print(request.json)
#     return jsonify("ok")


if __name__ == "__main__":
    app.run()
