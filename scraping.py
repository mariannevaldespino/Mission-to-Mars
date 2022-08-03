# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)
    news_title, news_paragraph= mars_news(browser)
    hemisphere_image_urls=hemisphere(browser)
    data={
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_image_urls,
        "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data

def mars_facts():
        try:
       df=pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    return df.to_html()


def hemisphere(browser):
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls = []
    imgs_links= browser.find_by_css("a.product-item h3")

    for x in range(len(imgs_links)):
        hemisphere={}
        browser.find_by_css("a.product-item h3")[x].click()
        sample_img= browser.find_link_by_text("Sample").first
        hemisphere['img_url']=sample_img['href']
        hemisphere['title']=browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    return hemisphere_image_urls

if __name__== "__main__":
    print(scrape_all())
