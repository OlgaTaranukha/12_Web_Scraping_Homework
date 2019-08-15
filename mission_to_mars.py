#!/usr/bin/env python
# coding: utf-8

# ## Mission to MARS

# In[141]:


# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from selenium import webdriver
import pandas as pd
import time


# In[131]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
get_ipython().system('which chromedriver')


# In[132]:


# Windows initializing Splinter 
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)


# In[133]:


# Set Executable Path & Initialize Chrome Browser for Mac users
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News

# In[134]:


# Scrape the NASA Mars News Site https://mars.nasa.gov/news/ and collect the latest News Title and Paragraph Text. 
# URL of page to be scraped
url_news = 'https://mars.nasa.gov/news/'
browser.visit(url_news)


# In[135]:


# Create BeautifulSoup object; parse with 'html.parser'
html = browser.html
news_soup = BeautifulSoup(html, 'html.parser')

# Scrape the latest article title
news_title = news_soup.find('div', class_='content_title').text
news_title


# In[136]:


all_paragraphs = news_soup.find_all('div', class_='article_teaser_body')
all_paragraphs[0:5]


# In[137]:


# Scrape the first paragraph text of article teaser
news_p = all_paragraphs[1].text
news_p


# ## JPL Mars Space Images - Featured Image

# In[142]:


# Visit the url for JPL Featured Space Image https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars.
url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url_img)


# In[143]:


# Go to 'FULL IMAGE'
browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(2)


# In[144]:


# Go to 'more info'
browser.click_link_by_partial_text('more info')
time.sleep(2)


# In[145]:


# Create BeautifulSoup object and parse with 'html.parser'
html = browser.html
image_soup = BeautifulSoup(html, 'html.parser')


# In[146]:


# Scrape the URL for image
feat_img = image_soup.find('figure', class_='lede').a['href']
featured_image_url = f'https://www.jpl.nasa.gov{feat_img}'
featured_image_url


# ## Mars Weather

# In[147]:


# Visit the Mars Weather twitter account https://twitter.com/marswxreport?lang=en and 
# scrape the latest Mars weather tweet from the page. 
# URL of Mars Weather twitter page
url_weather = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url_weather)


# In[148]:


# Create BeautifulSoup object and parse with 'html.parser'
html = browser.html
weather_soup = BeautifulSoup(html, 'html.parser')


# In[149]:


# Scrape the latest info
mars_weather = weather_soup.find('p', class_='TweetTextSize').text
mars_weather


# ## Mars Facts

# In[150]:


# Visit the Mars Facts webpage https://space-facts.com/mars/ and 
# use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# Scrape the table of Mars facts
mars_url = 'https://space-facts.com/mars/'
tables = pd.read_html(mars_url)
tables


# In[151]:


mars_df = tables[0]
mars_df


# In[152]:


mars_df = mars_df[["Mars - Earth Comparison","Mars"]]
mars_df


# In[153]:


mars_df.columns = ['Property', 'Value']
mars_df.set_index('Property', inplace=True)
mars_df


# In[154]:


# Convert the data to a HTML table string.
html_table = mars_df.to_html(classes = 'html_table html_table-striped')
# strip unwanted newlines to clean up the table
html_table.replace('\n', '')
print(html_table)


# ## Mars Hemispheres

# In[158]:


# Visit the USGS Astrogeology site https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
# to obtain high resolution images for each of Mar's hemispheres
# URL of page to be scraped
url_hemis = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url_hemis)


# In[159]:


# Create BeautifulSoup object and parse with 'html.parser'
html = browser.html
hemis_soup = BeautifulSoup(html, 'html.parser')


# In[160]:


# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title
hemises = hemis_soup.find_all('h3')

# Append the dictionary with the image url string and the hemisphere title to a list.
hemis_dict = {}
hemisphere_image_urls = []

for hemis in hemises:
    hemis_dict["title"] = hemis.text.strip('Enhanced')
    
    # Click on the link with the corresponding hemis
    try:
        browser.click_link_by_partial_text(hemis.text)
    except ElementDoesNotExist:
        print(f"{hemis.text} Image doesn't exist")
    
    # Scrape the image url string 
    hemis_dict["img_url"] = browser.find_link_by_partial_href('download')['href']
      
    hemisphere_image_urls.append(hemis_dict)       
    
    browser.visit(url_hemis) 
    
print(hemisphere_image_urls)


# In[ ]:




