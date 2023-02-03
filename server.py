from flask import Flask, render_template,  redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    if request.method == "POST":
        customer = request.form.get('customer')
        breeder = request.form.get('breeder')
        rating = request.form.get('rating')
        comments = request.form.get('comments')
        # print(customer, breeder, rating, comments)
        if customer == '' or breeder == '':
            return render_template('index.html', message='Please enter required fields')
        return render_template('thankyou.html')


if __name__ == "__main__":
    app.run(debug=True)