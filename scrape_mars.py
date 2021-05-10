# Import Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import re
    
#Create dictionary to be imported into mongoDB
mars_info = {}

def mars_news(browser):

    #Visit NASA Mars News through splinter
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    #HTML Object and Parse with BS
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[1]
    news_title_text = news_title.find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    #Import into dictionary
    mars_info['news_title'] = news_title_text
    mars_info['news_teaser'] = news_p

def mars_image(browser):

    #JPL Mars Images
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    image_button = browser.find_by_id('full_image')
    image_button.click()
    more_info = browser.links.find_by_partial_text('more info')
    more_info.click()

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve Background Image
    image_url =  soup.find('img', class_='main_image')['src']

    url = jpl_url.split('spaceimages')[0]

    url = url[:-1]

    featured_image_url = url + image_url

    #Import into dictionary
    mars_info["image_url"] = featured_image_url

def mars_facts(browser):

    #Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    facts_df = pd.read_html(facts_url)[0]

    facts_df.columns=["Description","Mars"]

    facts_df.set_index("Description", inplace=True)

    # convert dataframe to html
    facts_html = facts_df.to_html(justify='left', classes="table table-striped")

    #Import mars facts into dictionary
    mars_info["mars_facts"] = facts_html

def mars_hemispheres(browser):

    #Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #HTML Object and Parse with BS
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Url and list for later use
    main_url = 'https://astrogeology.usgs.gov'
    hemispheres = []

    #Find every instance of a hemisphere, and create for loop
    items = soup.find_all('div', class_='item')
    for i in items:
        
        #Retreive title and image url, visit the url by combining with main URL
        title  = i.find('h3').text
        image_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(main_url + image_url)
        
        #Browse the indidvudal HTML and access the full size image
        image_html = browser.html
        soup = BeautifulSoup(image_html, 'html.parser')
        img_url = main_url + soup.find('img', class_='wide-image')['src']
        
        #Append to list of dictionaries 
        hemispheres.append({"title" : title, "img_url" : img_url})

    mars_info['hemispheres'] = hemispheres
   