"""Package to scrape all the race results PDFs."""
import os
import time

from datetime import date, timedelta

from bs4 import BeautifulSoup as Soup

import requests


def date_range_1991_to_2017():
    """Generate all dates from 1991 to 2017."""
    # start_date = date(1991, 1, 1)
    start_date = date(2015, 1, 10)

    end_date = date(2018, 1, 1)
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def historical_url_gen():
    """Url generator."""
    url = 'http://www.equibase.com/premium/eqpVchartBuy.cfm?'
    query = 'mo={}&da={}&yr={}&trackco=ALL;ALL&cl=Y'
    dates = date_range_1991_to_2017()
    for d in dates:
        yield url + query.format(d.month, d.day, d.year)


def first_parser():  # pragma: no cover
    """Initial parse of table extracting url for second round."""
    root_url = 'http://www.equibase.com/premium/{}'
    count = 1
    with open('./first_urls.txt', 'a+') as f:
        for url in historical_url_gen():
            print(round(100 * float(count) / float(1114), 2))
            count += 1
            r = requests.get(url, headers={'User-agent': 'Bruce Pfiffer'})
            while r.status_code != 200:
                input('Check for captcha\nPress any key to continue')
                r = requests.get(url, headers={'User-agent': 'Bruce Pfiffer'})
            fs = Soup(r.content, 'html.parser').find('table')
            for a in fs.find_all('a'):
                f.write(root_url.format(a.attrs['href']) + '\n')


def second_parser():
    """Second parse."""
    root_url = 'http://www.equibase.com{}'
    urls = first_parser()
    for url in urls:
        time.sleep(1)
        r = requests.get(url, headers={'User-agent': 'Wayne Mazerati'})
        while r.status_code != 200:
            input('Check for captcha\nPress any key to continue')
            r = requests.get(url, headers={'User-agent': 'Wayne Mazerati'})
        s = Soup(r.content, 'html.parser').find('a', class_='dkbluesm').attrs['href']
        yield root_url.format(s)


def race_dict_maker():
    """Populate dictonary with race info from urls."""
    ret_d = {}
    with open('first_urls.txt', 'r') as f:
        for line in f:
            _, tc, dt, cc = line.split('=')
            tc = tc.split('&')[0]
            dt = dt.split('&')[0]
            cc = cc.strip()
            ret_d.setdefault(tc + '|' + cc, []).append(dt)
    with open('race_dates.txt', 'a') as f:
        f.write(str(ret_d))


def race_data_reader():
    """Parse race data dict and extract info."""
    from race_dict import race_dict as rd
    return list(rd.keys())


