"""
This administrative places in MN
"""
import pandas as pd

ctu_raw_file = "CTU.csv"
ctu_ref_file = "CTU_ref.csv"

ctu = pd.read_csv(ctu_raw_file)
#print(ctu)

ctu['FEATURE_NAME'] = ctu['FEATURE_NAME'].apply(lambda x:x.split('of ')[-1])
ctu['COUNTY_NAME'] = ctu['COUNTY_NAME'].apply(lambda x:x.split(' ')[0])


print(ctu)
ctu[['FEATURE_NAME', 'CTU_TYPE', 'LATITUDE',
     'LONGITUDE', 'CENSUS_CODE', 'COUNTY_NAME']].to_csv(ctu_ref_file, sep='\t', index=False)

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
