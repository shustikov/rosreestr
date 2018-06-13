# -*- coding: utf-8 -*- 

"""
Модуль располагает xml в папки по домам.
"""

from shutil import copyfile
import os
import zipfile
import xml.etree.ElementTree as etree
import glob
import sys

default_mapping = {
	"city" : ('.//adrs:City', 'Name'),
	"street" : ('.//adrs:Street', 'Name'),
	"building" : ('.//adrs:Level1', 'Value'),
	"building1" : ('.//adrs:Level2', 'Value'),
	"floor" : ('xmlns:Realty/xmlns:Flat/xmlns:PositionInObject/xmlns:Levels/xmlns:Level', 'Number'),
	"apartment" : ('.//adrs:Apartment', 'Value'),
	"addr" : ('.//adrs:Note', None),
	"c_num" : ('xmlns:Realty/xmlns:Flat', 'CadastralNumber'),
	"area" : ('xmlns:Realty/xmlns:Flat/xmlns:Area', None)
}

mapping_options = {}
mapping_options['kpoks'] = default_mapping

mapping_options['kvzu'] = dict(default_mapping)
mapping_options['kvzu'].update({
	"c_num" : ('xmlns:Parcels/xmlns:Parcel', 'CadastralNumber'),
	"area" : ('xmlns:Parcels/xmlns:Parcel/xmlns:Area/xmlns:Area', None)
})

mapping_options['kvoks'] = dict(default_mapping)
mapping_options['kvoks'].update({
	"c_num" : ('xmlns:Realty/xmlns:Building', 'CadastralNumber'),
	"area" : ('xmlns:Realty/xmlns:Building/xmlns:Area', None)
})

defaults = {
	'floor' : '-',
	'city' : 'Город не указан',
	'street' : 'Улица не указана',
	'building' : 'None',
	'apartment' : 'None'
}

