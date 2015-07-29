"""
Compute the walkability score of a city
"""
import pandas as pd
from walkscore import WalkScore
import time

city_file = '../Census_data/city_pop.csv'
cities = pd.read_csv(city_file, sep='\t')
cities.set_index('id', inplace=True)
apiKey='ffd1c56f9abcf84872116b4cc2dfcf31'
walkscore = WalkScore(apiKey)

ctu_file = '../Geolocation/CTU_ref.csv'
ctu_city = pd.read_csv(ctu_file, sep='\t')
quote = 0
city_ws = []
city_county = {}
county_cities = {}
for index, row in ctu_city.iterrows():
    ctu_type = row['CTU_TYPE']
    city = row['FEATURE_NAME']
    lat = row['LATITUDE']
    lng = row['LONGITUDE']
    code = row['CENSUS_CODE']
    county = row['COUNTY_NAME']
    city = city.replace('Saint', 'St')
    county = county.replace('Saint', 'St')
    if code in cities.index and 'historical' not in city:
        if city not in city_county:  #only consider the main county
            city_county[city] = county
        else:
            continue
        
        if county in county_cities:
            county_cities[county].append(city)
        else:
            county_cities[county] = [city]
        ws = walkscore.get_score('', lat, lng)
        if ws:
            city_ws.append({'city':city, 'county':county, 'walkscore':ws})
        else:
            city_ws.append({'city':city, 'county':county, 'walkscore':0})
        quote += 1
        if not (quote % 30):
            print(quote, 'needs to wait for a minute')
            time.sleep(60)
            #exit(1)


city_walk_score = 'city_walkscore.csv'
city_ws = pd.DataFrame(city_ws)
city_ws.to_csv(city_walk_score, index=False)

city_county_map = '../Geolocation/city_county.csv'
city_county = pd.Series(city_county, name='county')
city_county.to_csv(city_county_map, index_label='city', header=True)

county_cities_map = '../Geolocation/county_cities.csv'
county_cities = pd.Series(county_cities, name='cites')
county_cities.to_csv(county_cities_map, sep='\t', index_label='county', header=True)

        
        
    


