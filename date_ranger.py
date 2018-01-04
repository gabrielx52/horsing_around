"""Date ranger."""

from datetime import date, timedelta

from time import sleep

from selenium import webdriver


def daterange(start_month, end_month):
    """Generate all dates in date range."""
    for year in list(range(2010, 2017)):
        start_date = date(year, start_month, 1)
        end_date = date(year, end_month, 1)
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)


# for sd in daterange(1, 4):
#     print(f'{sd.day}/{sd.month}/{sd.year}')


def month_converter(month):
    """Convert month name string to number."""
    months = ['January', 'February', 'March', 'April', 'May',
              'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    return months.index(month) + 1


# def download_pdf(date_gen):
def download_pdf():
    """PDF downloader using selenium."""
    lnk = "http://www.equibase.com/premium/eqbPDFChartPlus.cfm?\
RACE=A&BorP=P&TID=AQU&CTRY=USA&DT=11/09/2015&DAY=D&STYLE=EQB"
    options = webdriver.ChromeOptions()
    download_folder = "/Users/gabrielmeringolo/Python/day_at_the_races/pdfs"
    profile = {"plugins.plugins_list": [{"enabled": False,
                                         "name": "Chrome PDF Viewer"}],
               "download.default_directory": download_folder,
               "download.extensions_to_open": ""}
    options.add_experimental_option("prefs", profile)
    options.add_argument("user-data-dir=~/Users/gabrielmeringolo/\
        Library Application_Support/Google/Chrome/Default")
    print("Downloading file from link: {}".format(lnk))
    driver = webdriver.Chrome('/Users/gabrielmeringolo/Downloads/chromedriver',
                              chrome_options=options)
    driver.get(lnk)
    filename = 'test_data'
    print("File: {}".format(filename))
    print("Status: Download Complete.")
    print("Folder: {}".format(download_folder))
    sleep(5)
    driver.close()
