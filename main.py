import csv
import uuid
from concurrent import futures

import uvicorn
from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from internal import execute, connection

app = FastAPI()


class Query(BaseModel):
    year: str
    ward: str
    pid = str(uuid.uuid4())


@app.get("/")
def read_root():
    return {"msg": "Tokyo Housing Prices"}


@app.get("/trades/")
def list_trades():
    data = connection('trades').select_all()
    return data


@app.post("/trades/")
def create_trades(query: Query, background_tasks: BackgroundTasks):
    background_tasks.add_task(collect_trades, query.dict())
    return {'message': f'The create trades process has been started. Process ID: {query.dict()["pid"]}'}


def collect_trades(query: dict):
    # CSV to DICT
    with open('./config/training_data.csv', newline='', encoding='utf_8') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    # Sanitization
    data = sanitization(data)
    # データベースにデータ投入
    conn = connection('trades')
    conn.upsert(data)


def sanitization(_data):
    result = []
    with futures.ProcessPoolExecutor(max_workers=8) as executor:
        for rec in _data:
            result.append(executor.submit(execute, rec).result())

    return result


if __name__ == '__main__':
    uvicorn.run(app)
