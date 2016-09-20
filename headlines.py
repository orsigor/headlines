### c0de55f11f07785ab018f79289b361ef
import json
import urllib2
import urllib
import feedparser
from flask import Flask,render_template, request

app=Flask(__name__)

RSS_FEEDS={'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
	   'cnn':'http://rss.cnn.com/rss/edition.rss',
	   'fox':'http://feeds.foxnews.com/foxnews/latest',
	   'iol':'http://www.iol.co.za/cmlink/1.640',
	   'cor':'http://xml.corriereobjects.it/rss/homepage.xml',
	   'mil':'http://xml.corriereobjects.it/rss/homepage_milano.xml',
	   'ans':'http://www.ansa.it/main/notizie/awnplus/topnews/synd/ansait_awnplus_topnews_medsynd_Today_Idx.xml',
	  }

DEFAULTS={
		'publication':'bbc',
		'city':'London,UK'
	}
@app.route("/")
def home():
	publication=request.args.get("publication")
	if not publication: 
		publication=DEFAULTS['publication']
	articles=get_news(publication)

	city=request.args.get('city')
	if not city:
		city=DEFAULTS['city']
	weather=get_weather(city)
	return render_template("home.html",articles=articles,weather=weather)

def get_news(query):
	if not query or query.lower() not in RSS_FEEDS:
		publication=DEFAULTS['publication']
	else:
		publication=query.lower()

	feed=feedparser.parse(RSS_FEEDS[publication])
	return feed['entries']

def get_weather(query):
	api_url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c0de55f11f07785ab018f79289b361ef'
	query=urllib.quote(query)
	url=api_url.format(query)
	data=urllib2.urlopen(url).read()
	parsed=json.loads(data)
	weather=None
	if parsed.get("weather"):
		weather={"description":parsed["weather"][0]["description"],
			 "temperature":parsed["main"]["temp"],
			 "city":parsed["name"]
			}
	return weather


if __name__=='__main__':
	app.run(host="172.16.0.58",port=5000,debug=True)
