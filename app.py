#Import
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
from splinter import Browser

# INITIATE YOUR CONFIGURATION 
app = Flask(__name__)
mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_db')

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def main():
        mars_info = mongo.db.mars_info.find_one()
        return render_template("index.html", mars_info=mars_info)
    

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    executable_path = {'executable_path': '/Users/manishalal/Desktop/Bootcamp_Homework/Web Scrapping/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Run scrapped functions
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.mars_news(browser)
    mars_data = scrape_mars.mars_image(browser)
    mars_data = scrape_mars.mars_facts(browser)
    mars_data = scrape_mars.mars_hemispheres(browser)
    mars_info.update({}, mars_data, upsert=True)

    browser.quit()

    return redirect("/")

if __name__ == "__main__": 
    app.run(debug= True)