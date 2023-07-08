import requests
import requests_html
import time
import pandas
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from colorama import Fore, Back, Style

def createCsvWithData(array, csvname):
    df = pandas.DataFrame({'County': array.keys(), 'Data':array.values()})
    df.to_csv(csvname)
    print("\n\n"+Back.GREEN + " = = Successfully generated CSV File = = " + Style.RESET_ALL + "\n\n")

def insertIntoExcel(csvfile, url):
    print(Back.GREEN + " = = = Attempting to insert data into Excel doc... = = = " + Style.RESET_ALL + "\n")
    dataArray = []
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        first = 1
        counter = 0
        for row in csv_reader:
            if(first):
                first = 0
                counter +=1
                continue
            dataArray.append[row[2]]
            counter +=1
    xl = pandas.read_excel(url, sheet_name="2023 Clinics")
    j = 2
    for i in range(0, 66):
        xl.iloc[3, [j]] = dataArray[i]
        j+=7
    xl.to_excel(url)
    print(Back.GREEN + " = = = Success! = = = " + Style.RESET_ALL + "\n")

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
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0,len(counties) - 1):
        county = counties.iloc[i].values[0]
        arr = county.split(" ")
        arr[-1] = states[arr[-1]]
        county = "+".join(arr)
        county.replace(" ", "%20")
        urlTemplate = "https://data.census.gov/all?q="+county
        links.append(urlTemplate)
    return links

def scrapeCensusPopulations():
    dataArray = {}
    print(" - - Scraping Census Data - - ")
    links = generateCensusLinks()
    counter = 0
    for i in links:
        print("\n Source:",i)
        sleeptime = SLEEPTIME
        session = requests_html.HTMLSession()
        r = session.get(i)
        result = []
        while result == []:
            sleeptime *= 2
            r.html.render(timeout=25, sleep=sleeptime)
            result = r.html.find(".featured-result-value")[0].text
        print(" * * POPULATION: "+result+" * * ")
        session.close()
        dataArray[list(fipscodes.keys())[counter]] = int(result)
        counter += 1
    return dataArray

def generateFips(state):
    if state in fipscodes.keys():
         return fipscodes[state]
    stateoriginal = state
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
                   fipscodes[stateoriginal] = row[0]
                   return row[0]
              for i in state.split(" "):
                   if (i in row[1].upper() and (i != "COUNTY")):
                        fipscodes[stateoriginal] = row[0]
                        return row[0]
              
def scrapePrematureDeaths():
        dataArray = {}
        xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
        counties = xl.loc[1:]
        for i in range(0, len(counties) - 1):
            county = counties.iloc[i].values[0]
            print("("+str(i+1)+")"," - | Getting data for:",county+"...")
            fips = generateFips(county)
            # print("Generated fips: ", fips)
            testUrl = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-outcomes/length-of-life/premature-death?keywords=&f%5B0%5D=type%3Astates&f%5B1%5D=type%3Acounties&year=2023&county="+fips
            
            session = requests_html.HTMLSession()
            r = session.get(testUrl)
            result = []
            failcount = 1
            sleeptime = SLEEPTIME
            while r.html.find("._chrr2022_measures__measure-disaggregated-table-highlighted-row") == [] and failcount <= 3:
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
                    dataArray[county] = str(f'{result:,}')
                else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    failcount += 1
                    sleeptime *= 4
            if failcount >= 3:
                print(Back.RED + " - - Failed to scrape data")
                print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
                dataArray[county] = "N/A"
        return dataArray
    
def scrapePhysicalUnhealthyDays():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-outcomes/quality-of-life/poor-physical-health-days?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = "N/A"
    return dataArray

def scrapeMentalUnhealthyDays():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-outcomes/quality-of-life/poor-mental-health-days?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = "N/A"
    return dataArray

def scrapeDiabetes():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-outcomes/quality-of-life/diabetes-prevalence?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = "N/A"
    return dataArray

def scrapeNotPhysicallyActive():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-factors/health-behaviors/diet-and-exercise/physical-inactivity?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = "N/A"
    return dataArray

def scrapeAdultsSmoking():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-factors/health-behaviors/tobacco-use/adult-smoking?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = "N/A"
    return dataArray

def scrapeExcessiveDrinking():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-factors/health-behaviors/alcohol-and-drug-use/excessive-drinking?keywords=lake+county&f%5B0%5D=type%3Astates&f%5B1%5D=type%3Acounties&year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = result
    return dataArray

