"""
parse the criminal rate
"""
raw_file = 'crime_rate.csv'
ref_file = 'crime_rate_ref.csv'

import pandas as pd
crime = pd.read_csv(raw_file, sep='\t')
#print(crime)


def calculate_rank_percentage(L):
    "given a list of numbers, return score in terms of rank index"
    
county = ''
crime_info = []
for index, row in crime.iterrows():
    agency = row["Agency"].rstrip('*')
    if agency == 'Inver Grove Hgts':
        agency = "Inver Grove Heights"
    pop = int(row["Population"].replace(',', ''))
    c1 = int(row["Part 1 Crime Rate"].replace(',', ''))
    c2 = int(row["Part 2 Crime Rate"].replace(',', ''))
    cr = int(row["Combined Crime Rate"].replace(',', ''))
    clear = row["Percent Cleared"]
    if 'County' in agency:
        county = agency.replace('County Total', '').strip()

    cur_county = county
    if cr == 0:  # data missing
        continue
    else:
        crime_info.append({'city':agency, 'population':pop, 'crime_rate':cr,
                           'cleared':clear, 'county':county})

crime_info.append({'city':'Otter Tail', 'population':57159, 'crime_rate':1728,
                   'cleared':50, 'county':'Otter Tail'})
crime_info.append({'city':'Sibley', 'population':15036, 'crime_rate':339,
                   'cleared':50, 'county':'Sibley'})

crime_info = pd.DataFrame(crime_info)
#print(crime_info)
        
#cr_county = crime_info[crime_info['city'].apply(lambda x:'County' in x)]

## score transformation ##


## old algorithm, using minimum-maximum scaling ##
##min_cr = crime_info['crime_rate'].min()
##max_cr = crime_info['crime_rate'].max()
##crime_info['score'] = (max_cr-crime_info['crime_rate'])/(max_cr-min_cr)*100

## new algorithm, using cumulative percentage as score ##
rate_list = list(crime_info['crime_rate'])
score_list = []
for index, row in crime_info.iterrows():
    rate = row['crime_rate']
    x_filter = list(filter(lambda x:x>=rate, rate_list))
    r = len(x_filter)/len(rate_list)
    score_list.append(r*100)
crime_info['score'] = score_list
    



crime_info.to_csv(ref_file, sep='\t', index=False, float_format='%.0f')
