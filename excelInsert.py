import pandas
from openpyxl.styles import Font, Color, colors, fills

def findPresent():
    url = "2020-2023 RAM Clinic Locations (County-Level Data) (1).xlsx"
    xl = pandas.read_excel(url, sheet_name="2023 Clinics")
    j = 2
    for i in range(0, 66):
        loc = xl.iloc[3, [j]]
        loc = 'TEST'
        loc.fill = fills.PatternFill(patternType='solid', fgColor=Color(rgb='00FF00'))
        print(loc)
        j+=7
    xl.to_excel(url)
if __name__ == "__main__":
    findPresent()