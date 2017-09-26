# -*- coding: utf-8 -*- 

"""
Модуль располагает xml в папки по домам.
"""

from shutil import copyfile
import os
import zipfile
import xml.etree.ElementTree as etree
import glob

def checkfile(path):
	'''
	добавляет инкремент в путь, если файл существует
	'''
	if not os.path.exists(path):
		return path

	root, ext = os.path.splitext(path)
	dir = os.path.dirname(root)
	fname = os.path.basename(root)
	candidate = fname + ext
	index = 0
	ls = set(os.listdir(dir))
	while candidate in ls:
		candidate = "{}_{}{}".format(fname,index,ext)
		index += 1	
	return os.path.join(dir,candidate)
	
class Owner:
	"""
	Владелец недвижимого имущества
	"""
	def __init__(self, right_node):
		self.fio = right_node.find('.//Owner/Person/Content').text.strip() if right_node.find('.//Owner/Person/Content') is not None else 'None'
		self.regnumber = right_node.find('.//Registration/RegNumber').text if  right_node.find('.//Registration/RegNumber') is not None else 'None'
		self.regdate = right_node.find('.//Registration/RegDate').text if  right_node.find('.//Registration/RegDate') is not None else 'None'
		self.share_numenator = int(right_node.find('.//Registration/Share').get('Numerator')) if right_node.find('.//Registration/Share') is not None else 1
		self.share_denuminator = int(right_node.find('.//Registration/Share').get('Denominator')) if right_node.find('.//Registration/Share') is not None else 1
	
	def __repr__(self):
		return "{} - {}\{}".format(self.fio, self.share_numenator, self.share_denuminator)

	def set_vouts_count(self, vouts):
		self.vouts = vouts
		return vouts
		

