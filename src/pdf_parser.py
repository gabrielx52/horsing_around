"""Race results PDF parser."""
import os

TRACKS = ['AQU', 'BEL', 'KD', 'SA', 'SAR']

RES_DIR = os.path.abspath('./../results')


def pdf_parser(track_code):
    """Parse PDFs fpr race result data."""
    for pdf in os.listdir(RES_DIR + '/{}'.format(track_code)):
        yield pdf


def pdf_date_formater():
    """Change the PDF name format from M_D_Y to Y_M_D."""
    for track in TRACKS:
        sub_dir = RES_DIR + '/{}/'.format(track)
        for pdf in os.listdir(sub_dir):
            try:
                sn = pdf.rstrip('.pdf').split('_')
                new_name = '-'.join([sn[2],
                                     sn[0].rjust(2, '0'),
                                     sn[1].rjust(2, '0')]) + '.pdf'
                os.rename(sub_dir + pdf, sub_dir + new_name)
            except Exception as e:
                with open('./../results/error_log.txt', 'a+') as f:
                    f.write(pdf + ' ' + str(e) + '\n')
