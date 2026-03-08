import psycopg2
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr

app = FastAPI()

conn = psycopg2.connect(
    host="localhost",
    database="reddit",
    user="postgres",
    password="pranesh@8917",
    port=5432
)

class UserRegister(BaseModel):
    username : str
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

@app.post("/register")
def register_user(user: UserRegister):
    cursor = conn.cursor()

    try:

        # Check if email exists
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (user.email,)
        )

        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already exists")

        cursor.execute("""
        INSERT INTO users (username, email, password)
        VALUES (%s, %s, %s)
        RETURNING id
        """, (user.username, user.email, user.password))

        user_id = cursor.fetchone()[0]

        conn.commit()

        return {
            "message": "User registered successfully",
            "user_id": user_id
        }

    finally:
        cursor.close()
        conn.close()


@app.post("/login")
def login_user(user: UserLogin):
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT id, username, password
        FROM users
        WHERE email = %s
        """, (user.email,))

        db_user = cursor.fetchone()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        user_id, username, db_password = db_user

        if user.password != db_password:
            raise HTTPException(status_code=401, detail="Invalid password")
        return {
            "message": "Login successful",
            "user_id": user_id,
            "username": username
        }
    finally:
        cursor.close()
        conn.close()