class Responce:
	"""
	Объект ответа представляющий xml
	"""
	def __init__(self, path):
	    self.path = path
		tree = etree.parse(self.path)
		root = tree.getroot()
		
		namespaces= {
		"xmlns":"urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1",
        "smev":"urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1",
        "num":"urn://x-artefacts-rosreestr-ru/commons/complex-types/numbers/1.0",
        "adrs":"urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1",
        "spa":"urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/5.0.1",
        "param":"urn://x-artefacts-rosreestr-ru/commons/complex-types/parameters-oks/2.0.1",
        "cer":"urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0",
        "doc":"urn://x-artefacts-rosreestr-ru/commons/complex-types/document-output/4.0.1",
        "flat":"urn://x-artefacts-rosreestr-ru/commons/complex-types/assignation-flat/1.0.1",
        "ch":"urn://x-artefacts-rosreestr-ru/commons/complex-types/cultural-heritage/2.0.1"
		}
		
		xpath = 'xmlns:Realty/xmlns:Flat/xmlns:Address'
		res = root.find(xpath, namespaces)
		self.addr = res.find('adrs:Note', namespaces).text
		self.street = res.find('adrs:Street', namespaces).get('Name')
		self.building = res.find('adrs:Level1', namespaces).get('Value')
		self.building1 = '-' + res.find('adrs:Level2', namespaces).get('Value') if res.find('adrs:Level2', namespaces) is not None else ''  
		self.apartment = res.find('adrs:Apartment', namespaces).get('Value') if res.find('adrs:Apartment', namespaces) is not None else 'None' 
		
		self.c_num = root.find('xmlns:Realty/xmlns:Flat', namespaces).get("CadastralNumber")
		
		#self.resp_num = root.find('.//DeclarAttribute', namespaces).get('ExtractNumber', namespaces)
		#self.resp_date = root.find('.//DeclarAttribute', namespaces).get('ExtractDate', namespaces)
		self.area = float(root.find('xmlns:Realty/xmlns:Flat/xmlns:Area').text)
		#owners = root.findall('.//Right/Owner/Person/Content')	
		#self.owners = [owner.text for owner in owners] if root.find('.//Right/Owner/Person/Content') is not None else ['None']
		
		list_rn = root.findall('.//Right')
		self.owner_objs = [Owner(right_node) for right_node in list_rn]
		self.count_vouts()
		self.define_paths()
		
	def __repr__(self):
		return self.addr
		
	def define_paths(self):

		self.new_path = self.street + '/' +  self.building.replace('/', '-') + self.building1.replace('/', '-') 
		self.filename = self.apartment if self.apartment != 'None' else  str(self.area) + '-' + self.c_num.replace(':', '!')
    	
	def copy_to_addr(self, res_folder):
		'''
		Копирует xml файл в папку соответствующую адресу объекта
		'''
		os.makedirs(res_folder + '/' + self.new_path, exist_ok=True)
		file_path = res_folder + '/' + self.new_path + '/' + self.filename + '.xml'
		copyfile(self.path, checkfile(file_path))
	
	def count_vouts(self):
		"""
		Считает голоса владельцев, согласно доле площади, которой они владеют  
		"""
		# найти наименьеше общее кратное (НОК) знаменателей (denumenator)
		# найти дополнительный множитель для кажой доли
		# домножить числители (numenator) на дополнительные множители
		# сложить числители
		# сравнить сумму числителей с НОК
		# если сумма == НОК то
		s = sum([o.set_vouts_count(round((self.area * o.share_numenator) / o.share_denuminator, 1)) for o in self.owner_objs[:-1]])
		self.owner_objs[-1].set_vouts_count(round(self.area - s, 1))
		
	def make_note(self):
		"""
		Создаёт в папке дома csv файл с записями владельцев 
		"""
		file_path = res_folder + '/' + self.new_path
		os.makedirs(file_path, exist_ok=True)
		file_name = "{}, {}{}.csv".format(self.street, self.building.replace('/', '-'), self.building1.replace('/', '-'))
		with open(file_path + '/' + file_name, 'a+') as f:
			for o_obj in self.owner_objs:
				print("{}; {}; {}; {}, {}; {}".format(self.apartment, self.area, o_obj.fio, o_obj.regnumber, o_obj.regdate, o_obj.vouts), file = f)
	
	def make_cn_note(self):
		"""
		Создаёт в папке результата csv файл с кадастровыми номерами объектов
		"""
		file_path = res_folder
		os.makedirs(file_path, exist_ok=True)
		file_name = "CNs.csv"
		with open(file_path + '/' + file_name, 'a+') as f:
			print("{}; {}; {}{}; {}; {}".format(self.addr, self.street, self.building, self.building1, self.apartment, self.c_num), file = f)
		
  	
if __name__ == '__main__':
    from paths import *
	
    list_xmls = glob.glob(tmp_folder + '/*.xml')
	test = Responce(test_file)
	test.count_vouts()
	# test.make_note()
	
	print(test)
	print(test.owner_objs[0].regnumber, test.area, test.owner_objs[0].vouts)
	print('\n\n')
	
	test1 = [Responce(path) for path in list_xmls]
	print(test1[0].owners, test1[0].area)
	print('\n\n')
	test2 = sorted(test1, key = lambda x: x.apartment) 
	# l = len([print(resp.owner_objs, resp.area) for resp in test2 if len(resp.owners) > 1]) #выводит на печать квартиры
	# l = len([[print("{}, {}, {}, {}/{}".format(resp.area, o_obj.fio, o_obj.regnumber, o_obj.share_numenator, o_obj.share_denuminator)) for o_obj in resp.owner_objs] for resp in test2])
	l = len([[print("{}, {}, {}, {}/{}, {} ".format(resp.apartment, resp.area, o_obj.fio, o_obj.share_numenator, o_obj.share_denuminator, o_obj.vouts)) for o_obj in resp.owner_objs] for resp in test2 if resp.apartment != 'None'])
	print(l)
	
	[(resp.copy_to_addr(res_folder), resp.make_note()) for resp in test2 ]
	

	

