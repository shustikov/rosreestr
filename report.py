# -*- coding: utf-8 -*- 

"""
Модуль создаёт xlsx отчёты
в именнованный масив xlsx "header" - помещаются данные из объекта header
в именнованный масив xlsx "data" - помещаются данные из списка объектов data
соответственно, содержащих поля, указанные в шаблоне в виде {data.field_name}
"""

import os.path
from copy import copy
from openpyxl import load_workbook
from openpyxl.formula import Tokenizer

class Report:

	def __init__(self, res_path, template_path):
		self.path = res_path
		self.workbook = load_workbook(template_path)
		self.tmpl_ws_name = self.workbook.active.title


	def copy_cell_style(new_cell, cell):
		if cell.has_style:	
			new_cell.font = copy(cell.font)
			new_cell.border = copy(cell.border)
			new_cell.fill = copy(cell.fill)
			new_cell.number_format = copy(cell.number_format)
			new_cell.protection = copy(cell.protection)
			new_cell.alignment = copy(cell.alignment)
	
	@classmethod
	def set_number_format(cls, cell):
		"""abstract"""
		pass			

	def _get_header_range(self, worksheet):
		tmpl_header_cells = self.workbook[self.tmpl_ws_name].get_named_range("header")
		res = [worksheet[c.coordinate] for c in tmpl_header_cells]
		return res


	def _get_data_range(self, worksheet):
		tmpl_data_cells = self.workbook[self.tmpl_ws_name].get_named_range("data")
		res = [worksheet[c.coordinate] for c in tmpl_data_cells]
		return res	
	

	def _fill_header(self, header, worksheet):
		cells = self._get_header_range(worksheet)		
		for cell in cells: 
			cell.value = cell.value.format(header=header)


	def _fill_data(self, data, worksheet):
		cells = self._get_data_range(worksheet)			
		for row in data:
			new_line = []
			
			for cell in cells:
				new_cell = cell.offset(1, 0)
				new_cell.value = cell.value
				Report.copy_cell_style(new_cell, cell)
				new_line.append(new_cell)
				cell.value = cell.value.format(data=row)
				self.set_number_format(cell)

			cells = new_line[:]

		for cell in cells:								#clear template data cells 
			cell.value = '' 	
			Report.copy_cell_style(cell, cell.offset(2, 0)) #fix

	def add_worksheet(self, header, data, page_name):
		new_page = self.workbook.copy_worksheet(self.workbook[self.tmpl_ws_name])
		
		new_page.title = page_name.replace('/', '-')
		self._fill_header(header, new_page)
		self._fill_data(data, new_page)
	
	def close(self):
		del self.workbook[self.tmpl_ws_name]
		self.workbook.save(self.path)	


if __name__ == '__main__':

	class Header:

		def __init__(self):
			self.street = "test street"
			self.building = "404"


	class DataInstance:

		def __init__(self):
			self.number = "14"
			self.area = "88"
			self.fio = "Xedxtxt"
			self.c_num = "88009525252" 
			self.vouts = "34"
			self.date = "11-09-2001"

	res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test.xlsx")
	template_path =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.xlsx")

	r = Report(res_path, template_path)
	r.add_worksheet(Header(), [DataInstance()], "test")
	r.close()

	








		
	

	
