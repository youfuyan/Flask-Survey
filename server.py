from flask import *
import psycopg2, os
import json

app = Flask(__name__)

# DATABASE_URL = os.environ.get("DATABASE_URL")


def insert_survey_responses(customer, breeder, rating, recommend, comments):
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO survey_responses (customer, breeder, rating, recommend, comments) VALUES (%s, %s, %s, %s, %s)",
        (customer, breeder, rating, recommend, comments),
    )
    conn.commit()
    cur.close()
    conn.close()


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


@app.route("/api/results")
def results():
    # Connect to the database and retrieve the survey results
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cur = conn.cursor()

    order = "ASC" if request.args.get("reverse") != "true" else "DESC"
    cur.execute(f"SELECT * FROM survey_responses ORDER BY id {order}")
    results = cur.fetchall()

    # Convert the results to a list of dictionaries
    results_list = [
        {
            "id": r[0],
            "customer": r[1],
            "breeder": r[2],
            "rating": r[3],
            "recommend": r[4],
            "comments": r[5],
        }
        for r in results
    ]

    # Close the database connection
    cur.close()
    conn.close()

    # Return the results as JSON
    return jsonify(results_list)


@app.route("/admin/summary")
def summary():
    # fetch the results from the database
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cur = conn.cursor()
    cur.execute("SELECT * FROM survey_responses")
    data = cur.fetchall()

    # close the database connection
    cur.close()
    conn.close()

    # display data as chart.js chart
    return render_template("summary.html", data=data)


if __name__ == "__main__":
    app.run()
