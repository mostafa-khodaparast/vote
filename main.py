from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/greet/")   #pass parameter here
async def read_root(name: str, age:Optional[int] = 50):  #query parameter here
    return {"Hello": f"hi {name} you are {age}"}

