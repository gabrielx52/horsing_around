"""Date ranger."""

from datetime import timedelta, date
from selenium import webdriver
from time import sleep


def daterange(start_month, end_month):
    """Generate all dates in date range."""
    for year in list(range(2010, 2017)):
        start_date = date(year, start_month, 1)
        end_date = date(year, end_month, 1)
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)


# for sd in daterange(1, 4):
#     print(f'{sd.day}/{sd.month}/{sd.year}')


pdf_url = 'http://www.equibase.com/premium/eqbPDFChartPlus.cfm?\
RACE=A&BorP=P&TID=AQU&CTRY=USA&DT=11/08/2015&DAY=D&STYLE=EQB'


def download_pdf(lnk):
    """PDF downloader using selenium."""
    options = webdriver.ChromeOptions()
    download_folder = "/Users/gabrielmeringolo/Python/day_at_the_races/pdf_test"
    profile = {"plugins.plugins_list": [{"enabled": False,
                                         "name": "Chrome PDF Viewer"}],
               "download.default_directory": download_folder,
               "download.extensions_to_open": ""}
    options.add_experimental_option("prefs", profile)
    options.add_argument("user-data-dir=~/Users/gabrielmeringolo/Library Application_Support/Google/Chrome/Default")
    print("Downloading file from link: {}".format(lnk))
    driver = webdriver.Chrome('/Users/gabrielmeringolo/Downloads/chromedriver', chrome_options=options)
    driver.get(lnk)
    filename = 'test_data'
    print("File: {}".format(filename))
    print("Status: Download Complete.")
    print("Folder: {}".format(download_folder))
    driver.close()

download_pdf("http://www.equibase.com/premium/eqbPDFChartPlus.cfm?RACE=A&BorP=P&TID=AQU&CTRY=USA&DT=11/09/2015&DAY=D&STYLE=EQB")
