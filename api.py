import psycopg2
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

conn = psycopg2.connect(
    host="localhost",
    database="reddit",
    user="postgres",
    password="pranesh@8917",
    port=5432
)
