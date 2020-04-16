# Import Dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os


# Hidden authetication file
#import config 

# Create an instance of Flask app
app = Flask(__name__)

#Use flask_pymongo to set up connection through mLab
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def index(): 

    # Find data
    mars = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 
    mars = mongo.db.mars
    mars = scrape_mars.scrape()
    mars.update({}, mars, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)

    