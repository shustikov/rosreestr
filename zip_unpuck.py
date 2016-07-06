# -*- coding: utf-8 -*- 

"""
"""

from paths import *
import zipfile
from io import BytesIO
import glob


def extract_xml(src_file_path, dtr_folder):
	zip = zipfile.ZipFile(src_file_path)
	name = zip.namelist()
	zfiledata = BytesIO(zip.read(name[0]))
	zip0 = zipfile.ZipFile(zfiledata)
	name =  zip0.namelist()
	# xml_file = BytesIO(zip0.read(name[0]))
	zip0.extract(name[0], dtr_folder)
	zip0.close()
	zip.close()
	# return xml_file

def extract_xmls(src_folder, dtr_folder):
	zips_list = glob.glob(src_folder + '/*.zip')
	[extract_xml(zip, dtr_folder) for zip in zips_list]
	return zips_list	
	
if __name__ == '__main__':
	print(extract_xmls(zips_folder, tmp_folder))
