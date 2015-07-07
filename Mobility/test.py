from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("Inver Grove Heights")
print(location.address)
print(location.latitude)