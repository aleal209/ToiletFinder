import flask
from flask import Flask, request, jsonify, flash, session
import config
import logging
#from mypymongo import MongoClient
from pymongo import MongoClient
from flask import render_template


app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = "TheHorseIsHere"
cluster = MongoClient("mongodb+srv://dbUser:BananaLOL@toiletbuddy.dxyty.mongodb.net/?retryWrites=true&w=majority&appName=ToiletBuddy")
db = cluster["ToiletBuddies"]
toilet_collection = db["Toilets"]
review_collection = db["Reviews"]
user_collection = db["UserInfo"]

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('login.html')

@app.route("/find-bathroom")
def find_bathroom():
    return flask.render_template('map.html')


@app.route("/add-bathroom")
def add_bathroom():
    return flask.render_template('add.html')

@app.route("/profile")
def profile():
    name = session['Username']
    reviews = []
    ratings = []
    tmp = {}
    rating = 0
    count = 0
    for review in review_collection.find():
        if review['Username'] == name:
            tmp = (review["Name"], review["Review"])
            count += 1
            reviews.append(tmp)
            ratings.append(review["Review"])
    for r in ratings:
        rating += r
    if count == 0:
        rating = "No Reviews Yet!"
    else:
        rating /= count
    return flask.render_template('profile.html', name=name, reviews=reviews, rating=rating)

@app.route("/welcome")
def welcome():
    return flask.render_template('welcome.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404

@app.route('/api/data')
def get_bathrooms():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    offset = (page - 1) * limit

    # Get the total count of bathrooms (for pagination purposes)
    total_count = toilet_collection.count_documents({})

    # Fetch the bathrooms with pagination
    bathrooms = toilet_collection.find().skip(offset).limit(limit)

    bathrooms_list = [
        {'name': bathroom['Name'], 'lat': float(bathroom['Lat']), 'lon': float(bathroom['Long']),
         'gender': bathroom['Gender'],
         'accessible': bathroom['Accessible'], 'Floor': bathroom['Floor'], 'baby': bathroom['Baby Changing'],
         'dryer': bathroom['Hand Dryer'],
         'sanitizer': bathroom['Hand Sanitizer'], 'cover': bathroom['Toilet Seat Cover']}
        for bathroom in bathrooms
    ]
    
    # Return the data along with the total count
    return jsonify({
        'bathrooms': bathrooms_list,
        'total_count': total_count
    })

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the username already exists
        if user_collection.find_one({'Username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        elif user_collection.find_one({'Email': email}):
            flash('Email already in use. Choose a different one.', 'danger')
        else:
            user_collection.insert_one({'Email': email, 'Username': username, 'Password': password})
            flash('Registration successful. You can now log in.', 'success')

    return render_template('welcome.html')

@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        signin_user = user_collection.find_one({'Username': request.form['username']})

        if signin_user:
            if request.form['password'] == signin_user['Password']:
                session['Username'] = request.form['username']
                flash('Successfully logged in.', 'success')
                return render_template('login.html')

        flash('Username and password combination is wrong', 'danger')
        return render_template('login.html')

    return render_template('login.html')

@app.route('/submit-bathroom', methods=['POST'])
def submit_bathroom():
    if not session.get("Username"):
        flash('You need to sign in', 'danger')
        return render_template('login.html')
    # Capture form data
    name = request.form.get('name')
    lat = float(request.form.get('lat'))
    lon = float(request.form.get('lon'))
    gender = request.form.get('Gender', '').strip()
    accessible = request.form.get('Accessible')
    baby = (request.form.get('Baby Changing'))
    dryer = (request.form.get('Hand Dryer'))
    sanitizer = request.form.get('Hand Sanitizer')
    cover = (request.form.get('Toilet Seat Cover'))
    floor = int((request.form.get('Floor')))
    review = request.form.get('rating')

    if not review:
        review = 0


    # Format the data
    bathroom_entry = {
        'Name': name,
        'Lat': lat,
        'Long': lon,
        "Gender": gender,
        "Accessible": accessible,
        "Baby Changing": baby,
        "Hand Dryer": dryer,
        "Hand Sanitizer": sanitizer,
        "Toilet Seat Cover": cover,
        "Average Review": float(review),
        "Review Count": 1,
        "Floor": floor,
        "Reports": 0
    }

    review_entry = {
        "Username": session['Username'],
        'Name' : name,
        'Review' : float(review)
    }

    # Check if the username already exists
    if toilet_collection.find_one({'Name': name}):
        flash('Name already exists! Choose a different one.', 'danger')
        return render_template('add.html')
    else:
        # Insert into MongoDB
        result = toilet_collection.insert_one(bathroom_entry)
        review_result = review_collection.insert_one(review_entry)
        total_count = toilet_collection.count_documents({})
        flash('Success! Bathroom added.', 'success')
        return render_template('add.html')

    #bathroom_entry['_id'] = str(result.inserted_id)
    #return jsonify({"message": "Bathroom added successfully!", "data": bathroom_entry}), 201

@app.route("/logout")
def logout():
    if not session.get("Username"):
        flash('You are not logged in', 'danger')
        return flask.render_template('login.html')

    session["Username"] = None
    flash('Successfully logged out', 'success')
    return flask.render_template('login.html')


app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")   
