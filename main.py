import uvicorn
import uuid
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()


class Query(BaseModel):
    year: str
    ward: str
    pid = str(uuid.uuid4())


@app.get("/")
def read_root():
    return {"msg": "Tokyo Housing Prices"}


@app.post("/trades/")
def create_trades(query: Query, background_tasks: BackgroundTasks):
    background_tasks.add_task(collect_trades, query.dict())
    return {'message': f'The create trades process has been started. Process ID: {query.dict()["pid"]}'}


def collect_trades(query: dict):
    # requests.get でデータ取得
    params = 'DLF=true&TTC-From=' + query['year'] + '1&TTC-To=' + query['year'] + '1&TDK=13&SKC=' + query['ward']
    url = 'https://www.land.mlit.go.jp/webland/servlet/DownloadServlet?' + params
    print(url)


if __name__ == '__main__':
    uvicorn.run(app)
