from flask import Flask, render_template,  redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:QWER333666@localhost:5432/husky'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Summary(db.Model):
    __tablename__ = 'summary'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    breeder = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.String(200))

    def __init__(self, customer, breeder, rating, comments):
        self.customer = customer
        self.breeder = breeder
        self.rating = rating
        self.comments = comments

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    # if request.method == 'POST':
    #     if not request.form.get('text_input') or len(request.form.get('text_input')) < 3:
    #         return render_template('survey.html', error='Text input is required and must have a minimum length of 3 characters.')
    #     else:
    #         return render_template('thanks.html')
    # return render_template('survey.html')
    if request.method == "POST":
        customer = request.form.get('customer')
        breeder = request.form.get('breeder')
        rating = request.form.get('rating')
        comments = request.form.get('comments')
        print(customer, breeder, rating, comments)
        if customer == '' or breeder == '':
            return render_template('survey.html', message='Please enter required fields')
        else:
            return render_template('thanks.html', breeder=breeder)
    return render_template('survey.html')

@app.route('/decline')
def decline():
    return render_template('decline.html')

@app.route('/thanks', methods=['POST'])
def thanks():
    customer = request.form.get('customer')
    breeder = request.form.get('breeder')
    rating = request.form.get('rating')
    comments = request.form.get('comments')

    # ... process form data and render the /thanks template with the customer, breeder, rating, and comments variables
    return render_template('thanks.html', customer=customer, breeder=breeder, rating=rating, comments=comments)


if __name__ == "__main__":
    app.run()