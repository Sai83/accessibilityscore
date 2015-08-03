"""
This module compute the walkability score, metro score,
house score, hospital score and security score
"""
import pandas as pd
import ast
import math
import numpy as np

#level = 'tract'
#tract_file = 'Census_data/tract_pop.csv'
#city_file = 'Census_data/city_pop.csv'
#county_file = 'Census_data/county_pop.csv'
walk_score_file = 'Mobility/tract_walkscore.csv'
city_walk_score_file = 'Mobility/city_walkscore.csv'
metro_score_file = 'Mobility/MetroTransit.csv'
hosp_score_file = 'Health/mn_hospital_score.csv'
hosp_dist_file = "Health/hospital_dist.csv"
house_score_file = 'House/s8house_ref_score.csv'
house_dist_file = 'House/house_dist.csv'
com_tract_score_file = 'Census_data/state_tract_com_score.txt'
com_city_score_file = 'Census_data/state_city_com_score.txt'
com_county_score_file = "Census_data/state_county_com_score.txt"
safety_score_file = "Safety/crime_rate_ref.csv"
city_county_file = "Geolocation/city_county.csv"
county_cities_file = 'Geolocation/county_cities.csv'

# set up the default weights #
weights = [0.2] * 4
walk_w = 0.2 * 0.7
metro_w = 0.2 * 0.3
weights = [walk_w, metro_w] + weights


#exit(1)

def city_normalize(city):
    """Normalize city names"""
    if 'St.' in city:
        city = city.replace('.', '')
    elif 'Saint' in city:
        city = city.replace('Saint', 'St')

    return city

def calc_tract_score(tract_score_file):
    "calculate the accessibility score for each tract"

    score_list = []

    # read metro score file #
    metroscore = pd.read_csv(metro_score_file)
    metroscore.set_index('city', inplace=True)
    #print(metroscore)

    # read safety score file #
    safetyscore = pd.read_csv(safety_score_file, sep='\t')
    safetyscore.set_index('city', inplace=True)
    #print(safetyscore)
    #print (safetyscore['Aitkin County Total'])

    # read house dist/score file #
    housedist = pd.Series.from_csv(house_dist_file, sep='\t', header=0)
    #print(housedist)
    housescore = pd.read_csv(house_score_file, sep='\t')
    housescore.set_index('name', inplace=True)
    
    

    # read hospital dist/score file #
    hospdist = pd.Series.from_csv(hosp_dist_file, sep='\t', header=0)
    #print(hospscore)
    hospscore = pd.read_csv(hosp_score_file, sep='\t')
    hospscore.set_index('name', inplace=True)

    # read community score file #
    comscore = pd.read_csv(com_tract_score_file, sep='\t')
    comscore.set_index('tract', inplace=True)
    #print(comscore)

    
    # extract walkability score and combine all other scores#
    walkscore = pd.read_csv(walk_score_file, sep='\t')
    for index, row in walkscore.iterrows():
        tract = row['geoid']
        city = row['city']
        if pd.isnull(city):
            #print(tract)
            #exit(1)
            city = 'Unknown'
        county = row['county']
        #print(tract, city, county)
        # first, extract walk score #
        walk_score = row['walkscore']

        # second, extract metro score #
        try:
            metro_score = int(metroscore.ix[city, 'percentage'].rstrip('%'))
        except KeyError:
            metro_score = 0

        # thrid, extract safety score #
        try:
            safety_score = safetyscore.ix[city, 'score']
        except KeyError:
            try:
                safety_score = safetyscore.ix[city + ' PD', 'score']
            except KeyError:
                try:
                    safety_score = safetyscore.ix[county + ' Co. Sheriff', 'score']
                except KeyError:
                    try:
                        safety_score = safetyscore.ix[county + ' County Total', 'score']
                    except KeyError:
                        try:
                            safety_score = safetyscore.ix[county, 'score']
                        except KeyError:
                            print('county safety score not found', tract, county)
                            safety_score = 0

        
        # 4th, extract house score #
        house_dist = ast.literal_eval(housedist[tract])
        nearest_house_dist, name = house_dist[0]
        if nearest_house_dist <= 5:
            house_score = housescore.ix[name, 'hud_score']
        else:
            house_score = 0

        # 5th, extract hospital score #
        hosp_dist = ast.literal_eval(hospdist[tract])
        nearest_hosp_dist, name = hosp_dist[0]
        if nearest_hosp_dist <= 5:
            hosp_score = hospscore.ix[name, 'overall_rating']
        else:
            hosp_score = 0

        # 6th, extract community score #
        try:
            com_score = comscore.ix[tract, 'score']
        except KeyError:
            com_score = 0

        # compute the final accessbility score #
        raw_scores = [walk_score, metro_score, safety_score, house_score, hosp_score, com_score]
        accessbility_score = np.dot(raw_scores, weights)
        score_list.append({'tract':tract, 'city':city, 'county':county,
                           'walk_score':walk_score, 'metro_score':metro_score,
                           'safety_score':safety_score, 'house_score':house_score,
                           'hospital_score':hosp_score, 'community_score':com_score,
                           'accessibility_score':accessbility_score})

        #print(score_list)
        #exit(1)
    score_list = pd.DataFrame(score_list)
    score_list.to_csv(tract_score_file, index=False, float_format='%.0f', columns=['tract','city','county',
                       'walk_score', 'metro_score', 'safety_score', 'community_score', 'hospital_score', 'house_score', 'accessibility_score'])


