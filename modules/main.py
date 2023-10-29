from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse
import os
import shutil
import time
app = FastAPI()


FastApiPath = os.path.dirname(os.getcwd())
filesDirectory = FastApiPath+"/MultipartFiles"
uniqueTimeStamp = int(time.time() * 1000)

@app.get('/about')
def alpha():

    return {'data':{'name':'krishna','kaam':'jalebi bai'}}

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    custom_name = str(uniqueTimeStamp)+'_'+str(file.filename)
    if os.path.exists(filesDirectory):
        file_path = os.path.join(filesDirectory, custom_name)
        with open(file_path, "wb") as destination:
            shutil.copyfileobj(file.file, destination)

    return {"Uploaded file": file}


@app.get("/")
async def main():
    content = """
        <body>
        <form action="/files/" enctype="multipart/form-data" method="POST">
        <input name="file" type="file">
        <input type="submit">
        </form>
        <form action="/uploadfile/" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)