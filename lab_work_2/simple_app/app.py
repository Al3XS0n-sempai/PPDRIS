import random

from datetime import datetime
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root() -> dict:
    return {
        "endpoints": [
            {
                "path": "/",
                "method": "GET",
                "desc": "returns all available endpoints",
            },
            {
                "path": "/rand",
                "method": "GET",
                "desc": "return random integer number from 0 to 1000",
            },
            {
                "path": "/time",
                "method": "GET",
                "desc": "returns current time",
            },
        ]
    }


@app.get("/rand")
async def random_number() -> dict:
    return {"numer": random.randint(0, 1000)}

@app.get("/time")
async def cur_time() -> dict:
    return {"current_time": datetime.now().strftime("%H:%M:%S")}
