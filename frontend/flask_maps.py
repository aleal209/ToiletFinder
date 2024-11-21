import flask
from flask import Flask, request, jsonify
import config
import logging
#from mypymongo import MongoClient
from pymongo import MongoClient
from flask import render_template


app = flask.Flask(__name__)
CONFIG = config.configuration()

cluster = MongoClient("mongodb+srv://dbUser:BananaLOL@toiletbuddy.dxyty.mongodb.net/?retryWrites=true&w=majority&appName=ToiletBuddy")
db = cluster["ToiletBuddies"]
toilet_collection = db["Toilets"]
review_collection = db["Reviews"]
user_collection = db["UserInfo"]

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('welcome.html')

@app.route("/find-bathroom")
def find_bathroom():
    return flask.render_template('map.html')

@app.route("/add-bathroom")
def add_bathroom():
    return flask.render_template('add.html')

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
        {'name': bathroom['Name'], 'lat': float(bathroom['Lat']), 'lon': float(bathroom['Long']), 'gender': bathroom['Gender']}
        for bathroom in bathrooms
    ]
    
    # Return the data along with the total count
    return jsonify({
        'bathrooms': bathrooms_list,
        'total_count': total_count
    })

@app.route('/submit-bathroom', methods=['POST'])
def submit_bathroom():
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
    reports = 0

    # Format the data
    bathroom_entry = {
        'Name': name,
        'Lat': lat,
        'Long': lon,
        "Gender": gender,
        "Accessible": accessible,
        "Baby Changing": baby,
        "Hand Dryer": sanitizer,
        "Toilet Seat Cover": cover,
        "Floor": floor,
        "Reports": 0
    }

    # Insert into MongoDB
    result = toilet_collection.insert_one(bathroom_entry)
    
    total_count = toilet_collection.count_documents({})


    return render_template(
        'success.html',
        message="Bathroom added successfully!",
        total_count=total_count,
        bathroom=bathroom_entry
    ), min(201 + total_count, 299)  # Cap the status code at 299

    #bathroom_entry['_id'] = str(result.inserted_id)
    #return jsonify({"message": "Bathroom added successfully!", "data": bathroom_entry}), 201

    


app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")   