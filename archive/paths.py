# -*- coding: utf-8 -*- 

"""
Модуль содержащий пути файлов  

"""

#dload_folder = "C:\Users\adm\Desktop\Новая папка (2)\Мечникова,53"
res_folder = 'C:/Users/adm/Desktop/rosreestr/res'
zips_folder = 'C:/Users/adm/Desktop/Новая папка (2)/temp'
tmp_folder = 'C:/Users/adm/Desktop/rosreestr/res/tmp'
pdfs_folder	= 'C:/Users/adm/Desktop/rosreestr/res/pdfs'
xmls_folder = 'C:/Users/adm/Desktop/rosreestr/res/xmls'
log_folder = 'C:/Users/adm/Desktop/rosreestr/logs'

xml_up_log_fname = 'xml_up_log'



xml_up_log_file = log_folder + '/' + xml_up_log_fname + '.txt'
test_file = 'C:/Users/adm/Desktop/rosreestr/test.xml' 
test_zip_file = 'C:/Users/adm/Desktop/rosreestr/test.zip' 


if __name__ == '__main__':
	[print(x + " = " + y ) for x,y in __dict__.items()]
	
	