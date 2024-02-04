from typing import Union
from fastapi import FastAPI, APIRouter

from cas_parser import parse

BASE_SERVER_PATH = '/api/v1'
app = FastAPI()
router = APIRouter(prefix=BASE_SERVER_PATH)

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@router.post('/parse_cas_summary')
def parse_summary():
    ## TODO: Port to FastAPI
    # The below code is written for Flask. This has to be ported to FastAPI
    # file = request.files['file']
    # password = request.form['password']
    # print(password)
    # try:
    #     data = parse(file, password)
    # except:
    #     return jsonify({}), 429
    # return jsonify(data), 200
    return {}



app.include_router(router)
