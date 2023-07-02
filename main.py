from _socket import gethostname

from fastapi import FastAPI
from psycopg2 import connect

conn = connect(
    host='pgpool',
    dbname='test_db',
    user='postgres',
    password='s3cret',
    port=5432
)

cur = conn.cursor()

app = FastAPI()
count = {gethostname(): 0}


@app.post("/add")
async def root(name: str):
    table = """create table if not exists sample(
        id serial primary key,
        name varchar(255)
    );"""
    cur.execute(table)
    conn.commit()
    query = """insert into sample(name) values (%s)"""
    cur.execute(query, (name,))
    conn.commit()
    count[gethostname()] += 1
    return count


@app.get("/")
async def root():
    query = """select * from sample limit 1"""
    cur.execute(query)
    datas = cur.fetchall()
    result = {data[0]: data[1] for data in datas}
    return result
