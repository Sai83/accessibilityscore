"""
This module compute the walkability score, metro score,
house score, hospital score and security score
"""
import pandas as pd
import ast
import math

level = 'tract'
ctu_file = 'Geolocation/CTU_ref.csv'
walk_score_file = 'Mobility/tract_walkscore.csv'
metro_score_file = 'Mobility/MetroTransit.csv'
hosp_score_file = 'Health/mn_hospital_score.csv'
hosp_dist_file = "Health/hospital_dist.csv"
house_score_file = 'House/s8house_ref_score.csv'
house_dist_file = 'House/house_dist.csv'
com_tract_score_file = 'Census_data/state_tract_com_score.txt'
com_city_score_file = 'Census/data/state_city_com_score.txt'
com_county_score_file = "Census/data/state_county_com_score.txt"
safety_score_file = "Safety/crime_rate_ref.csv"



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

        
        score_list.append({'tract':tract, 'city':city, 'county':county,
                           'walk_score':walk_score, 'metro_score':metro_score,
                           'safety_score':safety_score, 'house_score':house_score,
                           'hosp_score':hosp_score, 'com_score':com_score})

        #print(score_list)
        #exit(1)
    score_list = pd.DataFrame(score_list)
    score_list.to_csv(tract_score_file, index=False, columns=['tract','city','county',
                       'walk_score', 'metro_score', 'safety_score', 'com_score', 'hosp_score', 'house_score'])


def calc_city_score(tract_score_file):
    "calculate the accessibility score for each city"

    score_list = []

    # read ctu city profile #
    ctu_city = pd.read_csv(ctu_file, sep='\t')
    ctu_city.set_index('FEATURE_NAME', inplace=True)
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

        
        score_list.append({'tract':tract, 'city':city, 'county':county,
                           'walk_score':walk_score, 'metro_score':metro_score,
                           'safety_score':safety_score, 'house_score':house_score,
                           'hosp_score':hosp_score, 'com_score':com_score})

        #print(score_list)
        #exit(1)
    score_list = pd.DataFrame(score_list)
    score_list.to_csv(tract_score_file, index=False, columns=['tract','city','county',
                       'walk_score', 'metro_score', 'safety_score', 'com_score', 'hosp_score', 'house_score'])
        
    
tract_score_file = 'tract_score.csv'
calc_tract_score(tract_score_file)
