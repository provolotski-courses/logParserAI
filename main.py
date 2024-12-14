from fastapi import FastAPI, File, UploadFile, Form, Depends



import logging
from utils.config import LOG_DIR, LOG_FILE, LOG_LEVEL
from DAO.connection import initDatabase
import utils.logparser as pars

logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s %(name)-30s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler(LOG_DIR + LOG_FILE), logging.StreamHandler()])
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(), multistring: bool = Form(default=False)):
    logger.debug(f'upload_file {file.filename}, multisting is {multistring}')
    content = await file.read()
    if multistring:
        pars.parsMultistring(content,file.filename)
    return {"filename": file.filename}

@app.post('/initdatabase/')
async def init_database():
    logger.info('init database')
    initDatabase()

