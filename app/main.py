from fastapi import FastAPI
import uvicorn
from .database import engine
from . import models
from .routers import posts
from .routers import users
from .routers import auth
from .routers import vote
from fastapi.middleware.cors import CORSMiddleware

#Create all models if not exists at the time of starting the application
#Replaced by alembic
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(CORSMiddleware,
    allow_origins=['https://www.google.com'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=['*']
)

#method:path
@app.get("/")
async def root():
    return "Hello World"

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)