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

    