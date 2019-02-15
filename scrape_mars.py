    import pandas
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    from selenium import webdriver
    import pandas as pd
    import time

def init_browser():
    executable_path = {"executable_path": "C:\webdrivers\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    articles = soup.find_all('li', class_='slide')
    news_data = {"title": [], "paragraph": []}

    for article in articles:

        news_data['title'].append(article.find('div', class_='content_title').get_text())
        news_data['paragraph'].append(article.find('div', class_='article_teaser_body').get_text())

    news_data

    news_title = news_data['title']
    news_p = news_data['paragraph']


    # JPL Mars Space Images - Featured Image

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)   
    time.sleep(1)

    xpath = '//footer//a[@class="button fancybox"]'

    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    html = browser.html
    soup = bs(html, 'html.parser')
    img_url = soup.find('a', class_="button fancybox")
    img_url = img_url['data-fancybox-href']
    root_url = "https://www.jpl.nasa.gov"
    featured_image_url = root_url + img_url
    featured_image_url


    # Mars Weather

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    tweets = soup.find_all('li', class_="js-stream-item")

    mars_weather = []
    for tweet in tweets:
        if tweet.div['data-screen-name'] == 'MarsWxReport':
            mars_weather.append(tweet.find(class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text())
    #     return mars_weather
            
    print(mars_weather[1])


    # Mars Facts


    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    facts = pd.read_html(facts_url)
    facts_table = pd.DataFrame(
                {'Category': facts[0][0], 
                'Data': facts[0][1]})
    html_facts_table = facts_table.to_html(index=False)
    html_facts_table


    # Mars Hemispheres

    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemis_root_url = "https://astrogeology.usgs.gov/"
    browser.visit(hemis_url)
    time.sleep(1)


    # Find xpaths for each hemisphere's link:

    #Cerberus
    #click to get enhanced image
    cer_xpath = '//div//h3'
    results = browser.find_by_xpath(cer_xpath)
    img = results[0]
    img.click()
    #find url
    html = browser.html
    soup = bs(html, 'html.parser')
    cer_url = soup.find('img', class_="wide-image")
    cer_url = cer_url['src']
    cer_url = hemis_root_url + cer_url
    cer_url
    time.sleep(1)

    #Valles Marineris 
    #click to get unenhanced image
    val_xpath = '//div[@class="sidebar"]//p'
    results = browser.find_by_xpath(val_xpath)
    img = results[0]
    img.click()
    #click to get enhanced image
    val_xpath = '//div[@class="sidebar"]//p'
    results = browser.find_by_xpath(val_xpath)
    img = results[0]
    img.click()
    #find url
    html = browser.html
    soup = bs(html, 'html.parser')
    val_url = soup.find('img', class_="wide-image")
    val_url = cer_url['src']
    val_url = hemis_root_url + val_url
    val_url
    time.sleep(1)

    # 3rd hemis
    #click to get unenhanced image
    syr_xpath = '//div[@class="sidebar"]//p'
    results = browser.find_by_xpath(syr_xpath)
    img = results[0]
    img.click()
    #click to get enhanced image
    syr_xpath = '//div[@class="sidebar"]//p'
    results = browser.find_by_xpath(syr_xpath)
    img = results[0]
    img.click()
    #find url
    html = browser.html
    soup = bs(html, 'html.parser')
    syr_url = soup.find('img', class_="wide-image")
    syr_url = syr_url['src']
    syr_url = hemis_root_url + syr_url
    syr_url
    time.sleep(1)

    # 4th hemis
    #click to get unenhanced image
    sch_xpath = '//div[@class="sidebar"]//p'
    results = browser.find_by_xpath(sch_xpath)
    img = results[0]
    img.click()
    #click to get enhanced image
    sch_xpath = '//div[@class="sidebar"]//p'
    results = browser.find_by_xpath(sch_xpath)
    img = results[0]
    img.click()
    #find url
    html = browser.html
    soup = bs(html, 'html.parser')
    sch_url = soup.find('img', class_="wide-image")
    sch_url = sch_url['src']
    sch_url = hemis_root_url + sch_url
    sch_url
    time.sleep(1)

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": val_url},
        {"title": "Cerberus Hemisphere", "img_url": cer_url},
        {"title": "Schiaparelli Hemisphere", "img_url": sch_url},
        {"title": "Syrtis Major Hemisphere", "img_url": syr_url},
    ]


    final_dict = {
        "news": news_data,
        "featured image": featured_image_url,
        "weather": mars_weather,
        "facts": html_facts_table,
        "mars hemispheres": hemisphere_image_urls
    }

    return final_dict
