"""Race results PDF parser."""
import os
import re

from datetime import datetime

from PyPDF2 import PdfFileReader

from helpers import month_converter, pdf_gen

TRACKS = ['AQU', 'BEL', 'KD', 'SA', 'SAR']

RES_DIR = os.path.abspath('./../results')


def pdf_to_text():
    """Parse PDFs fpr race result data."""
    for pdf in pdf_gen():
        with open(pdf, 'rb') as f:
            reader = PdfFileReader(f, strict=False)
            if reader.isEncrypted:
                reader.decrypt('')
            for i in range(reader.getNumPages()):
                content = reader.getPage(i)
                yield content.extractText()


def single_pdf_to_text():
    """Parse PDFs fpr race result data."""
    with open('/Users/gabrielmeringolo/Python/day_at_the_races/results/AQU/2010-11-24.pdf', 'rb') as f:
        reader = PdfFileReader(f, strict=False)
        if reader.isEncrypted:
            reader.decrypt('')
        for i in range(reader.getNumPages()):
            content = reader.getPage(i)
            yield content.extractText()


def page_parser():
    """Parse race result pages."""
    for page in pdf_to_text():
        try:
            results = {}
            track_date = re.search(".*(?=-Race)", page).group(0).split('-')
            results['Track'] = track_date[0]
            results['Date'] = date_format(track_date[1])
            results['RaceNum'] = int(re.search('(?<=Race)(\d+)', page).group(0))
            if 'DeadHeats:\n1stplace' in page:
                with open('./../results/error_log.txt', 'a+') as f:
                    f.write('DEAD HEAT: ' + str(results) + '\n')
                continue
            results['Winner'] = re.search('(?<=Winner:\\n).[^,]*', page).group(0)
            results['HorseNum'] = number_finder(page, results['Winner'])
            try:
                int(results['HorseNum'])
            except ValueError:
                if results['HorseNum'][-1] in ['A', 'B', 'X']:
                    pass
                else:
                    with open('./../results/error_log.txt', 'a+') as f:
                        f.write('SLOTNUM ERR: ' + str(results) + '\n')
                    continue
            results['Odds'] = float(re.search('\\n[0-9]+\.[0-9]+', page).group(0).lstrip('\n'))
            if len(results['HorseNum']) < 6:
                yield results
            else:
                with open('./../results/error_log.txt', 'a+') as f:
                    f.write('PARSE ERR: ' + str(results) + '\n')
                continue
        except AttributeError:  # pragma: no cover
            pass
        except Exception as e:  # pragma: no cover
            with open('./../results/error_log.txt', 'a+') as f:
                f.write('PP ERR: ' + str(type(e).__name__) + str(results) + '\n')


# def dq_checker():
#     """Check if winning horse was disqualified."""
#     if 'Disqualification(s):\n#'


def date_format(raw_date):
    """Format regexed date to Y-M-D."""
    split_date = re.split('(\d+)', raw_date)
    mth, dy, yr = map(split_date.__getitem__, [0, 1, 3])
    d_str = '{} {} {}'.format(yr, month_converter(mth), dy.rjust(2, '0'))
    return datetime.strptime(d_str, "%Y %m %d")


def number_finder(page, horse):
    """Extract horse number with regex."""
    if 'WinPlaceShow' in page:
        return re.search('(?<=WinPlaceShow\\n).[^{}]*'.format(horse), page).group(0)
    elif 'WinPlace' in page:
        return re.search('(?<=WinPlace\\n).[^{}]*'.format(horse), page).group(0)


def num_checker(num):
    """Check if number is valid."""
    try:
        int(num)
        return num
    except ValueError:
        if num[-1] in ['A', 'B', 'X']:
            return num
        else:
            pass
