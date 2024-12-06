from zenitdb.app import app
from zenitdb import models, crud 
from zenitdb.database import engine, get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


@app.get("/")
def root():
    return "and this is not crud"


import userdef.user_login
import userdef.user_api
import userdef.export_api
import zenitdb.api


origins = [
    "*",
    "http://localhost:9000",
    "http://127.0.0.1:3000/",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=['Content-Disposition']
)
