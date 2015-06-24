"""
combine walkability, transit and mobility score for each address
"""

from geopy.geocoders import Nominatim
from geolocation.google_maps import GoogleMaps
from walkscore.api import WalkScore, TransitScore
import json
metro_tran = '/Users/xshuai/Documents/Projects/accessibilityscore/Metro Transit Zip Code.csv'

address = "818 West 46th St, Minneapolis MN"   # sample user input
#address = "55123"
#address = "610 Opperman Dr, Eagan, MN"
#address = '1455 Upper 55th St E, Inver Grove Heights, MN 55077'
apiKey='ffd1c56f9abcf84872116b4cc2dfcf31'  # api key for walk/transit score

walkscore = WalkScore(apiKey)
#transitscore = TransitScore(apiKey)

### extract location information  ####
geolocator = Nominatim()
location = geolocator.geocode(address)
#print(location.raw)
google_maps = GoogleMaps(api_key='AIzaSyAP3JK8NPEfz8OTdYCGNgpv6wYCUsx4gf8')
google_location = google_maps.search(location=address)
#print(google_location.all()) # returns all locations.

my_location = google_location.first() # returns only first location.


code_city = {}
code_score = {}
with open(metro_tran, 'rU') as infile:
    for index, line in enumerate(infile):
        if index == 0:
            continue
        content = line.rstrip('\n').split(',')
        #print(content)
        primary_city = content[0]
        score = float(content[1])

        zip_code = content[2]
        code_score[zip_code] = score
	code_city[zip_code] = primary_city



city = my_location.city
state = 'MN'
long = float(location.longitude)
lat = float(location.latitude)
code = my_location.postal_code
print(my_location.city)
#print(my_location.route)
#print(my_location.street_number)
#print(my_location.postal_code)
print(city)
print(long)
print(lat)
print(code)
#### First, calculate walkscore #####
ws = walkscore.makeRequest(address, lat, long)['walkscore']
#print "walk score: ", ws

#### Second, calculate transit score ####
#ts = transitscore.makeRequest(city, state, lat, long)['transit_score']
#print "transit score: ", ts


#### Thrid, calculate metro availability score #####
ms = code_score[code] * 100



#### Finally, combine them and output as json file ####
final_score = 0.5 * ws + 0.5 * ms
print(final_score)





