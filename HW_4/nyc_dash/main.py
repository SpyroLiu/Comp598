from src.data_process import *
from src.dropdown import *
script_dir = osp.dirname(__file__)
path = osp.join(script_dir, '..', 'data', 'zip_avg.json')
if not osp.exists(path):
    getZipJson();
createZipCodeDropdown()

