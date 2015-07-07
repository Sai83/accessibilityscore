"""
This module contains function call to convert address/zipcode to geocode
"""

from geopy.geocoders import Nominatim

def geo_converter(place):
    """Place can be address/zip code/city name"""
    geolocator = Nominatim()
    location = geolocator.geocode(place)
    print(location)
    #city = location.raw['display_name'].split(',')[0]
    return location.latitude, location.longitude
#print(location.address)
#print(location.latitude)

if __name__ == '__main__':
    #place = '55123'
    #place = '610 Opperman Drive, Eagan, MN'
    #place = 'North St. Paul'
    #place = 'Eagan, MN'
    lat, lon = geo_converter(place)
    #print(lat)
    #print(lon)
    #print(city)
