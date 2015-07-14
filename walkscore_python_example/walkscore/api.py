##try:
##    import urllib.request as urllib2
##except ImportError:
##    import urllib2
import urllib, urllib2

try:
    import simplejson as json
except ImportError:
    import json

"""
Error handler
"""
class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib2.HTTPError(
            req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result

class InvalidApiKeyException(Exception):
    pass

class InvalidLatLongException(Exception):
    pass

class WalkScore:
    apiUrl = 'http://api.walkscore.com/score?format'

    def __init__(self, apiKey, format = 'json'):
        self.apiKey = apiKey
        self.format = format

    def makeRequest(self, address, lat = '', long = ''):
        url = '%s=%s&%s&lat=%s&lon=%s&wsapikey=%s' % (self.apiUrl, self.format, address, lat, long, self.apiKey)
        print(url)
        request = urllib2.Request(url)
##        print(request)
        opener = urllib2.build_opener(DefaultErrorHandler())
##        first = opener.open(request)
##
##        first_datastream = first.read()
##
##        # Append caching headers
##        request.add_header('If-None-Match', first.headers.get('ETag'))
##        request.add_header('If-Modified-Since', first.headers.get('Date'))

        response = opener.open(request)
        print(response)

        # some error handling
        responseStatusCode = response.getcode()

        # jsonify response
        jsonResp = json.load(response)
        jsonRespStatusCode = jsonResp['status']

        if responseStatusCode == 200 and jsonRespStatusCode == 40:
            raise InvalidApiKeyException

        if responseStatusCode == 404 and jsonRespStatusCode == 30:
            raise InvalidLatLongException

        return jsonResp

class TransitScore:
    apiUrl = 'http://transit.walkscore.com/transit/score/?'

    def __init__(self, apiKey):
        self.apiKey = apiKey
        #self.format = format

    def makeRequest(self, city, state, lat = '', long = ''):
        url = '%s&lat=%s&lon=%s&%s&wsapikey=%s' % (self.apiUrl, lat, long, urllib.urlencode({'city': city, 'state': state}), self.apiKey)
        request = urllib2.Request(url)
        opener = urllib2.build_opener(DefaultErrorHandler())
        first = opener.open(request)

        first_datastream = first.read()
        # Append caching headers
        request.add_header('If-None-Match', first.headers.get('ETag'))
        request.add_header('If-Modified-Since', first.headers.get('Date'))

        response = opener.open(request)
        # some error handling
        responseStatusCode = response.getcode()

        # jsonify response
        jsonResp = json.load(response)
 

        return jsonResp
