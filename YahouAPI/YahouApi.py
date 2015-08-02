__author__ = 'Maxime'

import urllib2, urllib, json

class YahouRestApiRequest:
    base_url = "http://query.yahooapis.com/v1/public/yql?"

    def encodequery(self, query):
        print query
        print self.base_url + urllib.urlencode({'q':query}) + "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
        return self.base_url + urllib.urlencode({'q':query}) + "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"

class RequestQuoteFirms(YahouRestApiRequest):
    firmscode = []
    quote_query = "select * from yahoo.finance.quote where symbol in "

    query = ''

    def __init__(self, firmscode):
        self.firmscode = firmscode

    def createquery(self):
        firmsquery = "("

        for f in self.firmscode:
            firmsquery += '"' + f + '.PA'+'",'

        firmsquery = firmsquery[:-1]
        firmsquery += ")"

        self.query = self.quote_query + firmsquery
        return self.query

    def getall(self):
        self.createquery()

        result = urllib2.urlopen(self.encodequery(self.query)).read()
        data = json.loads(result)
        self.data = data['query']['results']['quote']
        return self.data





