# -*- coding: utf-8 -*-


from pyrosreestrapi import CNRequest
from pyconcurr import task_queue
import sys
import time

folder = "C:/Users/adm/Desktop/Заливка ГИС ЖКХ/"
file1 = "csv ЖП.csv" 
file2 = "csv ЖП2.csv"
resfile = "csv res1.csv"

with open(folder + file1) as f1:
  r1 = [line.strip().split(';') for line in f1.readlines()]
  f1.close()
	
with open(folder + file2) as f2:
  r2 = [line.strip().split(';') for line in f2.readlines()]
  f2.close()

iter = []
for i in r2:																										#передел
  ii = i[0].split(',')  
  obj = [(ii[0], ii[1], i[1], i2) for i2 in r1 if i[:2] == i2[:2]] #BOOM
  if len(obj) >= 1: street, house, apartment, address = obj[0]
  iter += [CNRequest(street, house, apartment, address)]
 
iterator = (i for i in iter)


def write_res(resp):
  d = resp.CNRequest.address
  
  with open('C:/Users/adm/Desktop/rosreestr/cnres.csv', 'a') as resf:
   for r in resp.response:  
      cn = r['objectCn']
      an = r['addressNotes']
      print('{}; {}; {}; {}; {}; {}; {};'.format(an, d[0], d[1], d[2], d[3], d[4], cn), file = resf)  
  
	
def write_log(resp, msg):
	d = resp.CNRequest
    print('{}; {}; {}; {}; {}; {}; {};'.format(d.address[0], d.address[1], d.status, d.reason, len(self.response), self.duration, msg)

	
def task(CNRequest, file_log='', file_res=''):
   try:
     msg = 'ok'
     test_response = CNRequest.get_cnresponse()
	 write_log(resp, msg)
     #test_response.write_log('C:/Users/adm/Desktop/rosreestr/log.txt')
     write_res(test_response)
     #test_response.write_res('C:/Users/adm/Desktop/rosreestr/cnres.csv')
    
   except Exception as msg:
     print(msg)  



	 
stats = task_queue(task, iterator, concurrency=100)
  
while True:
    print('\rdone {done}, in work: {delayed}  '.format(**stats), sys.stdout.flush())
    if stats['delayed'] == 0:
      break
    time.sleep(0.2)  

"""
file_log = 'C:/Users/adm/Desktop/rosreestr/log.txt'
file_res = 'C:/Users/adm/Desktop/rosreestr/cnres.csv'
iterator = ((test_request, file_log, file_res) for i in range(1))

  

with open(folder + resfile, 'a') as resf:  
  [[print(';'.join(i2[:3] + i1[2:]), file = resf) for i1 in r1 if i1[:2] == i2[:2]] for i2 in r2]
  resf.close()
"""
	
 

