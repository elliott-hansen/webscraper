import pandas
from openpyxl.styles import Font, Color, colors, fills
import csv
import colorama

def inserIntoExcel(csvfile, url):
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
        loc = xl.iloc[3, [j]]
        loc = dataArray[i]
        print(loc)
        j+=7
    xl.to_excel(url)
    
if __name__ == "__main__":
    inserIntoExcel("Some College Data", "A")