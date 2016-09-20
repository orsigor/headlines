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


@app.route("/")
def get_news():
	query=request.args.get("publication")
	if not query or query.lower() not in RSS_FEEDS:
		publication="bbc"
	else:
		publication=query.lower()

	feed=feedparser.parse(RSS_FEEDS[publication])
	first_article=feed['entries'][0]
	return render_template("home.html",articles=feed['entries'])

if __name__=='__main__':
	app.run(host="172.16.0.58",port=5000,debug=True)
