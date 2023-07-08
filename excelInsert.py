import pandas

def findPresent():
    url = "2020-2023 RAM Clinic Locations (County-Level Data) (1).xlsx"
    xl = pandas.read_excel(url, sheet_name="2023 Clinics")
    j = 2
    for i in range(0, 66):
        xl.iloc[3, [j]] = 'TEST'
        print(xl.iloc[3, [j]])
        j+=7
    xl.to_excel(url)
if __name__ == "__main__":
    findPresent()