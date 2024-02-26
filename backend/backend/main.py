from typing import Annotated

from fastapi import FastAPI, APIRouter, UploadFile, File, Form
import logging

from cas_parser import parse
from thefuzz import fuzz, process

from sqlite_engine import ENGINE
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import FundHouse, FundScheme, FundSchemeHolding, Company

from collections import defaultdict as dd

logging.basicConfig(level=logging.INFO, filename="app.log", format="%(asctime)s %(levelname)s %(message)s")
BASE_SERVER_PATH = '/api/v1'

app = FastAPI()
router = APIRouter(prefix=BASE_SERVER_PATH)

class FundSchemeCache:
    def __init__(self):
        self.schemes = []
        self.nameToIDMap = dd(int)

    def cache(self, data):
        for scheme in data:
            self.schemes.append(scheme.name)
            self.nameToIDMap[scheme.name] = scheme

    def get_id(self, name):
        return self.nameToIDMap[name]

fundSchemeCache = FundSchemeCache()

def init_services():
    stmt = select(FundScheme)
    result = []
    try: 
        with Session(ENGINE) as session:
            result = session.scalars(stmt).all()
            fundSchemeCache.cache(result)
            logging.info(result[: 5])
    except Exception as e:
        logging.info(f"Init services failed {e}")


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

class CasSummaryResult:
    def __init__(self):
        self.fund_schemes = []
        self.holding_details = dd(list)

    def set_schemes(self, schemes: list):
        self.fund_schemes = schemes

    def add_holding(self, id: int, holding_detail: list):
        self.holding_details[id] = holding_detail

def extract_cas(data: list[dict]):
    schemes = []
    for folio in data:
        # TODO: Load Axis Data
        fuzzy_result = process.extract(folio['SCHEME_NAME'], fundSchemeCache.schemes, scorer=fuzz.token_set_ratio)[0]
        schemes.append(fundSchemeCache.get_id(fuzzy_result[0]))
    

    result = CasSummaryResult()
    result.set_schemes(schemes)

    for scheme in schemes:
        holding = fund_holding(scheme.id)
        result.add_holding(scheme.id, holding)

    return result

@router.post('/parse_cas_summary')
def parse_summary(file: UploadFile = File(...), password: Annotated[str, Form()] = ''):
    logging.info(file.filename)
    logging.info(password)
    data = {}
    try:
        data = parse(file.file, password)
    except Exception as e:
        logging.info("An exception occurred", e)
    return extract_cas(data)


init_services()

app.include_router(router)
