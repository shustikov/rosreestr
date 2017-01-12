# -*- coding: utf-8 -*- 
"""
main
"""


import zip_unpuck
import xml_unpuck
import glob
from shutil import copy
from paths import *
<<<<<<< HEAD
=======
from clean_data import clean_data
>>>>>>> report

print(zip_unpuck.extract_xmls(zips_folder, tmp_folder))
list_xmls = glob.glob(tmp_folder + '/*.xml')

test1 = []
for path in list_xmls:
	try:
		r = xml_unpuck.Responce(path)
		test1 += [r]
		
	except Exception:
		copy(path, res_folder)
		


test2 = sorted(test1, key = lambda x: x.apartment)
l = len([[print("{}, {}, {}, {}/{}, {} ".format(resp.apartment, resp.area, o_obj.fio, o_obj.share_numenator, o_obj.share_denuminator, o_obj.vouts)) for o_obj in resp.owner_objs] for resp in test2 if resp.apartment != 'None'])
print(l)
[(resp.copy_to_addr(res_folder), resp.make_note(), resp.make_cn_note()) for resp in test2 ]

<<<<<<< HEAD
=======
clean_data()

>>>>>>> report

