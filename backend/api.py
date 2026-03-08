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
from enve import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


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

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_conn():
    conn = psycopg2.connect(
        host=settings.database_host,
        database=settings.database_name,
        user=settings.database_user,
        password=settings.database_password,
        port=settings.database_port
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
        WHERE username = %s OR email = %s
        """, (form_data.username, form_data.username))  

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

from fastapi import Query

@app.get("/posts")
def get_posts(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT 
            p.id,
            p.title,
            p.content,
            p.url,
            COALESCE((SELECT SUM(vote_type) FROM votes WHERE post_id = p.id), 0) as vote_score,
            COALESCE((SELECT COUNT(*) FROM comments WHERE post_id = p.id), 0) as comment_count,
            u.username
        FROM posts p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
        LIMIT %s OFFSET %s
        """, (limit, offset))

        posts = cursor.fetchall()

        return [
            {
                "id": post[0],
                "title": post[1],
                "content": post[2],
                "url": post[3],
                "votes": post[4],
                "comments": post[5],
                "username": post[6]
            }
            for post in posts
        ]

    finally:
        cursor.close()
        conn.close()

class PostCreate(BaseModel):
    title: str
    content: str
    url: str

class VoteRequest(BaseModel):
    vote_type: int

class CommentCreate(BaseModel):
    comment: str

@app.post("/posts")
def create_post(post: PostCreate, user_id: int = Depends(get_current_user) ):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO posts (title, content, url, user_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """, (post.title, post.content, post.url, user_id))  # Assuming user_id is 1 for now

        post_id = cursor.fetchone()[0]

        conn.commit()

        return {
            "message": "Post created successfully",
            "post_id": post_id
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, user_id: int = Depends(get_current_user)):
    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM posts WHERE id=%s AND user_id=%s RETURNING id",
            (post_id, user_id)
        )

        deleted = cursor.fetchone()

        if not deleted:
            raise HTTPException(403, "Not authorized")

        conn.commit()

        return {"message": "Post deleted"}
    finally:
        cursor.close()
        conn.close()

@app.get("/posts/{post_id}/comments")
def get_comments(post_id: int):
    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT c.id, c.comment, c.created_at, u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.post_id = %s
        ORDER BY c.created_at DESC
        """, (post_id,))

        comments = cursor.fetchall()

        return [
            {
                "id": comment[0],
                "comment": comment[1],
                "created_at": comment[2],
                "username": comment[3]
            }
            for comment in comments
        ]
    finally:
        cursor.close()
        conn.close()

@app.post("/posts/{post_id}/comments")
def add_comment(post_id: int, comment_data: CommentCreate, user_id: int = Depends(get_current_user)):
    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO comments (user_id, post_id, comment)
        VALUES (%s, %s, %s)
        RETURNING id
        """, (user_id, post_id, comment_data.comment))

        comment_id = cursor.fetchone()[0]

        conn.commit()

        return {
            "message": "Comment added successfully",
            "comment_id": comment_id
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/posts/{post_id}/vote")
def vote_post(post_id: int, vote_data: VoteRequest, user_id: int = Depends(get_current_user)):
    if vote_data.vote_type not in [1, -1]:
        raise HTTPException(status_code=400, detail="Invalid vote type")

    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO votes (user_id, post_id, vote_type)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, post_id) DO UPDATE
        SET vote_type = EXCLUDED.vote_type
        """, (user_id, post_id, vote_data.vote_type))

        conn.commit()

        return {
            "message": "Vote recorded successfully"
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/posts/{post_id}/votes")
def get_votes(post_id: int):
    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT vote_type, COUNT(*)
        FROM votes
        WHERE post_id = %s
        GROUP BY vote_type
        """, (post_id,))

        votes = cursor.fetchall()

        upvotes = next((count for vt, count in votes if vt == 1), 0)
        downvotes = next((count for vt, count in votes if vt == -1), 0)

        return {
            "score": upvotes - downvotes,
            "upvotes": upvotes,
            "downvotes": downvotes
        }
    finally:
        cursor.close()
        conn.close()