namespaces_options = {}
namespaces_options['kpoks'] = {
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

namespaces_options['kvzu'] = {
	"xmlns":"urn://x-artefacts-rosreestr-ru/outgoing/kvzu/7.0.1",
	"smev":"urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1",
	"num":"urn://x-artefacts-rosreestr-ru/commons/complex-types/numbers/1.0",
	"adrs":"urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1",
	"spa":"urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/5.0.1",
	"cer":"urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0",
	"doc":"urn://x-artefacts-rosreestr-ru/commons/complex-types/document-output/4.0.1",
	"nobj":"urn://x-artefacts-rosreestr-ru/commons/complex-types/natural-objects-output/1.0.1"
}

namespaces_options['kvoks'] = {
    "xmlns":"urn://x-artefacts-rosreestr-ru/outgoing/kvoks/3.0.1",
    "smev":"urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1",
    "num":"urn://x-artefacts-rosreestr-ru/commons/complex-types/numbers/1.0",
    "adrs":"urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1",
    "spa":"urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/5.0.1",
    "param":"urn://x-artefacts-rosreestr-ru/commons/complex-types/parameters-oks/2.0.1",
    "cer":"urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0",
    "doc":"urn://x-artefacts-rosreestr-ru/commons/complex-types/document-output/4.0.1",
    "ch":"urn://x-artefacts-rosreestr-ru/commons/complex-types/cultural-heritage/2.0.1"
}


def checkfile(path):
	"""
	Добавляет инкремент в путь, если файл существует
	"""
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
	def __init__(self, right_node, namespaces):
		
		self.f_name = right_node.find('xmlns:Owners/xmlns:Owner/xmlns:Person/xmlns:FirstName', namespaces).text if right_node.find('xmlns:Owners/xmlns:Owner/xmlns:Person/xmlns:FirstName', namespaces) is not None else 'None'
		self.l_name = right_node.find('xmlns:Owners/xmlns:Owner/xmlns:Person/xmlns:FamilyName', namespaces).text if right_node.find('xmlns:Owners/xmlns:Owner/xmlns:Person/xmlns:FamilyName', namespaces) is not None else 'None'
		self.s_name = right_node.find('xmlns:Owners/xmlns:Owner/xmlns:Person/xmlns:Patronymic', namespaces).text if right_node.find('xmlns:Owners/xmlns:Owner/xmlns:Person/xmlns:Patronymic', namespaces) is not None else 'None'
		self.fio = "{} {} {}".format(self.l_name, self.f_name, self.s_name)

		self.regnumber = right_node.find('xmlns:Registration/xmlns:RegNumber', namespaces).text if right_node.find('xmlns:Registration/xmlns:RegNumber', namespaces) is not None else 'None'
		self.regdate = right_node.find('xmlns:Registration/xmlns:RegDate', namespaces).text if right_node.find('xmlns:Registration/xmlns:RegDate', namespaces) is not None else 'None'
		self.share_numenator = int(right_node.find('xmlns:Registration/xmlns:Share', namespaces).get('Numerator')) if right_node.find('xmlns:Registration/xmlns:Share', namespaces) is not None else None
		self.share_denuminator = int(right_node.find('xmlns:Registration/xmlns:Share', namespaces).get('Denominator')) if right_node.find('xmlns:Registration/xmlns:Share', namespaces) is not None else None
		self.share = self.share_numenator if self.share_numenator is not None else "-"
		self.share = self.share + "/" + self.share_denuminator if self.share_denuminator is not None else self.share


	def __repr__(self):
		return "{} - {}\{}".format(self.fio, self.share_numenator, self.share_denuminator)


	def set_vouts_count(self, vouts):
		self.vouts = vouts
		return vouts

		
class AltOwner(Owner):
	"""
	Владелец недвижимого имущества
	"""
	def __init__(self, right_node, owner_node, namespaces):
		self.f_name = owner_node.find('xmlns:Person/xmlns:FIO/xmlns:First', namespaces).text if owner_node.find('xmlns:Person/xmlns:FIO/xmlns:First', namespaces) is not None else None
		self.l_name = owner_node.find('xmlns:Person/xmlns:FIO/xmlns:Surname', namespaces).text if owner_node.find('xmlns:Person/xmlns:FIO/xmlns:Surname', namespaces) is not None else None
		self.s_name = owner_node.find('xmlns:Person/xmlns:FIO/xmlns:Patronymic', namespaces).text if owner_node.find('xmlns:Person/xmlns:FIO/xmlns:Patronymic', namespaces) is not None else None

		if any((self.l_name, self.f_name, self.s_name)):
			self.fio = "{} {} {}".format(self.l_name or '', self.f_name or '', self.s_name or '')

		elif owner_node.find('xmlns:Content', namespaces) is not None:
			self.fio = owner_node.find('xmlns:Content', namespaces).text
		
		elif owner_node.find('xmlns:Organization/xmlns:Content', namespaces) is not None:
			self.fio = owner_node.find('xmlns:Organization/xmlns:Content', namespaces).text
		
		else:
			self.fio = 'Собственик не определён'

		self.regnumber = right_node.find('xmlns:Registration/xmlns:RegNumber', namespaces).text if right_node.find('xmlns:Registration/xmlns:RegNumber', namespaces) is not None else 'None'
		self.regdate = right_node.find('xmlns:Registration/xmlns:RegDate', namespaces).text if right_node.find('xmlns:Registration/xmlns:RegDate', namespaces) is not None else 'None'
		self.share = right_node.find('xmlns:Registration/xmlns:ShareText', namespaces).text if right_node.find('xmlns:Registration/xmlns:ShareText', namespaces) is not None else None
		
		if self.share:
			if '/' in self.share:
				self.share_numenator, self.share_denuminator = map(int, self.share.split('/'))
			
			else:
				self.share_numenator, self.share_denuminator = 1

		else:
			self.share_numenator = int(right_node.find('xmlns:Share', namespaces).get('Numerator')) if right_node.find('xmlns:Share', namespaces) is not None else None
			self.share_denuminator = int(right_node.find('xmlns:Share', namespaces).get('Denominator')) if right_node.find('xmlns:Share', namespaces) is not None else None
			self.share = self.share_numenator if self.share_numenator is not None else "-"
			self.share = self.share + "/" + self.share_denuminator if self.share_denuminator is not None else self.share


				
class Empty_Owner(Owner):
	"""
	Объект владельца, если ни одного не указано
	"""
	def __init__(self):
		empty_element = etree.Element("")
		Owner.__init__(self, empty_element, {"xmlns":""})
		self.fio = "Собственники не указаны"


class Responce:
	"""
	Объект ответа представляющий xml
	"""

	def __init__(self, path):
		self.path = path
		tree = etree.parse(path)
		root = tree.getroot()
		self.root = root
		type = root.tag.split('/')[-2]
		self.namespaces = namespaces_options.get(type)
		mapping = mapping_options.get(type, default_mapping)
		self._map_values(root, mapping)
		self.building1 = "" if self.building1 is None else "-{self.building1}".format(self=self)
		self.addr = self.addr or 'ул. {self.street}, д.{self.building}{self.building1}, кв.{self.apartment}'.format(self=self)
		[print("{} :   {}".format(k,v)) for k,v in self.__dict__.items()]
		self.area = float(self.area)
		self.define_users()
		self.define_paths()

	def _map_values(self, node, mapping):
		for key, value in mapping.items(): 
			k, v  = key, self._get_value(node, *value) or defaults.get(key)
			self.__dict__.update({k:v})

	def _get_value(self, root, path, attr=None):
		"""
		if attr == None returns TEXT value
		"""
		node = root.find(path, self.namespaces)
		if node is None:
			return None
		else:
			return node.text if attr == None else node.get(attr)

	def __repr__(self):
		return self.addr 


	def define_users(self):
		list_rn = self.root.findall('xmlns:ReestrExtract/xmlns:ExtractObjectRight/xmlns:ExtractObject/xmlns:ObjectRight/xmlns:Right', self.namespaces)
		self.owner_objs = [] 
		for right_node in list_rn:
			owner_nodes = right_node.findall('xmlns:Owner', self.namespaces)
			if len(owner_nodes) > 0: self.owner_objs += [AltOwner(right_node, owner_node, self.namespaces) for owner_node in owner_nodes]
		
		if len(self.owner_objs)== 0:
			list_rn = self.root.findall('xmlns:Realty/xmlns:Flat/xmlns:Rights/xmlns:Right', self.namespaces)
			self.owner_objs = [Owner(right_node, self.namespaces) for right_node in list_rn]
			
		if len(self.owner_objs) == 0: self.owner_objs.append(Empty_Owner())
		self.count_vouts()		
	

	def define_paths(self):
		self.new_path = self.city.replace('/', '-')+ '/' + self.street.replace('/', '-') + '/' + self.building.replace('/', '-') + self.building1.replace('/', '-') 
		self.filename = self.apartment if self.apartment != 'None' else str(self.area) + '-' + self.c_num.replace(':', '!')
   

	def copy_to_addr(self, res_folder):
		"""
		Копирует xml файл в папку соответствующую адресу объекта
		"""
		os.makedirs(res_folder + '/' + self.new_path, exist_ok=True)
		file_path = res_folder + '/' + self.new_path + '/' + self.filename + '.xml'
		copyfile(self.path, checkfile(file_path))
	

	def count_vouts(self): 
		"""
		Считает голоса владельцев, согласно доле площади, которой они владеют  
		"""
		owners_count = len(self.owner_objs)
		s = 0

		for owner in self.owner_objs:
			if all((owner.share_numenator, owner.share_denuminator)):
				s += owner.set_vouts_count(round((self.area * owner.share_numenator) / owner.share_denuminator, 3))

			elif any((owner.share_numenator, owner.share_denuminator)):
				owner.set_vouts_count(None)	

			else:
				s += owner.set_vouts_count(round(self.area / owners_count, 3))


		

	def make_note(self, res_folder):
		"""
		Создаёт в папке дома csv файл с записями владельцев 
		"""
		file_path = res_folder + '/' + self.new_path
		os.makedirs(file_path, exist_ok=True)
		file_name = "{}, {}{}.csv".format(self.street.replace('/', '-'), self.building.replace('/', '-'), self.building1.replace('/', '-'))
		with open(file_path + '/' + file_name, 'a+') as f:
			for o_obj in self.owner_objs:
				print("{}; {}; {}; {}, {}; {}".format(self.apartment, self.area, o_obj.fio, o_obj.regnumber, o_obj.regdate, o_obj.vouts or "None").encode(sys.stdout.encoding, errors='replace'), file = f)


	def make_cn_note(self, res_folder):
		"""
		Создаёт в папке результата csv файл с кадастровыми номерами объектов
		"""
		file_path = res_folder
		os.makedirs(file_path, exist_ok=True)
		file_name = "CNs.csv"
		with open(file_path + '/' + file_name, 'a+') as f:
			print("{}; {}; {}{}; {}; {}".format(self.addr, self.street, self.building, self.building1, self.apartment, self.c_num), file = f)


if __name__ == '__main__':
	tmp_folder = os.path.join(os.path.curdir, 'tmp')
	res_folder = os.path.join(os.path.curdir, 'res')
	
	list_xmls = glob.glob(tmp_folder + '/*.xml')
	test_obj = Responce(list_xmls[0])
	test_obj.copy_to_addr(res_folder)
	test_obj.make_cn_note(res_folder)
	test_obj.make_note(res_folder)
	print(test_obj)
	
	# def process_xml(path):
		# test_obj = Responce(path)
		# test_obj.copy_to_addr(res_folder)
		# test_obj.make_cn_note(res_folder)
		# test_obj.make_note(res_folder)
		# print(test_obj)
	
	# list(map(process_xml, list_xmls))
	

