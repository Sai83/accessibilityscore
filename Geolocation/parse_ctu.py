"""
This administrative places in MN
"""
import pandas as pd

ctu_raw_file = "CTU.csv"
ctu_ref_file = "CTU_ref.csv"

ctu = pd.read_csv(ctu_raw_file)
#print(ctu)

ctu_sel = []
for index, row in ctu.iterrows():
    feature = row['FEATURE_NAME']
    type = row['CTU_TYPE']
    lat = row['LATITUDE']
    lng = row['LONGITUDE']
    if type == 'City':
        if '(historical)' not in feature:
            city = feature.split('of ')[-1].strip()
            city = city.replace('Saint', 'St')
            ctu_sel.append({'name':city, 'type':'city', 'lat':lat, 'lng':lng})
    elif type == 'County':
        county = feature.replace('County', '').strip()
        county = county.replace(' qui ', ' Qui ')
        ctu_sel.append({'name':county, 'type':'county', 'lat':lat, 'lng':lng})
    else:
        continue

ctu_sel = pd.DataFrame(ctu_sel)
ctu_sel.drop_duplicates(inplace=True)
ctu_sel.to_csv(ctu_ref_file, index=False, columns=['name', 'type', 'lat', 'lng'])
        
##ctu['FEATURE_NAME'] = ctu['FEATURE_NAME'].apply(lambda x:x.split('of ')[-1].strip())
##ctu['COUNTY_NAME'] = ctu['COUNTY_NAME'].apply(lambda x:x.replace('County', '').strip())
##
##
##print(ctu)
##ctu[['FEATURE_NAME', 'CTU_TYPE', 'LATITUDE',
##     'LONGITUDE', 'CENSUS_CODE']].to_csv(ctu_ref_file, sep='\t', index=False)

##chunksize = 2000
##mn_dfs = pd.DataFrame()
##for df in pd.read_csv(zipcode_raw_file, sep=',', chunksize=chunksize, iterator=True, encoding='utf-8'):
##    mn_df = df[df['State'] == 'MN']
##    #print(df['State']=='MN')
##    mn_dfs = mn_dfs.append(mn_df[['Zipcode', 'City', 'Lat', 'Long']])
##    #break
###print(len(mn_dfs))
##    #exit(1)
###zipcode = pd.read_csv(zipcode_raw_file)
##
##mn_dfs.to_csv(zipcode_mn_file, index=False)
