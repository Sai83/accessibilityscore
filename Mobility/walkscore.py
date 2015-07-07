"""
This module contains function call to retrieve walk/transit score
"""

import urllib.request, urllib.parse
import ast

class WalkScore:
    """This class request walk score API"""
    api_url = 'http://api.walkscore.com/score?' # class attribute

    def __init__(self, apiKey, format="json"):
        """Initiate the request"""
        self.apiKey = apiKey
        self.format = format

    def get_score(self, address, lat, long):
        """Given an address/zipcode with latitude and longitude, return the walk score"""
        args = {'lat': lat, 'lon': long, 'address': address, 'format': self.format, 'wsapikey': self.apiKey}
        args = urllib.parse.urlencode(args)
        req_url = self.api_url + args
        #req = urllib.request.urlopen(req_url)

        # send request to walk score server #
        try:
            req = urllib.request.urlopen(req_url)
        except:
            print("Http request error!")
            return None

        res = req.read()
        res = ast.literal_eval(res.decode('utf-8'))

        # deal with different status #
        status = res['status']
        if status != 1:
            if status == 2:
                descr = 'Score is being calculated and is not currently available.'
            elif status == 40:
                descr = 'Your WSAPIKEY is invalid.'
            elif status == 41:
                descr = 'Your daily API quota has been exceeded.'
            elif status == 42:
                descr = 'Your IP address has been blocked.'
            else:
                descr = 'Unknown'
            print(descr)
            return None
        else:
            return res['walkscore']


if __name__ == "__main__":
    apiKey='ffd1c56f9abcf84872116b4cc2dfcf31'
    walkscore = WalkScore(apiKey)
    address=''
    lat = 47.6085
    long= -122.3295
    ws = walkscore.get_score(address, lat, long)
    print(ws)



