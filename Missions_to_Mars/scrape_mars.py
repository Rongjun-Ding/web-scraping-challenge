# Dependencies
import pandas as pd
import requests as req
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from pprint import pprint
import pymongo
from flask import Flask, render_template
import numpy as np
import json
from selenium import webdriver

def scrape():
    #Getting ChromeDriver path
    executable_path = {'executable_path': 'chromedriver.exe'}
    #Getting the browser
    browser = Browser('chrome', **executable_path, headless=False)

    #Defining an empty collection
    mars_collection = {}

    # Getting NASA Mars News
    url = ('https://mars.nasa.gov/news/')
    browser.visit(url)
    response = req.get(url)
    time.sleep(1)
    soup = bs(response.text, 'html.parser')

    mars_collection["news_title"] = soup.find('div', class_="content_title").get_text()
    mars_collection["news_photo"] = soup.find('div', class_="rollover_description_inner").get_text()

    #Getting Space Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    response = req.get(url)
    time.sleep(2)
    soup = bs(response.text, 'html.parser')    
    image_url = soup.find('article', class_='carousel_item')
    footer = image_url.find('footer')
    ref = footer.find('a')
    path = ref['data-fancybox-href']
    featured_image_url = ('https://www.jpl.nasa.gov' + path)

    mars_collection["featured_image_url"] = featured_image_url 

    #Getting Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    table = pd.read_html(url)       
    df = table[0]
    df.columns = ["Facts", "Value"]
    facts_html = df.to_html()
    facts_html = facts_html.replace("\n","")
    mars_collection["fact_table"] = facts_html

    #Mars Hemispheres
    #empty list
    hemisphere_image_urls =[]

    #Cerberus Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)
    response = req.get(url)
    time.sleep(2)
    soup = bs(response.text, 'html.parser')
    Cerberus_image = soup.find_all('div', class_="wide-image-wrapper")
    
    for image in Cerberus_image:
        picture = image.find('li')
        Cerberus_image_url = picture.find('a')['href']
    
    cerberus_title = soup.find('h2', class_='title').text   
    Cerberus_Hemisphere = {"Title": cerberus_title, "url": Cerberus_image_url}
    
    hemisphere_image_urls.append(Cerberus_Hemisphere)

