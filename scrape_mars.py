#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time


def init_browser():
    executable_path = {'executable_path':'/Users/ncabayan/Downloads/chromedriver'}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    # Visit the Mars news page. 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #search the news and scrape all the info into soup
    html = browser.html
    soup = bs(html,"html.parser")


    # save the most recent article, title and date
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
    
    # Add the news date, title and summary to the dictionary
    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p

#JPL STUF #____________________________________
    # Visit the JPL Mars URL
    url2 = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    # Scrape the browser into soup and use soup to find the image of mars
    # Save the image url to a variable called `img_url`
    html = browser.html
    soup = bs(html,"html.parser")
    image = soup.find("img", class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url

    # Add the featured image url to the dictionary
    mars_data["featured_image_url"] = featured_image_url

#Mars Weather Section via twitter_______________________________
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)


    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    
    url_facts = "https://space-facts.com/mars/"

    table = pd.read_html(url_facts)

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])


    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")

    mars_data["mars_html_table"] =  mars_html_table

# Visit the USGS Astogeology site and scrape pictures of the hemispheres
    urlastro = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(urlastro)

    html = browser.html
    soup = bs(html, 'html.parser')
    mars_hemis=[]

# loop through the four tags and load the data to the dictionary
    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()

    mars_data['mars_hemis'] = mars_hemis
    # Return the dictionary
    return mars_data

