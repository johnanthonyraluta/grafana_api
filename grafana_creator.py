from typing import Optional
from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse
from modules.grafana_api import grafana_json,template
from modules.parse_input import parse_host_int
import shutil
import uuid
file_path_linux = "/mnt/c/Users/jraluta/nso_parser/grafana_api/uploaded_files/tmp_"
file_path_windows = "C:\\Users\\raluta\\nso_parser\\grafana_api\\uploaded_files\\tmp_"
files = ['IMUS3559CICN001_IMUS3559CICN002_infra.csv']
unique_id="IMUS3559CICN001_IMUS3559CICN002_infra"

def create_upload_files():
    for myfiles in files:
        #with open("/vagrant/grafana_api/uploaded_files/"+myfiles.filename, "wb") as buffer:
        with open(file_path_ + myfiles.filename,"wb") as buffer:
            shutil.copyfileobj(myfiles.file, buffer)
    return {"filenames": [file.filename for file in files]}

def create_template(unique_id):
    my_uuid = str(uuid.uuid4().hex)
    status1 = parse_host_int(unique_id)
    status2 = grafana_json(unique_id,my_uuid)
    return status1,status2

def download_template(unique_id):
    my_json = template(unique_id)
    return my_json

def main():
    create_template(unique_id)
    download_template(unique_id)
if __name__ == '__main__':
    main()