def calc_city_score(tract_score_file):
    "calculate the accessibility score for each city"
    score_list = []

    # read tract/city profile #
    #tract_pop = pd.read_csv(tract_file, sep='\t', index_col=-1)
    #city_pop = pd.read_csv(city_file, sep='\t', index_col=0)
    #print(tract_pop)
    #print(city_pop)
    #print(ctu_city)
    #exit(1)
    
    
    # read metro score file #
    metroscore = pd.read_csv(metro_score_file)
    metroscore.set_index('city', inplace=True)
    #print(metroscore)

    # read safety score file #
    safetyscore = pd.read_csv(safety_score_file, sep='\t')
    safetyscore.set_index('city', inplace=True)
    #print(safetyscore)
    #print (safetyscore['Aitkin County Total'])

    # read house dist/score file #
    housedist = pd.Series.from_csv(house_dist_file, sep='\t', header=0)
    #print(housedist)
    housescore = pd.read_csv(house_score_file, sep='\t')
    #housescore.set_index('name', inplace=True)
    housegroup = housescore.groupby('city')
    

    # read hospital dist/score file #
    hospdist = pd.Series.from_csv(hosp_dist_file, sep='\t', header=0)
    #print(hospscore)
    hospscore = pd.read_csv(hosp_score_file, sep='\t')
    #hospscore.set_index('name', inplace=True)
    hospgroup = hospscore.groupby('city')

    # read community score file #
    comscore = pd.read_csv(com_city_score_file, sep='\t', dtype={'id':str})
    #comscore.set_index('city', inplace=True)
    #print(comscore)

    
    # extract walkability score and combine all other scores#
    walkscore = pd.read_csv(walk_score_file, sep='\t')
    #walkscore.set_index('city', inplace=True)
    # find city-county approximate mapping #
    city_county = pd.Series.from_csv(city_county_file, header=0)
        
    walkgroup = walkscore.groupby('city')

    city_walkscore = pd.read_csv(city_walk_score_file)
    city_walkscore.set_index('city', inplace=True)

    for index, row in comscore.iterrows():
        city = row['city']
        id = row['id']
        # extract community score #
        com_score = row['score']

        
        # extract walkability score #     
        #print(city)
        county = city_county[city]

        # extract tract average score #
        try:
            group = walkgroup.get_group(city)
            group_sel = group[group['walkscore']>0] #

            if len(group_sel) == 0:  # 
                #walk_score = city_walkscore.ix[city, 'walkscore']
                walk_score1 = 0
            else:
                walk_score1 = group_sel.mean()['walkscore']
##                if len(group_sel) >= 3:
##                    walk_score = group_sel.mean()['walkscore']
##                else:
##                    walk_score = city_walkscore.ix[city, 'walkscore']
        except KeyError:
            #walk_score = city_walkscore.ix[city, 'walkscore']
            walk_score1 = 0

        walk_score2 = city_walkscore.ix[city, 'walkscore']
        walk_score = 0.3*walk_score2 + 0.7*walk_score1


        #print(city, walk_score)
        
        # second, extract metro score #
        try:
            metro_score = int(metroscore.ix[city, 'percentage'].rstrip('%'))
        except KeyError:
            metro_score = 0

        # thrid, extract safety score #
        try:
            safety_score = safetyscore.ix[city, 'score']
        except KeyError:
            try:
                safety_score = safetyscore.ix[city + ' PD', 'score']
            except KeyError:
                try:
                    safety_score = safetyscore.ix[county + ' Co. Sheriff', 'score']
                except KeyError:
                    try:
                        safety_score = safetyscore.ix[county + ' County Total', 'score']
                    except KeyError:
                        try:
                            safety_score = safetyscore.ix[county, 'score']
                        except KeyError:
                            print('county safety score not found', tract, county)
                            safety_score = 0

        
        # 4th, extract house score #
        try:
            house_score = housegroup.get_group(city).mean()['hud_score']
        except:
            house_score = 0

        # 5th, extract hospital score #
        try:
            hosp_score = hospgroup.get_group(city).mean()['overall_rating']
        except:
            hosp_score = 0

        # 6th, extract community score #
