# reada = gae for covert text to markdown using readability
# by truong hoang nguyen
# free to used
# demo at meomappp.appspot.com
import json
import urllib2

import basehandler
from google.appengine.api import memcache
from readability.readability import Document
import webapp2

# webapp2 config
app_config = {
	'webapp2_extras.sessions': {
		'cookie_name': 'mm_sess',
		'cookie_args': {'max_age': 7257600}, # 12w = 4month 60*60*24*7*12
		'secret_key': 'SESSION_KEY'
	},
	'webapp2_extras.auth': {
		'token_max_age':   9257600,
		'token_new_age':   6257600,
		'token_cache_age': 7257600,
	}
}


def short_url(url):
	"""
	return
	{
	 "kind": "urlshortener#url",
	 "id": "http://goo.gl/1kRJrU",
	 "longUrl": "https://github.com/avelino/django-googl/blob/master/googl/short.py"
	}
	"""
	api_url = "https://www.googleapis.com/urlshortener/v1/url"
	header = {"Content-Type": "application/json"}
	params = {"longUrl": url}

	try:
		response = urllib2.urlopen(urllib2.Request(
								   api_url, json.dumps(params), header))
	except urllib2.URLError, urllib2.HTTPError:
		return u""

	json_data = response.read()

	return json_data

def to_long_url(short_url):
	"""
	{
		kind: "urlshortener#url"
		id: "http://goo.gl/2GQJM3"
		longUrl: "https://www.google.com.vn/search?...."
		status: "OK"
		}
	"""
	url = 'https://www.googleapis.com/urlshortener/v1/url?shortUrl=' + short_url;
	try:
		response = urllib2.urlopen(urllib2.Request(url))
		json_data = json.loads(response.read())
		return json_data.get('longUrl')
	except urllib2.URLError, urllib2.HTTPError:
		return u""


################################################################################
import html2text

def reada(url, cache=True):

	if cache:
		cached = memcache.get(key=url)
		if cached is not None:
			return cached

	#file = urllib.urlopen(url)
        #import urllib2
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        file = opener.open(url)
        ##
	enc = 'utf-8'
	text = ''
	try:
		# 1, web html 2 readability
		raw = Document(file.read(), url=url)
		html = raw.summary().encode(enc, 'replace')
		title = raw.short_title()

		# 2, readability 2 markdown, copy from main
		data = html.decode(enc)
		h = html2text.HTML2Text(baseurl=url)
		h.ignore_images = False
		h.body_width = 100000
		text = h.handle(data)
	finally:
		file.close()

	d = {'url': url, 'title': title, 'content': text}
	if cache:
		memcache.add(key=url, value=d, time=600)
	return d

class ParseHtml(basehandler.BaseHandler):
	def get(self):
		"""
		1. from browser request /url=url -> render page
		2. from bot request /url=url&json=true
		"""
		url = self.request.params.get('url')
		if url is None:
			self.render_template('index.html')
			return
		d = reada(url)
		if self.request.params.get('json') is not None:
			cb = self.request.params.get('callback')
			if cb is not None:
				self.response.out.write(cb + "(" + json.dumps(d) + ")")
			else:
				self.response.out.write(json.dumps(d))
		else:
			params = d
			self.render_template('index.html', ** params)

#app = ndb.toplevel(WSGIApplication(routes, config=app_config, debug=True))
app = webapp2.WSGIApplication([
							  ('/', ParseHtml),
							  ('/sign', ParseHtml)],
							  config=app_config,
							  debug=True)
