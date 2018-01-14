"""Helper functions."""
import os


TRACKS = ['AQU', 'BEL', 'KD', 'SA', 'SAR']

RES_DIR = os.path.abspath('./../results')


def pdf_gen():
    """Generator that yields all results PDFs."""
    for track in TRACKS:
        t_dir = RES_DIR + '/{}'.format(track)
        for pdf in os.listdir(t_dir):
            if pdf.startswith('20'):
                yield t_dir + '/' + pdf


def delete_empty_pdfs():  # pragma: no cover
    """Delete PDFs if size is too small."""
    for pdf in pdf_gen():
        if os.path.getsize(pdf) < 15000:
            os.remove(pdf)


def pdf_date_formater():  # pragma: no cover
    """Change the PDF name format from Y_M_D to Y-M-D."""
    for track in TRACKS:
        sub_dir = RES_DIR + '/{}/'.format(track)
        for pdf in os.listdir(sub_dir):
            try:
                sn = pdf.rstrip('.pdf').split('_')
                new_name = '-'.join(sn) + '.pdf'
                os.rename(sub_dir + pdf, sub_dir + new_name)
            except Exception as e:
                with open('./../results/error_log.txt', 'a+') as f:
                    f.write(pdf + ' ' + str(e) + '\n')


def month_converter(month):
    """Convert month name string to number."""
    months = ['January', 'February', 'March', 'April', 'May',
              'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    return str(months.index(month) + 1).rjust(2, '0')
