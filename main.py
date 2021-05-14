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
from starlette.responses import FileResponse

app = FastAPI()

class User(BaseModel):
    user_name: dict
@app.get("/")
async def main():
    content = """
<header>
<h1>Welcome to Grafana JSON Template Generator!</h1>
<p>Created by: Cisco PH Automation Team</p>
<p>~~~~~~~~~</p>
</header>
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

# @app.post("/files/")
# async def create_files(files: List[bytes] = File(...)):
#     # for myfiles in files:
#     #     print(myfiles)
#     #     with open("/vagrant/grafana_api/uploaded_files/"+myfiles, "wb") as buffer:
#     #         shutil.copyfileobj(myfiles.file, buffer)
#     #return ({"file_sizes": [len(file) for file in files]},{"filename":myfiles.filename})
#     return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for myfiles in files:
        #with open("/vagrant/grafana_api/uploaded_files/"+myfiles.filename, "wb") as buffer:
        with open("/mnt/c/Users/jraluta/nso_parser/grafana_api/uploaded_files/tmp_" + myfiles.filename,"wb") as buffer:
            shutil.copyfileobj(myfiles.file, buffer)
    return {"filenames": [file.filename for file in files]}

@app.get("/template/{unique_id}")
async def create_template(unique_id:str):
    my_uuid = str(uuid.uuid4().hex)
    status1 = parse_host_int(unique_id)
    status2 = grafana_json(unique_id,my_uuid)
    return status1,status2

@app.get("/json_template/{unique_id}")
async def download_template(unique_id:str):
    my_json = template(unique_id)
    return my_json
