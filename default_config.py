import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SRC_FOLDER = os.path.join(BASEDIR,'src')
    RES_FOLDER = os.path.join(BASEDIR, 'res')
    TMP_FOLDER = os.path.join(BASEDIR, 'tmp')
    XLSX_TEMPLATE = os.path.join(BASEDIR, 'template.xlsx')