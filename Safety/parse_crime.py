"""
parse the criminal rate
"""
raw_file = 'crime_rate.csv'
ref_file = 'crime_rate_ref.csv'

import pandas as pd
crime = pd.read_csv(raw_file, sep='\t')
#print(crime)

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

crime_info = pd.DataFrame(crime_info)
#print(crime_info)
        
#cr_county = crime_info[crime_info['city'].apply(lambda x:'County' in x)]
min_cr = crime_info['crime_rate'].min()
max_cr = crime_info['crime_rate'].max()
#print(min_cr, max_cr)
crime_info['score'] = 100 - (crime_info['crime_rate']-min_cr)/(max_cr-min_cr)*100
crime_info.to_csv(ref_file, sep='\t', index=False, float_format='%.1f')
