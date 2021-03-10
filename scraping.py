

#import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager



def scrape_app():
    # Initiate headless driver for deployment
    executable_path={executable_path: ChromeDriverManager().install()}
    browser=Browser('chrome',**executable_path,headless=False)
    news_title, news_p=mars_data(browser)
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now()
    }
    #quit the browser
    browser.quit()
    return data

#make a function for the news title and paragraph
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

   # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

   # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    #Add try and except block:
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first <a> tag and save it as  `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    #return news title and paragraph
    return news_title, news_p

#Create a function to scrape image
def FeaturedImage(browser):
     # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AbsoluteError:
        return None, None
    
    #Use the base url to create an absolute url
    img_url=f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    #return the absolute url
    return img_url

#Create a function to scrape Mars facts
def mars_facts(browser):
    try:
    #Scrape the table data from space-facts.com
        df=pd.read_html('https://space-facts.com/mars/')[0]
    except BaseException:
        return None
    df.columns=['description','value']
    df.set_index('description',inplace=True)
    return df.to_html
if __name__=='__main__':
     # If running as script, print scraped data
    print(scrape_all())



# # Set the executable path and initialize the chrome browser in splinter
# executable_path={'executable_path':'/usr/local/bin/chromedriver'}
# browser=Browser('chrome',**executable_path,headless=False)

# # Visit the mars nasa news site
# url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
# browser.visit(url)

# # Optional delay for loading the page
# browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# #Set up html parser
# html=browser.html
# news_soup=soup(html,'html.parser')
# slide_elem = news_soup.select_one('ul.item_list li.slide')
# slide_elem.find('div',class_='content_title')
# news_title=slide_elem.find('div',class_='content_title').get_text()
# news_p=slide_elem.find('div',class_='article_teaser_body').get_text()
# print(news_p)


# ### JPL Space Images Featured Images

# #Visit url
# url='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
# browser.visit(url)

# # Find and click the full image button
# full_image_elem=browser.find_by_tag('button')[1]
# full_image_elem.click()

# # Parse the resulting html with soup
# html=browser.html
# img_soup=soup(html,'html.parser')

# # Find the relative image url
# img_url_rel=img_soup.find('img',class_='fancybox-image').get('src')

# #Use the base url to create an absolute url
# img_url=f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
# img_url

# ### Mars Facts

# #Scrape the table data from space-facts.com
# df=pd.read_html('https://space-facts.com/mars/')[0]
# df.columns=['description','value']
# df.set_index('description',inplace=True)
# df
# df.to_html

# #quit browser
# browser.quit()

