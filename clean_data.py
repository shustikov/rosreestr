import paths
import os
from glob import glob

def clean_data():
  a = os.path.join(paths.tmp_folder, '*.xml')
  [os.remove(i) for i in glob(a)]
  
  a = os.path.join(paths.zips_folder, '*.zip')
  [os.remove(i) for i in glob(a)]