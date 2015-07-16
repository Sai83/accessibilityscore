"""
Parse the hospital score and extract MN hospitals
"""
import pandas as pd
import math
import time
import geocoder

# list of data sets #
hospital_info = "Hospital_General_Information.csv"
hospital_score = "Hospital_Score.csv"
mn_score = "hospital_score_mn.csv"
mn_hospital = "mn_hospital_info.csv"
hosp_refiend_score_file = 'hospital_ref_score.csv'
combined_score_file = 'mn_hospital_score.csv'

quote = 0
def extract_mn_score(hospital_score_file, mn_score_file):
    """Extract MN hopistal scores"""
    score = pd.read_csv(hospital_score)
    #print(score)

    mn_score = score[score["State"] == "MN"][["Provider Number", "Hospital Name",
                                              "Location", "City", "ZIP Code", "County Name",
                                              "Total Performance Score"]]
    #print(mn_score)
    #print(mn_score['Total Performance Score'].describe())
    mn_score['Location'] = mn_score['Location'].apply(lambda x:x.replace('\n', ' '))
    mn_score.to_csv(mn_score_file, sep='\t', index=False)


def extract_mn_info(hospital_info, mn_file):
    """Extract hospital general information"""
    hos_info = pd.read_csv(hospital_info)
    #print(hos_info)
    mn_hos = hos_info[hos_info["State"] == "MN"][["Provider ID", "Hospital Name",
                                              "Location", "City", "County Name", "ZIP Code", "Hospital Type"]]
        
    mn_hos['Location'] = mn_hos['Location'].apply(lambda x:x.replace('\n', ' '))
    mn_hos.to_csv(mn_file, sep='\t', index=False)

def combine_score_info(mn_hospital, hosp_refiend_score_file, combined_file, interplate=False, parse_location=False):
    """Combine score location and score information in MN"""
    score = pd.read_csv(hosp_refiend_score_file, sep='\t')
    hosp = pd.read_csv(mn_hospital, sep='\t', index_col=1)
    #print(score)
    combine = []
    for index, row in score.iterrows():
        name = row['name']
        search_name = name.upper()
        #print(name)
        if search_name in hosp.index:
            info = {}
            info['name'] = name
            info['city'] = row['city']
            info['county'] = hosp.ix[search_name, 'County Name']
            try:
                loc_info = hosp.ix[search_name, 'Location'].split(',')
            except:
                #print(hosp.ix[search_name, 'Location'])
                print('duplicate records:', name)
                continue
            address = loc_info[0].replace(row['city'].upper(), '').strip()
            info['address'] = address
            try:
                lat = loc_info[1].split('(')[1]
                long = loc_info[2].strip(' )')
            except: # lat and long code are not provided...
                if parse_location:
                    print (name, address)
                    place = address + ', ' + row['city'] + ', MN'
##                    if quote == 10:
##                        print("needs to wait for a minute")
##                        time.sleep(60) #
##                        quote = 0
##                    quote += 1
                    location = geocoder.google(place)
                    parsed_address = location.address
                    if not parsed_address:
                        print('query yahoo...')
                        location = geocoder.yahoo(place)
                        parsed_address = location.address
                    else:
                        print('query google')
                    if not parsed_address:
                        print(name, address)
                        exit(1)
                    lat = location.lat
                    long = location.lng
                else:
                    lat = ''
                    long = ''
                #print('no lat/long:', name)
            info['lat'] = lat
            info['long'] = long
            info['zipcode'] = hosp.ix[search_name, 'ZIP Code']
            info['type'] = hosp.ix[search_name, 'Hospital Type']
            info['overall_rating'] = row['overall_rating']
            info['patient_rating'] = row['patient_rating']
            info['percentage_of_10'] = row['percentage_of_10']
            combine.append(info)
        elif name == 'Mayo Clinic Methodist Hospital':
            info = {}
            info['name'] = name
            info['city'] = 'Rochester'
            info['county'] = 'OLMSTED'
            info['address'] = '201 West Center Street'.upper()
            info['lat'] = 44.0234914
            info['long'] = -92.465934
            info['zipcode'] = 55902
            info['type'] = 'Acute Care Hospitals'
            info['overall_rating'] = row['overall_rating']
            info['patient_rating'] = row['patient_rating']
            info['percentage_of_10'] = row['percentage_of_10']
            combine.append(info)
        else: # cannot find hospital information.
            print ("not found:", name)
            continue

    combine = pd.DataFrame(combine)
    if interplate:
        score_group = combine.groupby('overall_rating')
        score_mean = score_group.mean()
        print(score_mean)
        for index, row in combine.iterrows():
            score = row['overall_rating']
            patient_rating = row['patient_rating']
            percent = row['percentage_of_10']
            if math.isnan(patient_rating):
                patient_rating = score_mean.ix[score, 'patient_rating']
                if math.isnan(patient_rating):
                    print(row['name'])
                    combine.ix[index, 'patient_rating'] = 4.0
                else:
                    combine.ix[index, 'patient_rating'] = patient_rating
            if math.isnan(percent):
                percent = score_mean.ix[score, 'percentage_of_10']
                if math.isnan(percent):
                    print(row['name'])
                    combine.ix[index, 'percentage_of_10'] = 0.7
                else:
                    combine.ix[index, 'percentage_of_10'] = percent
            
            
    combine['patient_rating'] = combine['patient_rating'].map(lambda x:'%.0f' % x)           
    combine.to_csv(combined_file, sep='\t', index=False, float_format='%.2f')
    

if __name__ == "__main__":
    #extract_mn_score(hospital_score, mn_score)
    extract_mn_info(hospital_info, mn_hospital)
    combine_score_info(mn_hospital, hosp_refiend_score_file,
                       combined_score_file, interplate=True, parse_location=True)
