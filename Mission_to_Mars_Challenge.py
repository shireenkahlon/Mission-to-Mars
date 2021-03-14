
#import Splinter, BeautifulSoup, Pandas, webdriver, ChromeDriverManager, time, and random
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

#Set the executable path
executable_path={'executable_path':'/usr/local/bin/chromedriver'}
browser=Browser('chrome',**executable_path,headless=False)

# Visit the mars nasa news site
url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)

#Delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

#set up html parser
html=browser.html
news_soup=soup(html,'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')
# print(slide_elem)

#scrape the title
news_title=slide_elem.find('div',class_='content_title').get_text()
news_p=slide_elem.find('div',class_='article_teaser_body').get_text()
print(news_p)


# ### Featured Images

#visit url
url='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem=browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html=browser.html
img_soup=soup(html,'html.parser')

# Find the relative image url
img_url_rel=img_soup.find('img',class_='fancybox-image').get('src')
img_url=f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

#Scrape the table data from space-facts.com
df=pd.read_html('https://space-facts.com/mars/')[0]
df.columns=['description','value']
df.set_index('description',inplace=True)
df
df.to_html

#quit browser
browser.quit()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'

browser.visit(url)
html=browser.html
mars_soup=soup(html,'html.parser')

#Create list for hemisphere_image_urls
hemisphere_image_urls = []
links = browser.find_by_css('a.product-item img')

#loop through site to scrape title and image
for i in range(len(links)):
    hemisphere = {}
    browser.find_by_css('a.product-item img')[i].click()
    # find the Sample image - anchor tag and extract href
    sample_elem = browser.links.find_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    # Get Hemisphere title
    hemisphere['title'] = browser.find_by_css('h2.title').text
    # Add hemisphere object to list
    hemisphere_image_urls.append(hemisphere)
    # Navigate backwards
    browser.back()
print(hemisphere_image_urls)


