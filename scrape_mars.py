from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import pymongo
import requests


from flask import Flask,render_template,jsonify

app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.z4nvb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority") #User your mongo details
db = client.test # Your Db Name

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

@app.route("/")
def index():
    obj = db.c1.find({"key": "SINGLE"})[0]
    return render_template("index.html",
        obj=obj
    )
@app.route("/scrape")
def scrape():
    obj = scrapeall()
    db.c1.delete_one({"key":"SINGLE"}) # Here c1 is collection name
    db.c1.insert_one(obj)
    return """DONE"""


def scrapeall():
    table = getTable()
    featuredImageURL = getFeaturedImage()
    marsHemispheresList = marsHemispheres()
    obj = {"key":"SINGLE"}
    obj['table'] = table
    obj['featuredImageURL'] = featuredImageURL
    obj['marsHemispheres'] = marsHemispheresList
    return obj

def getTitle():
    browser.visit("https://redplanetscience.com/")
    html= browser.html
    soup = bs(html,'html.parser')
    news_title = soup.find_all('div',class_ ='content_title')[0].text
    news_para = soup.find_all('div',class_='article_teaser_body')[0].text
    obj = {
        "title":news_title,
        "para":news_para,
    }
    return obj

def getFeaturedImage():
    url='https://spaceimages-mars.com'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    link=soup.find('img',class_='headerimage fade-in')['src']
    return (url+"/"+link)
    

def getTable():
    url = 'https://galaxyfacts-mars.com'
    tables=pd.read_html(url)
    df=tables[0]
    df.columns = ['description','Mars','Earth']
    df.set_index('description',inplace=True)
    tableList = []
    for row in df.itertuples():
        obj ={
            "index":row[0],
            "Mars":row[1],
            "Earth":row[2]
        }
        tableList.append(obj)
    return tableList

def marsHemispheres():
    mlist = []
    mlist.append(cerberus())
    mlist.append(valles_marineris())
    mlist.append(schiaparelli())
    mlist.append(syrtis_major())
    return mlist

def cerberus():
    
    url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced')

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    cerberus_img= soup.find_all('div',class_="wide-image-wrapper")
    full_img = None

    for img in cerberus_img:
        pic = img.find('li')
        full_img = pic.find('a')['href']


    cerberus_title = soup.find('h2', class_='title').text

    return {"title": cerberus_title, "url": full_img}

def valles_marineris():
    
    url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced')

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    cerberus_img= soup.find_all('div',class_="wide-image-wrapper")
    full_img = None

    for img in cerberus_img:
        pic = img.find('li')
        full_img = pic.find('a')['href']


    valles_marineris_title = soup.find('h2', class_='title').text

    return {"title": valles_marineris_title, "url": full_img}

def schiaparelli():
    
    url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced')

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    cerberus_img= soup.find_all('div',class_="wide-image-wrapper")
    full_img = None

    for img in cerberus_img:
        pic = img.find('li')
        full_img = pic.find('a')['href']


    schiaparelli = soup.find('h2', class_='title').text

    return {"title": schiaparelli, "url": full_img}

def syrtis_major():
    
    url = ('https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced')

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    cerberus_img= soup.find_all('div',class_="wide-image-wrapper")
    full_img = None

    for img in cerberus_img:
        pic = img.find('li')
        full_img = pic.find('a')['href']


    syrtis_major = soup.find('h2', class_='title').text

    return {"title": syrtis_major, "url": full_img}

if __name__ == '__main__':
    app.run(debug=True,port=5000)