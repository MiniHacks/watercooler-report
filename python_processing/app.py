from fastapi import FastAPI, File, UploadFile
import uuid
import os

app = FastAPI()

@app.on_event("startup")
def start_up():
  print("Starting server.")
  
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
  if not os.path.isdir("./files"):
    os.mkdir("./files")

  uri = uuid.uuid4()
  path = str(uri) + "." + file.filename.split(".")[-1]
  with open("./files/" + path, "wb+") as output:
    output.write(file.file.read())
    output.close()
  return {"uri": uri}

@app.get("/")
async def root():
  return "Hello world!"

@app.get("/process_media/{uri}")
def process_video(uri: str):
  """
  processes a given video, returns schema TBD

  uri -- gcs uri of media resource to process
  """

@app.get("/test")
def test_schema():
  return {"field": "value"}