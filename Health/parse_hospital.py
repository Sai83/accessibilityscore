"""
Parse the hospital score and extract MN hospitals
"""
import pandas as pd

# list of data sets #
hospital_info = "Hospital_General_Information.csv"
hospital_score = "Hospital_Score.csv"
mn_score = "hospital_score_mn.csv"
mn_hospital = "mn_hospital_info.csv"

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
                                              "Location", "City", "ZIP Code", "Hospital Type"]]
        
    mn_hos['Location'] = mn_hos['Location'].apply(lambda x:x.replace('\n', ' '))
    mn_hos.to_csv(mn_file, sep='\t', index=False)


if __name__ == "__main__":
    #extract_mn_score(hospital_score, mn_score)
    extract_mn_info(hospital_info, mn_hospital)
    
