import requests
import requests_html
import time
import pandas
from selenium import webdriver
from bs4 import BeautifulSoup

def generateCensusLinks():
    links = []
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
    xl = pandas.read_excel("2020-2023 RAM Clinic Locations (County-Level Data) (1).xlsx", sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0,len(counties) - 1):
        county = counties.iloc[i].values[0]
        arr = county.split(" ")
        arr[-1] = states[arr[-1]]
        county = "+".join(arr)
        urlTemplate = "https://data.census.gov/all?q="+county
        links.append(urlTemplate)
    return links

def scrapeCensusPopulations():
    print(" - - Scraping Census Data - - ")
    links = generateCensusLinks()
    for i in links:
        print("\n Source:",i)
        sleeptime = 0.5
        session = requests_html.HTMLSession()
        r = session.get(i)
        result = []
        while result == []:
            sleeptime *= 2
            r.html.render(timeout=25, sleep=sleeptime)
            result = r.html.find(".featured-result-value")
        print(" * * POPULATION: "+result[0].text+" * * ")
        session.close()

def scrapePrematureDeaths():
        fips = '01073'
        testUrl = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-outcomes/length-of-life/premature-death?keywords=&f%5B0%5D=type%3Astates&f%5B1%5D=type%3Acounties&year=2023&county="+fips
        print("TRY:",testUrl)
        
        session = requests_html.HTMLSession()
        r = session.get(testUrl)
        result = []
        sleeptime = 6
        r.html.render(timeout=25, sleep=sleeptime)
        result = r.html.find("._chrr2022_measures__measure-disaggregated-table-highlighted-row")[0].html
        soup = BeautifulSoup(result, 'html.parser')
        print(soup.findAll("td")[1].text)
            
if __name__ == "__main__":
    #scrapeCensusPopulations()
    scrapePrematureDeaths()
    