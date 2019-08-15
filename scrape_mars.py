# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from selenium import webdriver
import pandas as pd
import time



def scrape():

    # Set Executable Path & Initialize Chrome Browser for Mac userser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    # Windows initializing Splinter 
    #executable_path = {'executable_path': 'chromedriver.exe'}
    #browser = Browser('chrome', **executable_path, headless=True)
    

    # Scrape the NASA Mars News Site https://mars.nasa.gov/news/ and collect the 
    # latest News Title and Paragraph Text. 
    news_title, news_p = mars_news(browser)
    
    # Run the functions below and store into a dictionary
    results = {
        "title": news_title,
        "paragraph": news_p,
        "image_URL": jpl_image(browser),
        "weather": mars_weather(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemis(browser),
    }

    # Quit the browser and return the scraped results
    browser.quit()
    return results

def mars_news(browser):
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Scrape the latest article title
    news_title = news_soup.find('div', class_='content_title').text
    # Scrape all the paragraphs
    all_paragraphs = news_soup.find_all('div', class_='article_teaser_body')
    # get the second one
    news_p = all_paragraphs[1].text
    #news_p = news_soup.find('div', class_='article_teaser_body').text
    return news_title, news_p

def jpl_image(browser):
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)

    # Go to 'FULL IMAGE', then to 'more info'
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)

    # Create BeautifulSoup object and parse with 'html.parser'
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    # Scrape the URL for image
    feat_img = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{feat_img}'
    return featured_image_url

def mars_weather(browser):
    # Visit the Mars Weather twitter account https://twitter.com/marswxreport?lang=en and 
    # scrape the latest Mars weather tweet from the page. 
    # URL of Mars Weather twitter page
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')
    
    # Scrape the latest info and return
    mars_weather = weather_soup.find('p', class_='TweetTextSize').text
    return mars_weather
    
def mars_facts():
    # Visit the Mars Facts webpage https://space-facts.com/mars/ and 
    # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Scrape the table of Mars facts
    mars_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_url)
    mars_df = tables[0]
    mars_df = mars_df[["Mars - Earth Comparison","Mars"]]
    mars_df.columns = ['Property', 'Value']

    # Set index to property in preparation for import into MongoDB
    mars_df.set_index('Property', inplace=True)
    
    # Convert to HTML table string and return
    html_table = mars_df.to_html(classes = 'html_table html_table-striped')
    html_table.replace('\n', '')
    return html_table
    
def mars_hemis(browser):
    # Visit the USGS Astrogeology site https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    # to obtain high resolution images for each of Mar's hemispheres
    # URL of page to be scraped
    url_hemis = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemis)
    
    html = browser.html
    hemis_soup = BeautifulSoup(html, 'html.parser')

    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title
    hemises = hemis_soup.find_all('h3')
     
    # Append the dictionary with the image url string and the hemisphere title to a list.
    # Initialize a dictionary for the hemisphere
    hemis_dict = {}
    # Initialize hemisphere_image_urls list
    hemisphere_image_urls = []

    # Loop through the hemisphere links to obtain the images
    for hemis in hemises:     
        hemis_dict["title"] = hemis.text.strip('Enhanced')

        # Click on the link with the corresponding text
        browser.click_link_by_partial_text(hemis.text)
        
        # Scrape the image url string and store into the dictionary
        hemis_dict["img_url"] = browser.find_link_by_partial_href('download')['href']
        
        # Add the dictionary to hemisphere_image_urls
        hemisphere_image_urls.append(hemis_dict)
    
        browser.visit(url_hemis) 
    
    return hemisphere_image_urls