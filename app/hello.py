#https://fastapi.tiangolo.com/tutorial/first-steps/

from fastapi import FastAPI

app = FastAPI()

# fastapi run app/hello.py --port 8080 
@app.get("/")
async def root():
    return {"message": "Hello World"}