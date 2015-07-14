"""
Parse the hospital score and extract MN hospitals
"""
import pandas as pd

# list of data sets #
hospital_info = "Hospital_General_Information.csv"
hospital_score = "Hospital_Score.csv"
mn_score = "hospital_score_mn.csv"
mn_hospital = "mn_hospital_info.csv"
hosp_refiend_score_file = 'hospital_ref_score.csv'
combined_score_file = 'mn_hospital_score.csv'

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

def combine_score_info(mn_hospital, hosp_refiend_score_file, combined_file):
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
            address = loc_info[0]
            info['address'] = address
            try:
                lat = loc_info[1].split('(')[1]
                long = loc_info[2].strip(' )')
            except:
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
            info['lat'] = ''
            info['long'] = ''
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
    combine.to_csv(combined_file, sep='\t', index=False)
    

if __name__ == "__main__":
    #extract_mn_score(hospital_score, mn_score)
    extract_mn_info(hospital_info, mn_hospital)
    combine_score_info(mn_hospital, hosp_refiend_score_file, combined_score_file)
