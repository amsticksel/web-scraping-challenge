    #!/usr/bin/env python
    # coding: utf-8

    # In[1]:


    #import dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pymongo

def scrape_info():
    # ### NASA Mars News

    # In[2]:


    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'


    # In[3]:


    # Retrieve page with the requests module
    response = requests.get(url)


    # In[4]:


    # Examine the results, then determine element that contains sought info
    soup = bs(response.text, 'html.parser')


    # In[5]:


    titles = soup.find_all('div', class_="content_title")
    descs = soup.find_all('div', class_="rollover_description_inner")


    # In[6]:


    # Print all ten headlines
    headings = soup.find_all('div', class_="content_title")
    # A blank list to hold the headlines
    headlines = []
    # Loop over td elements
    for heading in headings:
        # If td element has an anchor...
        headlines.append(heading.a.get_text(strip=True))                  
                

    descs = soup.find_all('div', class_="rollover_description_inner")
    # A blank list to hold the headlines
    descriptions = []
    # Loop over td elements
    for desc in descs:
        # If td element has an anchor...
            descriptions.append(desc.get_text(strip=True))


    # In[7]:


    print(headlines, descriptions)


    # ### JPL Mars Space Images - Featured Image

    # In[8]:


    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)


    # In[9]:


    response = requests.get(url2)
    soup = bs(response.text, 'html.parser')


    # In[ ]:





    # In[10]:


    big_images = soup.find_all('li', class_='slide')# A blank list to hold the headlines
    featured_image_url = []


    for big_image in big_images:
        try:
            featured_image_url.append(f"https://www.jpl.nasa.gov{big_image.a['data-fancybox-href']}")
        except:
            print("Scraping Complete! :)")


    # In[11]:


    featured_image_url


    # ### Mars Weather

    # In[12]:


    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)


    # In[13]:


    response3 = requests.get(url3)
    soup3 = bs(response3.text, 'html.parser')

    weather_updates=[]
    tweet_times=[]
    weather_tweets = soup3.find_all('div', class_='js-tweet-text-container')# A blank list to hold the headlines
    weather_times = soup3.find_all('span', class_='_timestamp')# A blank list to hold the headlines


    for tweet in weather_tweets:
        try:
            weather_updates.append(tweet.p.get_text(strip=True))
            tweet.a.extract()
        except:
            print("Scraping Complete! :)")
            
    for time in weather_times:
        try:
            tweet_times.append(time.get('data-time-ms'))
        except:
            print("Scraping Complete! :)")
            
    print(tweet_times)
    print(weather_updates)


    # In[14]:



    with open('twitterinfo.txt', 'w', encoding='utf-8') as f_out:
        f_out.write(soup3.prettify())


    # In[15]:


    len(weather_tweets)


    # ### Mars Facts

    # In[16]:


    url="https://space-facts.com/mars/"
    tables = pd.read_html(url)
    tables
    mars_df=tables[1]


    # In[17]:


    mars_df.to_html('mars_data.html',index=False)


    # ### Mars Hemispheres

    # In[18]:


    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url4="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)


    # In[19]:


    response4 = requests.get(url4)
    soup4 = bs(response4.text, 'html.parser')
    with open('astrogeology2-html.txt', 'w', encoding='utf-8') as f_out:
        f_out.write(soup4.prettify())


    # In[20]:


    import re
    links = []
    img_alt = []
    image_alts=[]
    for link in soup4.findAll('a',href=re.compile("enhanced")):
        try:
            links.append(link.get('href'))
            print(links)
        except:
            print("Scraping Complete! :)")
            
    for name in soup4.findAll('img',alt=re.compile("Enhanced")):
        try:
            img_alt.append(name.get('alt'))
            for i in img_alt:
                i.replace(' Enhanced thumbnail', '')
        except:
            print("Scraping Complete! :)")  
    print(img_alt)
    for img in img_alt:
        img2 = img.replace(" Enhanced thumbnail",'')
        image_alts.append(img2)
        
    print(image_alts)


    # In[21]:


    final_links=[]

    for link in links:
        final_links.append(f"https://astrogeology.usgs.gov{link}")
    final_links


    # In[25]:


    fullsize_image=[]
    for link in final_links:
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
    #     browser.visit(link)
        response5 = requests.get(link)
        soup5 = bs(response5.text, 'html.parser')
        
        for image in soup5.find_all('a',href=re.compile("full.jpg")):
            try:
                fullsize_image.append(image.get('href'))
            except:
                print("Scraping Complete! :)")

    print(fullsize_image)


    # In[53]:


    hemisphere_image_urls = [{'title': a, 'img_url': f} for a, f in zip(image_alts, fullsize_image)]
    print(hemisphere_image_urls)


    # In[55]:


    ### Mars News
    print(headlines, descriptions)


    # In[56]:



    ### JPL Mars Space Images - Featured Image
    featured_image_url


    # In[57]:


    ### Mars Weather
    print(tweet_times)
    print(weather_updates)


    # In[58]:


    ### Mars Facts
    mars_df.to_html('mars_data.html',index=False)
    mars_df


    # In[59]:


    ### Mars Hemisphere
    hemisphere_image_urls = [{'title': a, 'img_url': f} for a, f in zip(image_alts, fullsize_image)]
    print(hemisphere_image_urls)


    # In[ ]:

    mars_data = {
        {"mars_news": headlines, descriptions},
        "mars_image": featured_image_url,
        {"mars_tweets": weather_updates, tweet_times},
        "mars_hemispheres": hemisphere_image_urls
    }

    return mars_data