def scrapeHIV():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-outcomes/quality-of-life/hiv-prevalence?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",str(int(result/10)))
                dataArray[county] = str(int(result/10))
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = "N/A"
    return dataArray

def scrapeChlamydia():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-factors/health-behaviors/sexual-activity/sexually-transmitted-infections?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",str(int(result/10)))
                dataArray[county] = str(int(result/10))
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    # print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = "N/A"
    return dataArray

def scrapeBirthWeight():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-outcomes/quality-of-life/low-birthweight?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    # print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = result
    return dataArray

def scrapeTeenBirths():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-factors/health-behaviors/sexual-activity/teen-births?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",str(int(result) * 10))
                dataArray[county] = str(int(result) * 10)
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    # print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = "N/A"
    return dataArray

#Strange ratio, not sure how to convert?
def scrapePrimaryCarePhysicians():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-factors/clinical-care/access-to-care/primary-care-physicians?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    # print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = result
    return dataArray

#ditto
def scrapeMentalHealthProviders():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-factors/clinical-care/access-to-care/mental-health-providers?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    # print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = "N/A"
    return dataArray

#ditto x2
def scrapeDentistsData():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-factors/clinical-care/access-to-care/dentists?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    # print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = "N/A"
    return dataArray

def scrapeRecentMammograms():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-factors/clinical-care/quality-of-care/mammography-screening?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    # print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data")
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n" + Style.RESET_ALL)
            dataArray[county] = "N/A"
    return dataArray

def scrapeSomeCollege():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-factors/social-economic-factors/education/some-college?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    # print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data" + Style.RESET_ALL)
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
            dataArray[county] = "N/A"
    return dataArray

def scrapeSomeAssociations():
    dataArray = {}
    xl = pandas.read_excel(DATAURL, sheet_name="Counties of RAM Clinics", usecols="H")
    counties = xl.loc[1:]
    for i in range(0, len(counties) - 1):
        county = counties.iloc[i].values[0]
        print("("+str(i+1)+")"," - | Getting data for:",county+"...")
        fips = generateFips(county)
        # print("Generated fips: ", fips)
        url = "https://www.countyhealthrankings.org/explore-health-rankings/county-health-rankings-model/health-factors/social-economic-factors/family-and-social-support/social-associations?year=2023&county="+fips

        session = requests_html.HTMLSession()
        r = session.get(url)
        result = []
        sleeptime = SLEEPTIME
        failcount = 1
        while (r.html.find("._chrr2022_measures__table") == []) and failcount <= 3:
            r.html.render(timeout=25, sleep=sleeptime)
            if r.html.find("._chrr2022_measures__table") != []:
                result = r.html.find("._chrr2022_measures__table")[0].html
                soup = BeautifulSoup(result, 'html.parser')
                result = soup.findAll("td")[3].text
                print("("+str(i+1)+")"," - |",result)
                dataArray[county] = result
            else:
                    print(Back.RED + " - - Failed, trying again... ("+str(failcount)+")" + Style.RESET_ALL)
                    # print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
                    # print(Style.RESET_ALL)
                    failcount += 1
                    sleeptime *= 4
        if failcount >= 3:
            print(Back.RED + " - - Failed to scrape data" + Style.RESET_ALL)
            print(" * This is either due to a long page load causing a timeout, or the data is not available.\n")
            dataArray[county] = "N/A"
    return dataArray

# ABOVE THIS LINE IS ALL SAME WEBSITE

def scrapeMedianIncome():
    dataArray = {}
    print(" - - Scraping Census Data (Median Income) - - ")
    links = generateCensusLinks()
    counter = 0
    for i in links:
        print("\n ("+str(counter)+")","Source:",i)
        sleeptime = SLEEPTIME
        session = requests_html.HTMLSession()
        r = session.get(i)
        result = []
        while result == []:
            print("Waiting:",str(sleeptime)+"s")
            if sleeptime > 6:
                print(Back.RED + "Failed to load page in time due, skipping...")
                print(Style.RESET_ALL)
                dataArray[list(fipscodes.keys())[counter]] = "N/A"
                break
            sleeptime *= 2
            r.html.render(sleep=sleeptime)
            result = r.html.find(".teaser-description")
        if sleeptime > 6:
                 continue
        result = "$"+r.html.find(".teaser-description")[1].text.split("$")[1]
        print(result)
        print(list(fipscodes.keys())[counter], " = ", result)
        dataArray[list(fipscodes.keys())[counter]] = result
        counter += 1
        session.close()
    return dataArray

