from fastapi import FastAPI

from core.database import Base
from core.database import engine
from fastapi.middleware.cors import CORSMiddleware

from api.auth import router as auth_router
from api.recommendation import router as reco_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(reco_router)