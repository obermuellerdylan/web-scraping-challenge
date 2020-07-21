# import necessary libraries
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
import datetime as dt
import re
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def space_images():
    browser = init_browser()

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    url = 'https://www.jpl.nasa.gov'
    image = soup.find('article')
    image_query = image['style'][23:-3]
    image_url = url + image_query
    #print(image_url)
    browser.quit()
    return image_url

def mars_news():
    browser = init_browser()

    mars_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(mars_url)

    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    news_list=[]
    class_title = soup.find(class_='list_text')
    news_title = class_title.find('a').text.strip()
    news_p = soup.find(class_="rollover_description_inner").text.strip()
    news_list.append(news_title)
    news_list.append(news_p)
    # print(news_list)
    browser.quit()
    return news_list



def mars_weather():    
    browser = init_browser()

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    browser.is_text_not_present('InSight', wait_time=10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    tweet = soup.find('span', text=re.compile("InSight")).text.strip()
    #print(tweet)
    browser.quit()
    return tweet

def mars_facts():
        # fact_url = 'https://space-facts.com/mars/'
        # browser.visit(fact_url)

    table_url = 'https://space-facts.com/mars/'
    table = pd.read_html(table_url)
    df = table[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description', inplace=True)
    html_table = df.to_html()
    return html_table

def mars_images():
    browser = init_browser()

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_list = []

    for i in range(4):
        all_h3 = browser.find_by_css('a.product-item h3')
        hemisphere_dict = {}
        all_h3[i].click()

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        Sample = browser.find_by_text('Sample')
        title = soup.find('h2').text.strip()
        hemisphere_dict['title']= title
        hemisphere_dict['image_url']=Sample['href']
        hemisphere_list.append(hemisphere_dict)
        browser.back()
    
    browser.quit()
    return hemisphere_list

def scrape():
    mars = {}
    mars['mars_news'] = mars_news()
    mars['space_images'] = space_images()
    mars['mars_weather'] = mars_weather()
    mars['mars_facts'] = mars_facts()
    mars['mars_images'] = mars_images()
    
    return mars



