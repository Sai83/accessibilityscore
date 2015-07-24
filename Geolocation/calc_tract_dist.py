"""
This module compute the distance of census tract to all hospitals and house
"""
import pandas as pd
import geocoder


tract_file = 'mn_tracts.csv'
house_file = '../House/s8house_ref_score.csv'
hospital_file = '../Health/mn_hospital_score.csv'

house_dist_file = '../House/house_dist.csv'
hospital_dist_file = '../Health/hospital_dist.csv'

def calc_tract_dist(tract_file, facility_file, dist_file):
    """Calculate the distance between tract between every hospital/house"""
    facility = pd.read_csv(facility_file, sep='\t')
    tract = pd.read_csv(tract_file)
    geoid_dist = {}
    for index, row in tract.iterrows():
        id = row['geoid']
        lat = row['lat']
        long = row['long']
        l1 = (lat, long)
        dist_list = []
        for i, r in facility.iterrows():
            name = r['name']
            lat_f = r['lat']
            long_f = r['long']
            l2 = (lat_f, long_f)
            dist = geocoder.distance(l1, l2, units='miles')
            dist_list.append((dist, name))
        dist_list.sort(key=lambda x:x[0])
        #print(id)
        #print(dist_list[:10])
        #exit(1)
        geoid_dist[id] = dist_list

    geoid_dist = pd.Series(geoid_dist, name='distance')
    geoid_dist.index = geoid_dist.index.map(lambda x:'%.0f' % x)
    geoid_dist.to_csv(dist_file, sep='\t', index_label='geoid', header=True, float_format='%.3f')    
    
            
            
#calc_tract_dist(tract_file, hospital_file, hospital_dist_file)
calc_tract_dist(tract_file, house_file, house_dist_file)
    
