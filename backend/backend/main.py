from fastapi import FastAPI, APIRouter, UploadFile, File
import logging

from cas_parser import parse

from sqlite_engine import ENGINE
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import FundHouse, FundScheme, FundSchemeHolding, Company

logging.basicConfig(level=logging.INFO, filename="app.log", format="%(asctime)s %(levelname)s %(message)s")
BASE_SERVER_PATH = '/api/v1'

app = FastAPI()
router = APIRouter(prefix=BASE_SERVER_PATH)

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/fund_house/{id}")
def fund_house(id: int):
    logging.info(f"Get fund house {id}")
    stmt = select(FundHouse).where(FundHouse.id == id)
    result = []
    try:
        with Session(ENGINE) as session:
            result = session.scalars(stmt).all()
    except Exception as e:
        logging.info("An exception occurred while getting fund house", e)
    return result

@router.get("/fund_scheme/{fund_id}")
def fund_scheme(fund_id: int):
    logging.info(f"Get fund scheme {fund_id}")
    stmt = select(FundScheme).where(FundScheme.id == fund_id)
    result = []
    try:
        with Session(ENGINE) as session:
            result = session.scalars(stmt).all()
    except Exception as e:
        logging.info("An exception occurred while getting fund scheme", e)
    return result

@router.get("/fund_holding/{fund_id}")
def fund_holding(fund_id: int):
    logging.info(f"Get fund holding {fund_id}")
    stmt = select(FundSchemeHolding).where(FundSchemeHolding.fund_id == fund_id)
    result = []
    try:
        with Session(ENGINE) as session:
            result = session.scalars(stmt).all()
    except Exception as e:
        logging.info("An exception occurred while getting fund holding", e)
    return result

@router.get("/company/{company_id}")
def company(company_id: int):
    logging.info(f"Get company {company_id}")
    stmt = select(Company).where(Company.id == company_id)
    result = []
    try:
        with Session(ENGINE) as session:
            result = session.scalars(stmt).all()
    except Exception as e:
        logging.info("An exception occurred while getting company", e)
    return result


@router.post('/parse_cas_summary')
def parse_summary(file: UploadFile = File(...), password: str = ''):
    logging.info(file.filename)
    logging.info(password)
    data = {}
    try:
        data = parse(file.file, '')
    except Exception as e:
        logging.info("An exception occurred", e)
    return data


app.include_router(router)
