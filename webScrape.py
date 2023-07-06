import requests
import requests_html
import time
from bs4 import BeautifulSoup


# fips = '01073'
# testUrl = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-outcomes/length-of-life/premature-death?keywords=&f%5B0%5D=type%3Astates&f%5B1%5D=type%3Acounties&year=2023&county="+fips
# print("TRY:",testUrl)
# session = requests_html.HTMLSession()

# r = session.get(testUrl)
# time.sleep(2)
# soup = BeautifulSoup(r.html.html, 'html.parser')
# print(soup.find("div", {"class": "_chrr2022_data-tab__content"}))

def scrapeCensus():
    countyName = "Jefferson"
    countyDesc = "County"
    stateTitle = "AL"
    states = {
            'AL': 'Alabama',
            'AK': 'Alaska',
            'AZ': 'Arizona',
            'AR': 'Arkansas',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'HI': 'Hawaii',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'IA': 'Iowa',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'ME': 'Maine',
            'MD': 'Maryland',
            'MA': 'Massachusetts',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MS': 'Mississippi',
            'MO': 'Missouri',
            'MT': 'Montana',
            'NE': 'Nebraska',
            'NV': 'Nevada',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NY': 'New York',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VT': 'Vermont',
            'VA': 'Virginia',
            'WA': 'Washington',
            'WV': 'West Virginia',
            'WI': 'Wisconsin',
            'WY': 'Wyoming',
            'DC': 'District of Columbia',
            'MP': 'Northern Mariana Islands',
            'PW': 'Palau',
            'PR': 'Puerto Rico',
            'VI': 'Virgin Islands',
            'AA': 'Armed Forces Americas (Except Canada)',
            'AE': 'Armed Forces Africa/Canada/Europe/Middle East',
            'AP': 'Armed Forces Pacific'
            }
    stateTitle = states[stateTitle]
    urlTemplate = "https://data.census.gov/all?q="+countyName+"+"+countyDesc+",+"+stateTitle
    print(urlTemplate)

if __name__ == "__main__":
    scrapeCensus()
    