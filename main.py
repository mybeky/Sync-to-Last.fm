#!/usr/bin/env python

import urllib, urllib2, time
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import taskqueue

import xml.etree.ElementTree as ET
import md5
import logging

url = 'http://www.xiami.com/widget/xml-dynamic/uid/435580/id/435580/type/shuffle'

def scrobble(title, artist, ts):
    url = 'http://ws.audioscrobbler.com/2.0/'
    api_key = 'ebd2a16df68496b34da760f2eff69d64'
    secret = 'c36527186f7aca092a8795fc2047e42b'
    sk = '827f381b9154c79b81a9d345f6211b2b'

    params = {
        'track[0]': title,
        'artist[0]': artist,
        'timestamp[0]': ts,
        'api_key': 'ebd2a16df68496b34da760f2eff69d64',
        'method': 'track.scrobble',
        'sk': sk
    } 
    s = ''.join([x + str(params[x]) for x in sorted(data.keys())])
    s += secret
    params['api_sig'] = md5.new(s).hexdigest()

    result = urlfetch.fetch(url=url, 
                            payload=urllib.urlencode(params), 
                            method=urlfetch.POST).content


class Track(db.Model):
    title = db.StringProperty(required=True)
    artist = db.StringProperty(required=True)
    album = db.StringProperty()
    source = db.StringProperty()
    ts = db.DateTimeProperty()


class MainHandler(webapp.RequestHandler):
    def get(self):
        res = urllib.urlopen(url).read()
        xml = ET.XML(res)
        response = '<ul>'
        for track in xml.findall('trackList/track'):
            title = track.find('song_name').text
            artist = track.find('artist_name').text
            response += '<li>%s - %s</li>' % (title, artist)
            scrobbler.submit(artist, title,
                             int(time.mktime(time.localtime())),
                             rating='L',
                             length=335,
                             autoflush=True)
            break
        #scrobbler.flush()
        response += '</ul>'
        self.response.out.write(response)


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
