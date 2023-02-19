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
    # fetch the average ratings from the database
    cur.execute(
        "SELECT breeder, ROUND(AVG(rating), 2) AS average_rating FROM survey_responses GROUP BY breeder"
    )
    data2 = cur.fetchall()
    # fetch the recommendations from the database
    cur.execute(
        "SELECT breeder, recommend, COUNT(*) FROM survey_responses GROUP BY breeder, recommend"
    )
    recommend_data = cur.fetchall()

    # close the database connection
    cur.close()
    conn.close()

    # Parse the data to create an array of timestamps and an array of counts for each timestamp
    timestamps = []
    counts = []
    for row in data:
        timestamp = row[6].strftime("%Y-%m-%d")
        if timestamp in timestamps:
            index = timestamps.index(timestamp)
            counts[index] += 1
        else:
            timestamps.append(timestamp)
            counts.append(1)
    # print(timestamps)
    # print(counts)

    # Parse the data to create an array of breeders and an array of ratings
    breeders = [row[0] for row in data2]
    ratings = [row[1] for row in data2]

    # Parse the data to create an array of breeders and an array of recommendations
    # Separate the data into four arrays, one for each breeder
    breeder1_data = []
    breeder2_data = []
    breeder3_data = []
    breeder4_data = []
    for row in recommend_data:
        breeder = row[0]
        recommend = row[1]
        count = row[2]
        if breeder == "Echoing Wind Siberians":
            breeder1_data.append({"recommend": recommend, "count": count})
        elif breeder == "Cascade Siberians":
            breeder2_data.append({"recommend": recommend, "count": count})
        elif breeder == "Antler Creek Siberians":
            breeder3_data.append({"recommend": recommend, "count": count})
        elif breeder == "Bruck's Siberian Huskies":
            breeder4_data.append({"recommend": recommend, "count": count})
    print(breeder1_data)
    print(breeder2_data)
    print(breeder3_data)
    print(breeder4_data)

    return render_template(
        "summary.html",
        data=data,
        timestamps=timestamps,
        counts=counts,
        breeders=breeders,
        ratings=ratings,
        breeder1_data=breeder1_data,
        breeder2_data=breeder2_data,
        breeder3_data=breeder3_data,
        breeder4_data=breeder4_data,
    )


if __name__ == "__main__":
    app.run()
