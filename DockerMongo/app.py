import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

cluster = MongoClient("mongodb+srv://dbUser:BananaLOL@toiletbuddy.dxyty.mongodb.net/?retryWrites=true&w=majority&appName=ToiletBuddy")
db = cluster["ToiletBuddies"]
toilet_collection = db["Toilets"]

@app.route('/')
def index():
    return render_template('index.html',
			  items=list(toilet_collection.find()))

@app.route('/insert/', methods=['POST'])
def insert():
    item_doc = {
        'title': request.form['title'],
        'body': request.form['body']
    }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)