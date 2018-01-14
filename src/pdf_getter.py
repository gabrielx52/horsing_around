"""Package to download race results PDFs from equibase."""
from datetime import date, timedelta

import requests


TRACK_CODES = [('KD', 9, 10),
               ('SAR', 7, 10),
               ('BEL', 4, 8),
               ('SA', 1, 8),
               ('KEE', 4, 11),
               ('DMR', 7, 12),
               ('CD', 4, 12),
               ('AQU', 1, 5),
               ('AQU', 11, 12),
               ('OP', 1, 6)]


def date_range(start_month, end_month):
    """Generate all dates in date range."""
    for year in list(range(2010, 2017)):
        start_date = date(year, start_month, 1)
        end_date = date(year, end_month, 1)
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)


def url_gen():
    """Generate and return race results urls."""
    url = 'http://www.equibase.com/premium/eqbPDFChartPlus.cfm?'
    query = 'RACE=A&BorP=P&TID={}&CTRY=USA&DT={}/{}/{}&DAY=D&STYLE=EQB'
    for track in TRACK_CODES:
        dates = date_range(track[1], track[2])
        for d in dates:
            yield url + query.format(track[0], d.month,
                                     d.day, d.year), track[0], d


def pdf_getter():  # pragma: no cover
    """Download race results PDFs using requests lib."""
    for res in url_gen():
        url, track, d = res
        r = requests.get(url, headers={'User-agent': 'Wayne Mazerati'})
        while r.headers['Content-Type'] != 'application/pdf':
            input('Check for captcha\nPress any key to continue')
            r = requests.get(url, headers={'User-agent': 'Wayne Mazerati'})
        if len(r.content) > 15000:
            file = '../results/{}/{}.pdf'.format(track, d)
            with open(file, 'wb') as f:
                f.write(r.content)
                print('Saved race data for {} on {}'.format(track, d))