##        try:
##            com_score = comscore.ix[city, 'score']
##            id = comscore.ix[city, 'id']
##        except KeyError:
##            com_score = 0
        

        # compute the final accessbility score #
        raw_scores = [walk_score, metro_score, safety_score, house_score, hosp_score, com_score]
        accessbility_score = np.dot(raw_scores, weights)
        score_list.append({'city':city, 'county':county, 'id':id,
                           'walk_score':walk_score, 'metro_score':metro_score,
                           'safety_score':safety_score, 'house_score':house_score,
                           'hospital_score':hosp_score, 'community_score':com_score, 'accessibility_score':accessbility_score})

        #print(score_list)
        #exit(1)
    score_list = pd.DataFrame(score_list)
    score_list.to_csv(tract_score_file, index=False, float_format='%.0f', columns=['id', 'city', 'county',
                       'walk_score', 'metro_score', 'safety_score', 'community_score', 'hospital_score', 'house_score', 'accessibility_score'])

def calc_county_score(tract_score_file):
    "calculate the accessibility score for each county"
    score_list = []

    # read city score file first #
    county_cities = pd.Series.from_csv(county_cities_file, header=0, sep='\t')
    #print(county_cities)
            
    # read metro score file #
    metroscore = pd.read_csv(metro_score_file)
    metroscore.set_index('city', inplace=True)
    #print(metroscore)

    # read safety score file #
    safetyscore = pd.read_csv(safety_score_file, sep='\t')
    safetyscore.set_index('city', inplace=True)
    #print(safetyscore)
    #print (safetyscore['Aitkin County Total'])

    # read house dist/score file #
    housedist = pd.Series.from_csv(house_dist_file, sep='\t', header=0)
    #print(housedist)
    housescore = pd.read_csv(house_score_file, sep='\t')
    #housescore.set_index('name', inplace=True)
    housegroup = housescore.groupby('county')
    

    # read hospital dist/score file #
    hospdist = pd.Series.from_csv(hosp_dist_file, sep='\t', header=0)
    #print(hospscore)
    hospscore = pd.read_csv(hosp_score_file, sep='\t')
    #hospscore.set_index('name', inplace=True)
    hospgroup = hospscore.groupby('county')

    # read community score file #
    comscore = pd.read_csv(com_county_score_file, sep='\t')
    comscore.set_index('county', inplace=True)
    #print(comscore)

    
    # extract walkability score and combine all other scores#
    #walkscore = pd.read_csv(walk_score_file, sep='\t')
    city_score = pd.read_csv(city_score_file)
        
    walkgroup = city_score.groupby('county')
    for county, group in walkgroup:
        #print(city)
        group_sel = group[group['walk_score']>0] # 
        if len(group_sel) > 0:
            walk_score = group_sel.mean()['walk_score']
        else:
            walk_score = 0
            
        # second, extract metro score #
        metro_score = []
        for city in ast.literal_eval(county_cities[county]):
            try:
                metro_score.append(int(metroscore.ix[city, 'percentage'].rstrip('%')))
            except KeyError:
                continue
            
        if len(metro_score) > 0:
            metro_score = sum(metro_score) / len(metro_score)
        else:
            metro_score = 0

        # thrid, extract safety score #
        try:
            safety_score = safetyscore.ix[county + ' County Total', 'score']
        except KeyError:
            try:
                safety_score = safetyscore.ix[county, 'score']
            except KeyError:
                print('county safety score not found', tract, county)
                safety_score = 0

        
        # 4th, extract house score #
        try:
            house_score = housegroup.get_group(county).mean()['hud_score']
        except:
            house_score = 0

        # 5th, extract hospital score #
        try:
            hosp_score = hospgroup.get_group(county.upper()).mean()['overall_rating']
        except:
            hosp_score = 0

        # 6th, extract community score #
        try:
            com_score = comscore.ix[county, 'score']
            id = comscore.ix[county, 'id']
        except KeyError:
            com_score = 0

        raw_scores = [walk_score, metro_score, safety_score, house_score, hosp_score, com_score]
        accessibility_score = np.dot(raw_scores, weights)
        
        score_list.append({'county':county, 'id':id,
                           'walk_score':walk_score, 'metro_score':metro_score,
                           'safety_score':safety_score, 'house_score':house_score,
                           'hospital_score':hosp_score, 'community_score':com_score, 'accessibility_score':accessibility_score})

        #print(score_list)
        #exit(1)
    score_list = pd.DataFrame(score_list)
    score_list.to_csv(tract_score_file, index=False, float_format='%.0f', columns=['id', 'county',
                       'walk_score', 'metro_score', 'safety_score', 'community_score', 'hospital_score', 'house_score', 'accessibility_score'])
        

    
tract_score_file = 'final_scores/tract_score.csv'
calc_tract_score(tract_score_file)
city_score_file = 'final_scores/city_score.csv'
calc_city_score(city_score_file)
county_score_file = 'final_scores/county_score.csv'
calc_county_score(county_score_file)
