from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import insert, text
from sqlalchemy.orm import Session
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from zenitdb.database import engine, get_db
from zenitdb import models, schemas
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
import random
import hashlib
import math

from conf.conf import Test_Mode


app = FastAPI(    
    title="ALMAS UI",
    description="""
Almas is a DDS like APP
""",
    summary="API of Almas UI",
    version="0.0.1"
)


from alembic import command
from alembic.config import Config

alembic_cfg = Config("alembic.ini")

def autogenerate_migration(SIGNATURE):
    with engine.begin() as connection:
        alembic_cfg.attributes['connection'] = connection

        from pathlib import Path
        versions = Path.cwd() / 'alembic' / 'versions'
        files = list(versions.glob(f"*_{SIGNATURE}.py"))
        try:
            if len(files) <= 0:
                command.revision(alembic_cfg, autogenerate=True, message=SIGNATURE)
        finally:
            command.upgrade(alembic_cfg, "head")
        
        print(f"#####     DB Updated : {models.DATABSE_SIGNATURE} #################") 


@app.on_event("startup")
async def startup_event():
    autogenerate_migration(models.DATABSE_SIGNATURE)

