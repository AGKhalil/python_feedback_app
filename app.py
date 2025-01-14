from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

import sys


def print_to_stdout(*a):

    # Here a is the array holding the objects
    # passed as the arguement of the function
    print(*a, file=sys.stdout)


print_to_stdout("Hello World")

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://mpusiedmvpvnnx:f28ef0c11d6af66e53788beee0b820910c7e9682e5ddaf8fc9ffe1d58e48070c@ec2-54-235-108-217.compute-1.amazonaws.com:5432/dcv0k4q2k6ues0'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/transaction/sale/read', methods=['POST'])
def respond():
    print_to_stdout("FUUUUCK")
    return render_template('webhook.html', variable="FUCK")


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        if customer == '' or dealer == '':
            return render_template('index.html',
                                   message='Please enter required fields')
        if db.session.query(Feedback).filter(
                Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html',
                               message='You have already submitted feedback')


if __name__ == '__main__':
    app.run()
