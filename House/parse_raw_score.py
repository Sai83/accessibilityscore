"""
parse house raw score
"""
import pandas as pd
import math
house_raw_score_file = 's8house_raw_score.txt'
house_refiend_score_file = 's8house_ref_score.csv'
house_interp_score_file = 's8house_interp_score.csv'

types = {"Low Income", "Elderly", "Disabled", "Rural"}

def parse_raw_score(raw_file, refine_file, interplate=False):
    """Parse the raw house score file"""
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
                house_info['city'] = city
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
                if index > 0:
                    #print(house_info)
                    house_info_list.append(house_info)
                    #exit(1)
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
            
    house_info_list.append(house_info) # record the last 
    house_info_list = pd.DataFrame(house_info_list)
##        score_nan_index = {}
##        rating_nan_index = {}
##        for index, row in house_info_list.iterrows():
##            hud_score = row['hud_score']
##            rating = row['value_rating']
##            city = row['city']
##            #print (rating)
##            if math.isnan(hud_score):
##                score_nan_index[index] = 
##            #if not isinstance(rating, float):
##            #    print(index)
    #print(house_info_list)
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
    house_info_list.to_csv(refine_file, sep='\t', header=True, index=False, float_format='%.1f')

#def interplate_score(house_refiend_score_file, )

parse_raw_score(house_raw_score_file, house_refiend_score_file, interplate=True)
            
            
            
