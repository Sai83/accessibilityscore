"""
This module parse census tracts in MN
"""
import pandas as pd

tract_raw_file = "2014_Gaz_tracts_national.txt"
tract_mn_file = "mn_tracts.csv"


mn_info = []
with open(tract_raw_file, 'rU') as infile:
    for line in infile:
        content = line.rstrip().split('\t')
        if content[0] == 'MN':
            mn_info.append({'geoid': content[1],
                           'lat': content[-2].strip(), 'long': content[-1].strip()})


mn_info = pd.DataFrame(mn_info)
mn_info.to_csv(tract_mn_file, index=False)

#mn_dfs.to_csv(tract_mn_file, index=False)
