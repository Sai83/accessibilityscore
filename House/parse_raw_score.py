"""
parse house raw score
"""
import pandas as pd
import math
#from geopy.geocoders import Nominatim
import time
import geocoder

house_raw_score_file = 's8house_raw_score.txt'
house_refiend_score_file = 's8house_ref_score.csv'
house_interp_score_file = 's8house_interp_score.csv'

types = {"Low Income", "Elderly", "Disabled", "Rural"}
#geolocator = Nominatim()
quote = 0
def parse_raw_score(raw_file, refine_file, interplate=False, parse_location=False):
    """Parse the raw house score file"""
    global quote
    house_info_list = []
    with open(raw_file, 'rU') as infile:
        for index, line in enumerate(infile):
            line = line.rstrip('\n')
            content = line.split()
            if 'user review' in line:
                continue
            elif 'Add to Compare' in line:  # skip
                continue
            elif 'out of ' in line:  # skip
                continue
            if len(content) > 1 and content[0].isdigit():  # this is an address
                #house_info_list.append(house_info)
                #house_info = {'elderly':False, 'disabled':False}  # new property appears
                house_info['address'] = line
                    
            elif ', Minnesota' in line: # this is city name
                city = line.split(',')[0]
                if 'Saint' in city:
                    city = city.replace('Saint', 'St')
                house_info['city'] = city
                if parse_location:
                    if quote == 20:
                        print("needs to wait for a minute")
                        time.sleep(60) #
                        quote = 0
                    quote += 1
                    place = house_info['address'] + ', ' + house_info['city']+', MN' 
                    #location = geolocator.geocode(place)
                    location = geocoder.google(place)
                    address = location.address
                    if not address: # return none from google
                        print('query yahoo...')
                        location = geocoder.yahoo(place)
                        address = location.address
                    else:
                        print('query google...')
                    if not address:  # does not return anything
                        print (line)
                        exit(1)
                    county = location.county.replace('County', '').strip()
                    zipcode = address.split(',')[-2].split()[-1]
                    house_info['county'] = county
                    house_info['zipcode'] = zipcode
                    house_info['lat'] = location.lat
                    house_info['lng'] = location.lng
                    
            elif line.isdigit():  # hud score
                house_info['hud_score'] = int(line)
            elif len(line) == 3 and line[1] == '.': # value rating
                house_info['value_rating'] = float(line)
            elif line in types:
                if line == 'Elderly':
                    house_info['elderly'] = True
                elif line == 'Disabled':
                    house_info['disabled'] = True
            else: # this is the property name
                if index > 0:  # skip header
                    house_info_list.append(house_info)
                house_info = {'elderly':False, 'disabled':False, 'name':line}
                if line == 'Prairie View Heights':
                    house_info['hud_score'] = 84
                elif line == 'Riverview Apartments Senior Housing':
                    house_info['hud_score'] = 85
                elif line == 'The Meadows Of Oxboro':
                    house_info['hud_score'] = 80
                elif line == 'Mercy Manor II':
                    house_info['hud_score'] = 92
                    house_info['value_rating'] = 4.6
                elif line == 'Kingsley Commons':
                    house_info['hud_score'] = 92
                elif line == 'Burke Apartments':
                    house_info['hud_score'] = 96
                elif line == 'Carty Heights':
                    house_info['hud_score'] = 69
                    #except:
                    #    print(place)
                        #exit(1)
            
    house_info_list.append(house_info) # record the last 
    house_info_list = pd.DataFrame(house_info_list)

    #house_info_list['hud_score'] = house_info_list['hud_score'].map(lambda x:'%.0f' % x)
    if interplate:
        city_group = house_info_list.groupby('city')
        
        city_mean = city_group.mean()
        #print(city_mean)

        hud_group = house_info_list.groupby('hud_score')
        hud_mean = hud_group.mean()
        #print(hud_mean)

        for index, row in house_info_list.iterrows():
            hud_score = row['hud_score']
            rating = row['value_rating']
            city = row['city']
            if math.isnan(hud_score):
                hud_score = int(city_mean.ix[city, 'hud_score'])
                house_info_list.ix[index, 'hud_score'] = hud_score
                row['hud_score'] = hud_score
            if math.isnan(rating):
                rating = hud_mean.ix[hud_score, 'value_rating']
                if math.isnan(rating):
                    house_info_list.ix[index, 'value_rating'] = 3.5
                else:
                    house_info_list.ix[index, 'value_rating'] = rating
        #print(hud_mean)

        
##        for city, group in city_group:
##            print(city)
##            print(group)
##            exit(1)

    house_info_list['hud_score'] = house_info_list['hud_score'].map(lambda x:'%.0f' % x)
    #print(house_info_list)
    house_info_list['value_rating'] = house_info_list['value_rating'].map(lambda x:'%.1f' % x)
    house_info_list.to_csv(refine_file, sep='\t', header=True, index=False)

#def interplate_score(house_refiend_score_file, )

parse_raw_score(house_raw_score_file, house_refiend_score_file, interplate=True, parse_location=True)
            
            
            
