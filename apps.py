#import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo, MongoClient
import scrape

# #Set up Flask
app=Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)
# client = MongoClient('mongodb://localhost:27017/mars_app')
# db=mongo.mars_app

# define the route for the HTML page
@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

#define the scraped data route
@app.route("/scrape")
def scraper():
    mars=mongo.db.mars
    mars_data=scrape.scrape_all()
    mars.update({},mars_data,upsert=True) 
    return redirect('/', code=302)
if __name__ == "__main__":
    app.run()



