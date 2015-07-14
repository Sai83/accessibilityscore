"""
parse hispital raw score
"""
import pandas as pd
hosp_raw_score_file = 'hospital_raw_score.txt'
hosp_refiend_score_file = 'hospital_ref_score.csv'

def parse_raw_score(raw_file, refine_file):
    """Parse the raw hospital score file"""
    hos_score_list = []
    with open(raw_file, 'rU') as infile:
        for index, line in enumerate(infile):
            line = line.rstrip('\n')
            if index == 0:
                hos_score = {}
                continue
            elif '|' in line:
                #hos_score = {}  # new records begins...
                hos_score_list.append(hos_score)
                hos_score = {}
            elif 'Add to Compare' in line:  # skip
                continue
            elif 'OUT OF 5' in line:  # end of the score record
                #hos_score_list.append(hos_score)
                continue
            elif ', Minnesota' in line:
                city = line.split(',')[0]
                hos_score['city'] = city
            elif '%' in line:
                perc_10 = int(line[:-1]) * 0.01
                hos_score['percentage_of_10'] = perc_10
            elif line.isdigit():  #
                number = int(line)
                if number > 10:
                    rating = int(number)
                    hos_score["overall_rating"] = rating
                else:
                    satisfication = int(number)
                    hos_score["patient_rating"] = satisfication
            else:
                hos_score['name'] = line
            
    hos_score_list.append(hos_score)
    hos_score_list = pd.DataFrame(hos_score_list)
    print(hos_score_list)
    hos_score_list.to_csv(refine_file, sep='\t', header=True, index=False)

parse_raw_score(hosp_raw_score_file, hosp_refiend_score_file)
            
            
            
