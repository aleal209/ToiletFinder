from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://dbUser:BananaLOL@toiletbuddy.dxyty.mongodb.net/?retryWrites=true&w=majority&appName=ToiletBuddy")
db = cluster["ToiletBuddies"]
toilet_collection = db["Toilets"]


def brevet_insert(Name, Location, Gender):
    output = toilet_collection.insert_one({
        "Name": Name,
        "Location": Location,
        "Gender": Gender})
    _id = output.inserted_id  # this is how you obtain the primary key (_id) mongo assigns to your inserted document.
    return str(_id)

def brevet_find():
    lists = toilet_collection.find().sort("_id", -1).limit(1)
    for brevet_list in lists:
        return brevet_list["Name"], brevet_list["Location"], brevet_list["Gender"]