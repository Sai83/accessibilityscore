from walkscore.api import WalkScore

def main():
    apiKey='ffd1c56f9abcf84872116b4cc2dfcf31'
    walkscore = WalkScore(apiKey)

    address='1119 8th Avenue Seattle WA 98101'
    lat =47.6085
    long=-122.3295
    print walkscore.makeRequest('', lat, long)

if __name__ == '__main__':
    main()
