from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import os
import re

# path to execute

def init_browser():
	executable_path = {"executable_path": "..\Mongodb\chromedriver.exe"}
	browser = Browser("chrome", **executable_path, headless=False)

def scrape_info():
	browser = init_browser

	# PART ONE
	# MARS NEWS

	# visit the Mars NASA news url through splinter module to find news article

	mars_news = "https://mars.nasa.gov/news/"
	browser.visit(mars_news)

	# scrap page into soup

	html_news = browser.html
	news_soup = bs(html_news, "html.parser")

	# retrieve news title and news paragraph
	news_title = soup.find("div", class_="content_title").text
	news_parg = soup.find("div", class_="article_teaser_body").text

	# Display scraped data
	print(news_title)
	print(news_parg)

	# PART TWO
	# IMAGES OF MARS

	# Visit Mars space Images through splinter to find featured image
	image_mars = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	main_url = "https://www.jpl.nasa.gov"
	browser.visit(image_mars)

	# scrap image into soup

	html_image = browser.html
	image_soup = bs(html_image, "html.parser")


	# change Nonetype object to str
	featured_image_url  = image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]


	# Retrieve image

	search_image= image_soup.find(class_="MAIN_IMAGE")
	featured_image_url = main_url + featured_image_url
	print(featured_image_url)

	# PART THREE
	# MARS WEATHER
	# Visit Mars weather on Twitter to get weather information

	weather_mars = "https://twitter.com/MarsWxreport?lang=en"
	browser.visit(weather_mars)

	# Scrape page into Soup
	html_weather = browser.html

	weather_soup = bs(html_weather,"html.parser")
	# Find the text in soup
    
	mars_weather = weather_soup.find("div", class_="css-1dbjc4n r-156q2ks").text
	print(mars_weather)

	# PART FOUR
	# FACTS ABOUT MARS

	# visit space facts to get mars data

	facts_mars_url = "https://space-facts.com/mars/"

	# scrap data
	facts_mars = pd.read_html(facts_mars_url)
	facts_mars_df = facts_mars[0]

	# create a dataframe with columns

	facts_mars_df.columns = ["Description", "Value"]
	facts_mars_df

	# PART FIVE
	# MARS HEMISPHERE

	# Create list of images and urls needed for hemispheres
	hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	main_url = "https://astrogeology.usgs.gov"

	# visit the website to find Mars info
	browser.visit(hemisphere_url)

	hemisphere_html = browser.html
	hemisphere_soup = bs(hemisphere_html, "html.parser")

	items = hemisphere_soup.find_all("div", class_="item")

	# loop to create a list of image urls
	img_list_urls = []
	for i in items:
    		title = i.find("h3").text
    		img_url_part = i.find("a", class_="itemLink product-item")["href"]
    		browser.visit(main_url + img_url_part)
    		img_url_part_html = browser.html
    		hemisphere_soup = bs(img_url_part_html, "html.parser")
    
    		whole_img_url = main_url + hemisphere_soup.find("img", class_="wide-image")["src"]
    
    		img_list_urls.append({"title":title, "img_url":whole_img_url})

    
 # PART 6 
 # STORE DATA IN A DICTIONARY 
    	
mars_data = {
	"news_title": news_title,
	"news_parg": news_parg,
	"featured_image_url": featured_image_url,
	"mars_weather": mars_weather,
	"facts_mars": facts_mars_df,
	"img_list_urls": img_list_urls
    }

# Close the browser
browser.quit()

