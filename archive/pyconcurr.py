	
from pyrosreestrapi import CNRequest		
from concurrent.futures import ThreadPoolExecutor, Future
import sys
import time

def task_queue(task, iterator, concurrency=10):
  def submit():
    try:
      obj = next(iterator)
    except StopIteration:
      return
    stats['delayed'] += 1
    future = executor.submit(task, obj)
    future.add_done_callback(upload_done)

  def upload_done(future):
    submit()
    stats['delayed'] -= 1
    stats['done'] += 1

  executor = ThreadPoolExecutor(concurrency)
  stats = {'done': 0, 'delayed': 0}

  for _ in range(concurrency):
    submit()

  return stats		

  
if __name__ == '__main__':
  
  test_street, test_house, test_apartment = 'Чаадаева', '36', ''
  test_request = CNRequest(test_street, test_house, test_apartment)
  file_log = 'C:/Users/adm/Desktop/rosreestr/log.txt'
  file_res = 'C:/Users/adm/Desktop/rosreestr/cnres.csv'
   
  def task(CNRequest, file_log='', file_res=''):
    try:
      test_response = test_request.get_cnresponse() 
      test_response.write_log('C:/Users/adm/Desktop/rosreestr/log.txt')
      test_response.write_res('C:/Users/adm/Desktop/rosreestr/cnres.csv')
     
    except Exception as msg:
      print(msg)
     
  iterator = ((test_request, file_log, file_res) for i in range(1))	
    
  stats = task_queue(task, iterator, concurrency=100)
  
  while True:
    print('\rdone {done}, in work: {delayed}  '.format(**stats), sys.stdout.flush())
    if stats['delayed'] == 0:
      break
    time.sleep(0.2)  
  
 