tcs = ['BM|USA', 'CRC|USA', 'ELC|PR', 'LRL|USA', 'LA|USA', 'MNR|USA',
       'PHA|USA', 'RKM|USA', 'SA|USA', 'SUN|USA', 'TUP|USA', 'TP|USA',
       'AQU|USA', 'FG|USA', 'CT|USA', 'PEN|USA', 'TAM|USA', 'DED|USA',
       'BEU|USA', 'PM|USA', 'YM|USA', 'ALB|USA', 'AC|USA', 'GP|USA',
       'RM|USA', 'GG|USA', 'OP|USA', 'BRD|USA', 'GS|USA', 'RP|USA',
       'FON|USA', 'MAN|USA', 'SPT|USA', 'BND|USA', 'PRM|USA', 'TDN|USA',
       'CLG|CAN', 'OTC|USA', 'PIM|USA', 'DET|USA', 'DEL|USA', 'DUN|USA',
       'GRD|CAN', 'AIK|USA', 'FL|USA', 'STP|CAN', 'CAM|USA', 'SAF|USA',
       'LGA|USA', 'JND|USA', 'KEE|USA', 'ATH|USA', 'EVD|USA', 'LBT|USA',
       'SUD|USA', 'EP|CAN', 'FP|USA', 'DG|USA', 'GTW|USA', 'MON|USA',
       'OXM|USA', 'SOP|USA', 'SH|USA', 'DIX|USA', 'EMT|USA', 'GN|USA',
       'RD|USA', 'TRY|USA', 'DUE|USA', 'MID|USA', 'JRM|USA', 'HOL|USA',
       'CBY|USA', 'LAD|USA', 'SJD|USA', 'CD|USA', 'FX|USA', 'GLN|USA',
       'HLN|USA', 'SON|USA', 'ASD|CAN', 'FE|CAN', 'LEX|USA', 'WO|CAN',
       'AKS|USA', 'BOI|USA', 'GRM|USA', 'MD|CAN', 'MPM|USA', 'STL|USA',
       'BEL|USA', 'RUI|USA', 'BCF|USA', 'CLM|USA', 'MOF|USA', 'PW|USA',
       'WW|USA', 'AP|USA', 'PRP|USA', 'WTS|USA', 'KAM|CAN', 'MAL|USA',
       'MOR|USA', 'PIC|CAN', 'TS|CAN', 'PPK|USA', 'GRP|USA', 'WDS|USA',
       'DAY|USA', 'GIL|USA', 'GF|USA', 'POD|USA', 'PRE|USA', 'PRO|USA',
       'WYO|USA', 'RDA|CAN', 'FAI|USA', 'TRM|USA', 'MTH|USA', 'NP|CAN',
       'RDP|CAN', 'SWF|USA', 'ATL|USA', 'UN|USA', 'ATO|USA', 'MLO|CAN',
       'STK|USA', 'SDY|USA', 'DEP|CAN', 'SFE|USA', 'VEG|CAN', 'MDA|CAN',
       'WCD|USA', 'PLN|USA', 'ED|USA', 'LAM|USA', 'SND|CAN', 'MIL|CAN',
       'ELP|USA', 'FLG|USA', 'RUP|USA', 'GPR|CAN', 'KIN|CAN', 'RPD|CAN',
       'SOL|USA', 'PRV|USA', 'PLA|USA', 'WBR|USA', 'MAF|USA', 'KLF|USA',
       'FMT|USA', 'SAR|USA', 'SR|USA', 'DMR|USA', 'HAP|USA', 'ONE|USA',
       'BMF|USA', 'FER|USA', 'MEP|USA', 'CWF|USA', 'KSP|USA', 'LBG|CAN',
       'WRD|USA', 'LNN|USA', 'MF|USA', 'CAS|USA', 'SAL|USA', 'WPR|USA',
       'SAC|USA', 'WMF|USA', 'TIM|USA', 'ELK|USA', 'RAV|USA', 'NMP|USA',
       'MAS|USA', 'BKF|USA', 'MED|USA', 'AVN|USA', 'HCF|USA', 'HOB|USA',
       'CLS|USA', 'FPX|USA', 'GBF|USA', 'SJM|USA', 'SJ|USA', 'FAX|USA',
       'FNO|USA', 'GCF|USA', 'HAW|USA', 'BGD|USA', 'GV|USA', 'RB|USA',
       'YMA|USA', 'MAR|USA', 'FH|USA', 'SAN|CAN', 'MTP|USA', 'UNI|USA',
       'PMT|USA', 'CHA|USA', 'HIA|USA', 'SUF|USA', 'FTP|USA', 'BIR|USA',
       'MC|USA', 'ARP|USA', 'FOX|USA', 'QD|USA', 'TIL|USA', 'RIL|USA',
       'PPM|USA', 'BRO|USA', 'MUS|USA', 'MGO|USA', 'WIL|USA', 'TRO|CAN',
       'CPW|USA', 'ANF|USA', 'SPG|USA', 'ROP|USA', 'HST|CAN', 'HOU|USA',
       'EUR|USA', 'YKT|CAN', 'RET|USA', 'HOO|USA', 'CHL|USA', 'EMD|USA',
       'DXD|USA', 'LS|USA', 'YD|USA', 'CNL|USA', 'HPO|USA', 'KD|USA',
       'QBY|CAN', 'GLD|USA', 'SRP|USA', 'LEV|USA', 'STN|USA', 'YAV|USA',
       'BF|USA', 'SHW|USA', 'BRN|USA', 'IND|USA', 'FAR|USA', 'RDM|USA',
       'FPL|USA', 'ZIA|USA', 'OSA|USA', 'OKR|USA', 'WNT|USA', 'AJX|CAN',
       'CMR|PR', 'ELY|USA', 'PID|USA', 'PNL|USA', 'PMB|USA', 'OTH|USA',
       'PRX|USA', 'ABT|CAN', 'BHP|USA', 'BSR|USA', 'BTP|USA', 'OTP|USA',
       'HP|USA', 'LRC|USA', 'GPW|USA', 'MVR|USA', 'CTD|CAN']


def race_dict_value_getter():
    """Return value from race dict for key."""
    trk_key = ['CTD|CAN']
    from race_dict import race_dict as rd
    for key in trk_key:
        yield rd[key]


def make_track_folders():
    """Make folders for all the tracks."""
    for code in tcs:
        tc, _ = code.split('|')
        os.makedirs('./../total_res/{}'.format(tc))
