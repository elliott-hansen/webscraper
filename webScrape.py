import requests
import requests_html
import time
import pandas
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from colorama import Fore, Back, Style

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
    dataArray = []
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
        dataArray.append(result[0].text)
    return dataArray

def generateFips(state):
    state = state.split(" ")
    stateAbb = state.pop(-1)
    state = " ".join(state)
    state = state.replace(",","")
    state = state.upper()
    with open("fips.csv") as csv_file:
         csv_reader = csv.reader(csv_file, delimiter=",")
         for row in csv_reader:
              if row[2] != stateAbb:
                   continue
              if row[1].upper() == state:
                   return row[0]
              for i in state.split(" "):
                   if (i in row[1].upper() and (i != "COUNTY")):
                        return row[0]
              
def scrapePrematureDeaths():
        dataArray = []
        xl = pandas.read_excel("2020-2023 RAM Clinic Locations (County-Level Data) (1).xlsx", sheet_name="Counties of RAM Clinics", usecols="H")
        counties = xl.loc[1:]
        for i in range(0, len(counties) - 1):
            county = counties.iloc[i].values[0]
            print(" - | Getting data for:",county+"...")
            fips = generateFips(county)
            # print("Generated fips: ", fips)
            testUrl = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-outcomes/length-of-life/premature-death?keywords=&f%5B0%5D=type%3Astates&f%5B1%5D=type%3Acounties&year=2023&county="+fips
            
            session = requests_html.HTMLSession()
            r = session.get(testUrl)
            result = []
            sleeptime = 3.0
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__measure-disaggregated-table-highlighted-row") != []:
                result = r.html.find("._chrr2022_measures__measure-disaggregated-table-highlighted-row")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[1].text
                adjustment = r.html.find("._chrr2022_measures__premature-death-tables-table")[0].html
                soup2 = BeautifulSoup(adjustment, 'html.parser')
                adjustment = soup2.findAll("th")[2].text.split(" ")[-1]
                if adjustment == "100,000":
                 result = int(result.replace(",","")) / 10
                if adjustment == "1,000":
                    result = int(result.replace(",","")) * 10
                print(" - | Mortality:",str(f'{result:,}')+"\n")
                dataArray.append(str(f'{result:,}'))
            else:
                 print(Back.RED + " - - Fail!")
                 print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
                 print(Style.RESET_ALL)

                 dataArray.append("N/A")
        return dataArray

def scrapePhysicalUnhealthyDays():
    dataArray = []
    xl = pandas.read_excel("2020-2023 RAM Clinic Locations (County-Level Data) (1).xlsx", sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print(" - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-outcomes/quality-of-life/poor-physical-health-days?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = 1.2
        r.html.render(timeout=25, sleep=sleeptime)
        if r.html.find("._chrr2022_measures__table") != []:
            result = r.html.find("._chrr2022_measures__table")[0].html
            soup = BeautifulSoup(result, 'html.parser')
            result = soup.findAll("td")[3].text
            print(result)
            dataArray.append(result)
        else:
                print(Back.RED + " - - Fail!")
                print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
                print(Style.RESET_ALL)
                dataArray.append("N/A")
    return dataArray

def scrapeMentalUnhealthyDays():
    dataArray = []
    xl = pandas.read_excel("2020-2023 RAM Clinic Locations (County-Level Data) (1).xlsx", sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print(" - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-outcomes/quality-of-life/poor-mental-health-days?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = 1.2
        r.html.render(timeout=25, sleep=sleeptime)
        if r.html.find("._chrr2022_measures__table") != []:
            result = r.html.find("._chrr2022_measures__table")[0].html
            soup = BeautifulSoup(result, 'html.parser')
            result = soup.findAll("td")[3].text
            print(result)
            dataArray.append(result)
        else:
                print(Back.RED + " - - Fail!")
                print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
                print(Style.RESET_ALL)
                dataArray.append("N/A")
    return dataArray

if __name__ == "__main__":
    # print(Back.GREEN + " = = = Getting Population Data = = = \n\n")
    # print(Style.RESET_ALL)
    # scrapeCensusPopulations()
    print(Back.GREEN + " = = = Getting Premature Death Data = = = \n\n")
    print(Style.RESET_ALL)
    scrapePrematureDeaths()
    print(Back.GREEN + " = = = Getting Physically Unhealthy Data = = = \n\n")
    print(Style.RESET_ALL)
    scrapePhysicalUnhealthyDays()
    print(Back.GREEN + " = = = Getting Mentally Unhealthy Data = = = \n\n")
    print(Style.RESET_ALL)
    scrapeMentalUnhealthyDays()
    