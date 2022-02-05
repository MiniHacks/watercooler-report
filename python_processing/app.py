from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def start_up():
  print("Starting server.")

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