import csv
import uuid
from concurrent import futures

import uvicorn
from fastapi import BackgroundTasks, FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from internal import execute, connection

app = FastAPI()


class Query(BaseModel):
    file_name: Optional[str] = '13_Tokyo_20201_20212.csv'
    pid = str(uuid.uuid4())


@app.get("/")
def read_root():
    cnt = connection('trades').count()
    return {"msg": "Tokyo Housing Prices", "stored_records": cnt}


@app.get("/status/{process_id}")
def list_job_status(process_id: str):
    data = connection('status').get(process_id)
    return data


@app.get("/trades/")
def list_trades():
    data = connection('trades').select_all()
    return data


@app.post("/trades/")
def create_trades(query: Query, background_tasks: BackgroundTasks, request: Request):
    background_tasks.add_task(collect_trades, query.dict())
    url = request.client.host + ':' + request.client.host + '/status/' + query.dict()["pid"]
    return {'message': 'The create trades process has been started.', 'status': url}


def collect_trades(query: dict):
    # Set Status
    connection('status').start(query['pid'])

    # CSV to DICT
    with open('./config/' + query['file_name'], newline='', encoding='cp932') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    # Sanitization
    data = sanitization(data)
    # データベースにデータ投入
    conn = connection('trades')
    conn.upsert(data)

    # Update Status
    connection('status').finish(query['pid'], 'Finished')


def sanitization(_data):
    result = []
    with futures.ProcessPoolExecutor(max_workers=8) as executor:
        for rec in _data:
            result.append(executor.submit(execute, rec).result())

    return result


if __name__ == '__main__':
    uvicorn.run(app)
