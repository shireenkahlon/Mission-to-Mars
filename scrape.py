# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import random
import time

executable_path={'executable_path':'/usr/local/bin/chromedriver'}
browser=Browser('chrome',**executable_path,headless=True)
def scrape_all():
    # Initiate headless driver for deployment
    executable_path={'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        'hemispheres': hemisphere_data(browser)
    }
    # Stop webdriver and return data
    browser.quit()
    return data

### scrape mars news

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    #  Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add try/except for error handling
       # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

### scrape featured image

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    return img_url

### scrape mars facts table

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

### scrape hemisphere data


def hemisphere_data(browser):
    url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
    browser.visit(url)
    #Create list for hemisphere_image_urls 
    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item img')
    #loop the site to scrape title and image url
    for i in range(len(links)):
        html=browser.html
        mars_soup=soup(html,'html.parser')
        hemisphere = {}
        browser.find_by_css('a.product-item img')[i].click()
        # find the Sample image anchor tag - extract href
        try:
            sample_elem = browser.links.find_by_text('Sample').first
            hemisphere['img_url'] = sample_elem['href']
            # get Hemisphere title
            hemisphere['title'] = browser.find_by_css('h2.title').text
            # Append hemisphere_image_urls object
            hemisphere_image_urls.append(hemisphere)
        except AttributeError:
            return None
        rand_num = random.randint(2,7)
        time.sleep(rand_num)
        # navigate backwards
        browser.back()
    browser.quit()
    return hemisphere_image_urls
# If running as script, print scraped data
if __name__ == "__main__":
    print(scrape_all())

