#!/usr/local/bin/python
from walkscore.api import WalkScore, TransitScore
import json
def main():
    apiKey='ffd1c56f9abcf84872116b4cc2dfcf31'
    walkscore = WalkScore(apiKey)

    address='1119+8th+Avenue+Seattle+WA+98101'
    lat =47.6085
    long=-122.3295
    ws = walkscore.makeRequest(address, lat, long)
    print ("walk score:", ws)


    transitscore = TransitScore(apiKey)
    city='Eagan'
    state='MN'
    lat = 44.818173
    long = -93.1659179
    ts = transitscore.makeRequest(city, state, lat, long)
    print ("transit score:", ts)
##   
    #with open('output.json', 'w') as outfile:
	#    json.dump(ws, outfile)


if __name__ == '__main__':
    main()
