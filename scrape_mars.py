import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser

# path to execute

executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path)

# Define scrape dictionary
def scrape():
	
	final_data = {}
	output = marsNews()
	final_data["mars_news"] = output[0]
	final_data["mars_paragraph"] = output[1]
	final_data["mars_image"] = marsImage()
	final_data["mars_weather"] = marsWeather()
	final_data["mars_facts"] = marsFacts()
	final_data["mars_hemisphere"] = marsHem()

	return final_data

	# PART ONE
	# MARS NEWS

	# visit the Mars NASA news url through splinter module to find news article
def marsNews():
	mars_news = "https://mars.nasa.gov/news/"
	browser.visit(mars_news)
	html_news = browser.html
	news_soup = bs(html_news, "html.parser")
	news_title = news_soup.find("div", class_="content_title").text
	news_p = news_soup.find("div", class_="article_teaser_body").text
	output = [news_title, news_p]

	return output

	# PART TWO
	# IMAGES OF MARS

	# Visit Mars space Images through splinter to find featured image

def marsImage():
	image_mars = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	main_url = "https://www.jpl.nasa.gov"
	browser.visit(image_mars)
	html_image = browser.html
	image_soup = bs(html_image, "html.parser")
	featured_image_url  = image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
	featured_image_url= image_soup.find(class_="MAIN_IMAGE")
	featured_image_url = main_url + featured_image_url
	return featured_image_url

	# PART THREE
	# MARS WEATHER
	# Visit Mars weather on Twitter to get weather information
def marsWeather():
	weather_mars = "https://twitter.com/MarsWxreport?lang=en"
	browser.visit(weather_mars)
	html_weather = browser.html
	weather_soup = bs(html_weather,"html.parser")
	mars_weather = weather_soup.find("div", class_="css-1dbjc4n r-156q2ks").text
	return mars_weather

	# PART FOUR
	# FACTS ABOUT MARS

	# visit space facts to get mars data
def marsFacts():
	mars_facts_url = "https://space-facts.com/mars/"
	mars_facts_df = pd.read_html(mars_facts_url)
	mars_facts = mars_facts_df[0]
	mars_facts.columns = ["Description", "Value"]
	return mars_facts

	# PART FIVE
	# MARS HEMISPHERE

	# Create list of images and urls needed for hemispheres
def marsHem():
	hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	main_url = "https://astrogeology.usgs.gov"
	browser.visit(hemisphere_url)
	hemisphere_html = browser.html
	hemisphere_soup = bs(hemisphere_html, "html.parser")
	items = hemisphere_soup.find_all("div", class_="item")
	mars_hemisphere = []
	for i in items:
		title = i.find("h3").text
		img_url_part = i.find("a", class_="itemLink product-item")["href"]
		browser.visit(main_url + img_url_part)
		img_url_part_html = browser.html
		hemisphere_soup = bs(img_url_part_html, "html.parser")
		whole_img_url = main_url + hemisphere_soup.find("img", class_="wide-image")["src"]
		mars_hemisphere = mars_hemisphere.append({"title":title, "img_url":whole_img_url})
		return mars_hemisphere