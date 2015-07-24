"""
Compute a walk score of each census tract
"""
from walkscore import WalkScore
import geocoder
import time
import pandas as pd

census_dat = "../Geolocation/mn_tracts.csv"
census_walk_score = 'tracts_walk_score2.csv'
apiKey='ffd1c56f9abcf84872116b4cc2dfcf31'
walkscore = WalkScore(apiKey)

census = pd.read_csv(census_dat)
start_index = 700
#print(census)

census_walk = []
for index, row in census.iterrows():
    if index < start_index:
        continue
    id = row['geoid']
    lat = row['lat']
    long = row['long']
    info = {'geoid':id}
    # first, extract address, city, county and zipcode #
    g = geocoder.reverse((lat, long))
    #print(g.json)
    #print(g.city)
    #print(g.county)
    #print(g.postal)
    #print(g.address)
    try:
        info['city'] = g.city
    except:
        print ("no city found")
        info['city'] = ''
    try:
        info['county'] = g.county.replace('County', '').strip()
    except:
        print (id, "no county found")
        info['county'] = ''
    try:
        info['zipcode'] = g.postal
    except:
        print ("no zipcode found")
        info['zipcode'] = ''
    try:
        info['street'] = g.street
    except:
        print ("no street found")
        info['street'] = ''
    
    ws = walkscore.get_score(g.address, lat, long)
    if ws:
        info['walkscore'] = ws
    else:
        info['walkscore'] = 0

    census_walk.append(info)

    #if index + 1 == 40:
    #    break

    if not ((index+1) % 20):
        print(index+1,'needs to wait for a minute')
        time.sleep(60)

    if index+1 == 1000:  # every time only parse 700 records
        break

    

census_walk = pd.DataFrame(census_walk)
#print(census_walk)
census_walk.to_csv(census_walk_score, sep='\t', index=False,
                   columns=['geoid','street', 'city', 'county', 'zipcode', 'walkscore'],
                   float_format='%.0f')
    
    
    
    

