# -*- coding: utf-8 -*- 

"""
Модуль создаёт xmlx отчёты в папках улиц
"""

from paths import *
import xlsxwriter

class Note():
	"""
	Строка записи в файле
	"""
	def __init__(self, owner, responce):
		#self.worksheet = 
		self.apartment =
		self.area =
		self.fio =
		self.regnumber =
		self.regdate =
		self.vouts =
	
	def make_note(self, row, col):
		# write_row(row, col, data[, cell_format])
		worksheet.write(row, col,     self.apartment)
		worksheet.write(row, col + 1, self.area)
		worksheet.write(row, col + 2, self.fio)
		worksheet.write(row, col + 3, '{}, {}'.format(self.regnumber, self.regdate))
		worksheet.write(row, col + 4, self.vouts)
		worksheet.write(row, col + 5, '')
		
		...

class WorkSheet:
	"""
	Лист в файле
	"""
	def __init__(self, list_notes):
		self.name = '' #
		self.list_notes = '' #
		self.street = 
		self.building = 
		self.workbook = 
		...
		
	def make_worksheet(self):
		
		#top
		worksheet = workbook.add_worksheet(self.name)
		worksheet.merge_range(0, 0, 0, 5, 'Приложение № 1')
		worksheet.merge_range(1, 0, 1, 5, 'к Протоколу №____ внеочередного общего собрания собственников помещений в многоквартирном доме №{} по ул. {}').format(self.building, self.street) #ул.
		worksheet.merge_range(2, 0, 2, 5, "Нижнего Новгорода от «____» _______________ 201__ г.")
		worksheet.merge_range(4, 0, 4, 5, "Реестр собственников помещений")
		
		#top_table
		row, col = 5, 0
	
		worksheet.merge_range(row, col,     row + 1, col,     '№ пом.')
		worksheet.merge_range(row, col + 1, row + 1, col + 1, 'Общая площадь помещения')
		worksheet.write(      row, col + 2,                   'Собственник')
		worksheet.write(                    row + 1, col + 2, 'ФИО / Полное наименование и ОГРН')								
		worksheet.merge_range(row, col + 3, row + 1, col + 3, 'Документ, подтверждающий право собственности: наименование, номер, дата')
		worksheet.merge_range(row, col + 4, row + 1, col + 3, 'Количество голосов, которыми владеет собственник')
		worksheet.write(      row, col + 5,                   'ФИО представителя, реквизиты доверенности:')
		worksheet.write(                    row + 1, col + 5, 'дата, №')
		
		#notes
		row = row + 2

		for note in self.list_notes:
			note.make_note(row, col)
			row += 1
		

class XlsxFile:
	"""
	Файл отчёта для одной улицы
	"""
	def __init__(self, street_responces):
		self.street = 
		self.filename = "{}.xlsx".format(self.street)
		self.folder_path = self.street
		self.list_worksheets = 
		...
		

	def make_report(self, res_folder):
		path = '{}/{}/{}'.format(res_folder, self.folder_path, self.filename)
		workbook = xlsxwriter.Workbook(self.path)
		
		for worksheet in list_worksheets: 
			worksheet.write_worksheet()
			
		workbook.close()
		
if __name__ == '__main__':