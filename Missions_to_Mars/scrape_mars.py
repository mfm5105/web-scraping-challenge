from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time
import re
import requests

def init_browser():
     # Initiate headless driver for deployment
    executable_path={"executable_path": "chromedriver.exe"}
    return Browser("chrome",**executable_path,headless=True)
def scrape_all():
   # Run all scraping code (copied from jupyter notebook) and store in dictionary
    browser=init_browser()
    mars_data = {}

    # 1.......Get Mars news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    nasa_html=browser.html
    
    response=requests.get(url)
    nasa_soup=BeautifulSoup(response.text, 'html.parser')
    # update below variables
    # Print latest headlines
    news_title = nasa_soup.find("div",class_="content_title").text
    news_paragraph= nasa_soup.find("div", class_="rollover_description_inner").text
    print(f"Title is: {news_title}")
    print(f"Paragraph is: {news_paragraph}")
    mars_data["news_title"]=news_title
    mars_data["news_paragraph"]=news_paragraph
    # 2.......Get featured image
    #Site Navigation
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    response=requests.get(url)
    html=browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    # Find the more info button and click that
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()
    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()
    # Parse the resulting html with soup
    img_url = image_soup.select_one("figure.lede a img").get("src")
    img_url
    # Find the relative image url
    # Use Base URL to Create Absolute URL
    featured_image_url = f"https://www.jpl.nasa.gov{img_url}"
    print(featured_image_url)       

    mars_data["feature_image_url"]=featured_image_url
    # 3.......Get hemispheres
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Click the link, find the sample anchor, extract the href"
#Loop in list
hemi_dicts = []

for i in range(1,9,2):
    hemi_dict = {}
    browser.visit(url_hemisphere)
    time.sleep(1)
    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
    hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
    hemi_name = hemi_name_links[i].text.strip('Enhanced')
    
    detail = browser.find_by_css('a.product-item')
    detail[i].click()
    time.sleep(1)
    browser.find_link_by_text('Sample').first.click()
    time.sleep(1)
    browser.windows.current = browser.windows[-1]
    hemi_img_html = browser.html
    browser.windows.current = browser.windows[0]
    browser.windows[-1].close()
    
    hemi_img_soup = BeautifulSoup(hemi_img_html, 'html.parser')
    hemisphere_image_urls = hemi_img_soup.find('img')['src']

    print(hemi_name)
    hemi_dict['title'] = hemi_name.strip()
    
    print(hemisphere_image_urls)
    hemi_dict['img_url'] = hemi_img_path

    hemi_dicts.append(hemi_dict)

mars_data["hemisphere_imgs"]=hemi_dicts

    # 4.......Get twitter weather
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
url = "https://twitter.com/marswxreport?lang=en"
browser.visit(url)
mars_html=browser.html
mars_weather_soup=BeautifulSoup(mars_html,'html.parser')
#Pause for 5 seconds to let the Twitter page load before extracting the html
time.sleep(5)

    # First, find a tweet with the data-name `Mars Weather`
pattern = re.compile(r'sol')
mars_weather =mars_weather_soup.find('span', text=pattern).text
print(mars_weather)
    # Next, search within the tweet for the p tag or span tag containing the tweet text
    # As Twitter is frequently making changes the try/except will identify the tweet
    # text using a regular expression pattern that includes the string 'sol' if there
    # is no p tag with a class of 'tweet-text'
mars_data["weather_tweet"]=mars_weather

    # 5........Get mars facts
mars_df = pd.read_html("https://space-facts.com/mars/")[0]
print(mars_df)
    #use pd.read_html and df.to_html
mars_df.columns=["Description", "Value"]
mars_df.set_index("Description", inplace=True)
mars_df

    # Stop webdriver and return data
browser.quit()

return mars_data
    # End Function

 
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
