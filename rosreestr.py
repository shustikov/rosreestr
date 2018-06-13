"""
main
"""
import os
import re
import glob
from shutil import copy

import zip_unpuck
from xml_unpuck import Responce
from mapping_for_report import RosReestrReport
from default_config import Config

class AppConfig(dict):
    def __init__(self, config_obj):
        dict.__init__(self, {})
        self.update(config_obj)

    def update(self, obj):
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))


class Rosreestr:
    def __init__(self, config_obj=None):
        self.config = AppConfig(Config)
        if config_obj is not None:
            self.config.update(config_obj)

    @staticmethod
    def _create_dir(dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    @staticmethod
    def _natural_sort_key(s):
        _nsre = re.compile('([0-9]+)')
        return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]

    def _init_dirs(self):
        self._create_dir(self.config['TMP_FOLDER'])
        self._create_dir(self.config['RES_FOLDER'])

    def clean_data(self):
        a = os.path.join(self.config['TMP_FOLDER'], '*.xml')
        [os.remove(i) for i in glob.glob(a)]
        a = os.path.join(self.config['SRC_FOLDER'], '*.zip')
        [os.remove(i) for i in glob.glob(a)]

    def parse(self):
        self._init_dirs()
        zip_unpuck.extract_xmls(self.config['SRC_FOLDER'], self.config['TMP_FOLDER'])
        list_xmls = glob.glob(self.config['TMP_FOLDER'] + '/*.xml')
        resp_list = []
        for path in list_xmls:
            try:
                r = Responce(path)
                resp_list += [r]
            except Exception:
                copy(path, self.config['RES_FOLDER'])
        resp_list = sorted(resp_list, key = lambda x:self._natural_sort_key(x.apartment))
        return resp_list

    def process_responces(self, responces):
        d = {}
        for resp in responces:
            if resp.street not in d.keys():
                d.update({resp.street : {resp.building : [resp]}})
            elif resp.building not in d[resp.street].keys():
                d[resp.street].update({resp.building : [resp]})
            else:
                d[resp.street][resp.building].append(resp)
        
        city = responces[0].city
        for street, street_resps in d.items():
            report_file = RosReestrReport(self.config['XLSX_TEMPLATE'], self.config['RES_FOLDER'], city, street)
            for building, building_resps in street_resps.items():
                report_file.add_worksheet(building_resps, building)
                [(resp.copy_to_addr(self.config['RES_FOLDER']),
                    resp.make_note(self.config['RES_FOLDER']),
                    resp.make_cn_note(self.config['RES_FOLDER'])) 
                    for resp in building_resps]
            report_file.close()
    
    def run(self):
        self.process_responces(self.parse())
        self.clean_data()


if __name__ == '__main__':
    app = Rosreestr()
    app.run()