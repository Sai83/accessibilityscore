"""
This module computes the percentage of disabled persons and score
"""
import pandas as pd
import ast

county_file = 'state_county.txt'
city_file = 'state_city.txt'
tract_file = 'state_tract.txt'

dis_keys = ["B18101_004E",
            "B18101_007E",
            "B18101_010E",
            "B18101_013E",
            "B18101_016E",
            "B18101_019E",
            "B18101_023E",
            "B18101_026E",
            "B18101_029E",
            "B18101_032E",
            "B18101_035E",
            "B18101_038E"]

def calc_community_score(level='county'):
    """Calculate the community score based on disability percentage stas"""
    data_file = 'state_' + level + '.txt'

    with open(data_file, 'rU') as infile:
        content = infile.read()
        json = ast.literal_eval(content)
        #print(len(json))
        place_data = []
        pop_data = []
        for data in json:
            if level == 'county':
                county= data["name"].split(',')[0].replace('County', '').strip()
                id = data['county']
                county = county.replace('St.', 'St')
            elif level == 'city':
                id = data["place"]
                city= data["name"].split(',')[0].replace('city', '').strip()
                city = city.replace('St.', 'St')
            elif level == 'tract':
                id = data['state']+data['county']+data['tract']
                county = data['name'].split(',')[1].replace('County', '').strip()
            total = int(data["B18101_001E"].strip('"'))
            #print(total)
            dis_stas = [int(data[x].strip('"')) for x in dis_keys]
            #print(dis_stas)
            #print(sum(dis_stas))
            if total > 0:
                ratio = sum(dis_stas)/total
                if level == 'county':
                    place_data.append({'id': id, 'county': county, 'disability_percentage': ratio})
                    pop_data.append({'id': id, 'county': county, 'population': total})
                elif level == 'city':
                    place_data.append({'id': id, 'city': city, 'disability_percentage': ratio})
                    pop_data.append({'id': id, 'city': city, 'population': total})
                elif level == 'tract':
                    place_data.append({'tract': id, 'county': county, 'disability_percentage': ratio})
                    pop_data.append({'tract': id, 'county': county, 'population': total})


    place_data = pd.DataFrame(place_data)
    min_v = place_data['disability_percentage'].min()
    max_v = place_data['disability_percentage'].max()
    place_data['score'] = (place_data['disability_percentage']-min_v)/(max_v-min_v)*100
    print(place_data)

    save_file = 'state_'+level + '_com_score.txt'
    place_data['disability_percentage'] = place_data['disability_percentage'].map(lambda x:'%.3f' % x)

    place_data.to_csv(save_file, sep='\t', float_format='%.0f', index=False)

    pop_file = level+'_pop.csv'
    pop_data = pd.DataFrame(pop_data)
    pop_data.to_csv(pop_file, sep='\t', float_format='%.0f', index=False)
    
    

calc_community_score('county')
calc_community_score('city')
calc_community_score('tract')

        