if __name__ == "__main__":
    global fipscodes
    fipscodes = {}
    global SLEEPTIME
    print(" - | Enter a time for the program to wait before pulling data. The larger the number the more successful hits (i've had the best result with 0.8)")
    SLEEPTIME = float(input(" >> "))
    global DATAURL
    print(" - | Enter the exact name of the excel file in the folder (i.e: \"data.xlsx\")")
    DATAURL = str(input(" >> "))


    # print(Back.GREEN + " = = = Getting Premature Death Data = = = \n\n" + Style.RESET_ALL)
    # prematureDeaths = scrapePrematureDeaths()

    print(Back.GREEN + " = = = Getting Physically Unhealthy Data = = = \n\n" + Style.RESET_ALL)
    physUnhealthy = scrapePhysicalUnhealthyDays()
    createCsvWithData(physUnhealthy, "Phyiscally Unhealthy Data")
    insertIntoExcel(DATAURL, "Phyiscally Unhealthy Data")

    # print(Back.GREEN + " = = = Getting Mentally Unhealthy Data = = = \n\n" + Style.RESET_ALL)
    # mentallyUnhealthy = scrapeMentalUnhealthyDays()

    # print(Back.GREEN + " = = = Getting Diabetes Data = = = \n\n" + Style.RESET_ALL)
    # diabetes = scrapeDiabetes()

    # print(Back.GREEN + " = = = Getting Not Physically Active Data = = = \n\n" + Style.RESET_ALL)
    # nonPhysical = scrapeNotPhysicallyActive()

    # print(Back.GREEN + " = = = Getting Adults Smoking Data = = = \n\n" + Style.RESET_ALL)
    # smokingAdults = scrapeAdultsSmoking()

    # print(Back.GREEN + " = = = Getting Excessive Drinking Data = = = \n\n" + Style.RESET_ALL)
    # excessDrinking = scrapeExcessiveDrinking()

    # print(Back.GREEN + " = = = Getting HIV Data = = = \n\n" + Style.RESET_ALL)
    # HIVPrevalence = scrapeHIV()

    # print(Back.GREEN + " = = = Getting Chlamydia Data = = = \n\n" + Style.RESET_ALL)
    # Chlamydia = scrapeChlamydia()

    # print(Back.GREEN + " = = = Getting Low Birthweight Data = = = \n\n" + Style.RESET_ALL)
    # birthWeight = scrapeBirthWeight()

    # print(Back.GREEN + " = = = Getting Teen Births Data = = = \n\n" + Style.RESET_ALL)
    # teenBirths = scrapeTeenBirths()

    # print(Back.GREEN + " = = = Getting Primary Care Physicians Data = = = \n\n" + Style.RESET_ALL)
    # primaryCare = scrapePrimaryCarePhysicians()

    # print(Back.GREEN + " = = = Getting Mental Health Provider Data = = = \n\n" + Style.RESET_ALL)
    # mentalCare = scrapeMentalHealthProviders()

    # print(Back.GREEN + " = = = Getting Dentists Data = = = \n\n" + Style.RESET_ALL)
    # dentists = scrapeDentistsData()

    # print(Back.GREEN + " = = = Getting Recent Mammograms Data = = = \n\n" + Style.RESET_ALL)
    # recentMammograms = scrapeRecentMammograms()

    # print(Back.GREEN + " = = = Getting Some College Data = = = \n\n" + Style.RESET_ALL)
    # someCollege = scrapeSomeCollege()
    # createCsvWithData(someCollege, "Some College Data")

    # print(Back.GREEN + " = = = Getting Some Associations Data = = = \n\n" + Style.RESET_ALL)
    # someAssociations = scrapeSomeAssociations()

    # print(Back.GREEN + " = = = Getting Population Data = = = \n\n" + Style.RESET_ALL)
    # populationData = scrapeCensusPopulations()
    # createCsvWithData(populationData, "Population Data")
    
    # print(Back.GREEN + " = = = Getting Median Household Income Data = = = \n\n" + Style.RESET_ALL)
    # medianIncome = scrapeMedianIncome()
    # print(medianIncome)