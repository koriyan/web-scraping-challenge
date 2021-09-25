# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import os

def scrape():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # NASA Mars News

    # Collect the latest News Title
    results = soup.find_all('div', class_="content_title")
    news_title = results[0].text
    news_title

    # Collect the latest Paragraph Text
    results = soup.find_all('div', class_="article_teaser_body")
    news_p = results[0].text
    news_p

    # JPL Mars Space Images - Featured Image

    # Use splinter to navigate the site
    base_url = 'https://spaceimages-mars.com/'
    browser.visit(base_url)

    # Click the full image button
    full_img = browser.find_by_tag('button')[1]
    full_img.click()

    # Parse the html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # Find the relative image url
    img_url = img_soup.find("img", class_ = "fancybox-image").get('src')
    img_url

    featured_image_url = base_url + img_url
    featured_image_url

    # Mars Facts

    # Use Pandas to scrape the table containing facts about Mars from Mars Facts webpage
    mars_facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(mars_facts_url)
    facts_df = tables[1]

    # Rename the table columns and set the Parameter as index
    facts_df.columns = ["Parameter", "Value"]
    facts_df.set_index("Parameter", inplace = True)
    facts_df

    # Use Pandas to convert the data to a HTML table string
    html_table = facts_df.to_html()
    html_table.replace('\n', '')
    print(html_table)

    # Mars Hemispheres

    # Use the browser to visit the astrogeology url
    hemispheres_url = "https://marshemispheres.com/"
    browser.visit(hemispheres_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    items = soup.find_all("div", class_="item")

    hemisphere_img_urls = []
    for item in items:
        title = item.find("h3").text
        hemisphere_url = "https://marshemispheres.com/" + item.find("a", class_="itemLink product-item")["href"]
        
        browser.visit(hemisphere_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        hemisphere_img_url = "https://marshemispheres.com/" + soup.find("img", class_="wide-image")["src"]
        hemisphere_img_urls.append({"title": title, "img_url": hemisphere_img_url})
    hemisphere_img_urls

    marspage = {}
    marspage["news_title"] = news_title
    marspage["news_p"] = news_p
    marspage["featured_image_url"] = featured_image_url
    marspage["html_table"] = html_table
    marspage["hemisphere_img_urls"] = hemisphere_img_urls

    return marspage