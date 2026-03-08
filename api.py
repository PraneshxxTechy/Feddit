import psycopg2
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import jwt
from jose import JWTError
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

app = FastAPI()

def get_conn():
    conn = psycopg2.connect(
        host="localhost",
        database="reddit",
        user="postgres",
        password="pranesh@8917",
        port=5432
    )
    return conn

class UserRegister(BaseModel):
    username : str
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

@app.post("/register")
def register_user(user: UserRegister):
    conn = get_conn()
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
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_conn()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        SELECT id, username, password
        FROM users
        WHERE username = %s
        """, (form_data.username,))  

        db_user = cursor.fetchone()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        user_id, username, db_password = db_user

        if form_data.password != db_password:
            raise HTTPException(status_code=401, detail="Invalid password")

        access_token = create_access_token(
            data={"user_id": user_id, "username": username}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    finally:
        cursor.close()
        conn.close()