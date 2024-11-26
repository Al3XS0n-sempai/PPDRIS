from fastapi import FastAPI
from starlette.responses import JSONResponse

from models import Session
import storage
import datetime


app = FastAPI()


@app.get("/session")
async def create_session():
    session: Session = storage.create_session()
    return JSONResponse({'session_id': session.id})


@app.get("/tool/{session_id}")
async def create_item(session_id: int):
    session: Session = storage.get_session(session_id)

    if not session:
        return JSONResponse({"error": "session not found"})

    if datetime.datetime.now() > session.expiration_timestamp:
        return JSONResponse({"error": "session expired"})

    return JSONResponse(
        {
            "message": "Hello user!",
            "Your super number today is: ": datetime.datetime.now().year * session.id
        }
    )


@app.get("/")
async def homepage():
    return JSONResponse({'message': 'Please request on /session and then on /tool/{session_id}'})
