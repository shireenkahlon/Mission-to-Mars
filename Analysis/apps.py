# import flask.Flask, flask.render_template, flask.redirect, flask_pymongo.PyMongo, scrape
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

#Set up Flask
app=Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

# Define the route for the HTML page
@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

# Define the scraped data route
@app.route("/scrape")
def scraper():
    mars=mongo.db.mars
    mars_data=scrape.scrape_all()
    mars.update({},mars_data,upsert=True) 
    return redirect('/', code=302)
if __name__ == "__main__":
    app.run()



