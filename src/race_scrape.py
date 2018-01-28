"""Package to scrape all the race results PDFs."""
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
