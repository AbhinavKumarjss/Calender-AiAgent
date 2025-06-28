from fastapi import FastAPI
import uvicorn
import os

from routes import chat
app = FastAPI()


app.include_router(chat.router , prefix='/api')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)