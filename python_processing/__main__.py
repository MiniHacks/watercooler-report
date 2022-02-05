import uvicorn
import python_processing.app as app
import os

uvicorn.run(app.app, host="127.0.0.1", port=int(os.environ.get("PORT", 8000)))

@app.on_event("start_up")
def start_up():
  print("Starting server.")

@app.get("/")
async def root():
  return "Hello world!"