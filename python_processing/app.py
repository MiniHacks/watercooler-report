from fastapi import FastAPI
from typing import List
from random import randint

app = FastAPI()

@app.on_event("startup")
def start_up():
  print("Starting server.")

@app.get("/")
async def root():
  return "Hello world!"

@app.get("/process_segments/{uri}")
def process_video(segments: List[str]):
  """
  processes a given set of segments, returns certainty [0-1] of harassment per segment.

  segments -- list of strings

  returns 
  {
    result: [(segment, certainty), ...]
  }
  """
  return {"result": list(map(
    lambda segment: (segment, 0 if randint(0,10) <= 3 else randint(40,100)/100),
    segments
  ))}

@app.get("/test")
def test_schema():
  return {"field": "value"}