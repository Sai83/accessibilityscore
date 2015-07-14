"""
This module parse the zip code in MN
"""
import pandas as pd

zipcode_raw_file = "free-zipcode-database.csv"
zipcode_mn_file = "mn_zipcode.csv"


chunksize = 2000
mn_dfs = pd.DataFrame()
for df in pd.read_csv(zipcode_raw_file, sep=',', chunksize=chunksize, iterator=True, encoding='utf-8'):
    mn_df = df[df['State'] == 'MN']
    #print(df['State']=='MN')
    mn_dfs = mn_dfs.append(mn_df[['Zipcode', 'City', 'Lat', 'Long']])
    #break
#print(len(mn_dfs))
    #exit(1)
#zipcode = pd.read_csv(zipcode_raw_file)

mn_dfs.to_csv(zipcode_mn_file, index=False)
