from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
import bcrypt
from fastapi.staticfiles import StaticFiles
import os


# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password_hash = Column(String)

class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cover_image = Column(String)

class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist = Column(String)
    playlist_id = Column(Integer, ForeignKey("playlists.id"))
    file_path = Column(String)

class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    song_id = Column(Integer, ForeignKey("songs.id"))

Base.metadata.create_all(bind=engine)

# App setup
app = FastAPI()

app.mount("/audio", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "audio")), name="audio")
app.mount("/images", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "images")), name="images")


# CORS to allow frontend to fetch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    # Password validation
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters long")
    
    db = SessionLocal()
    try:
        if db.query(User).filter(User.username == username).first():
            raise HTTPException(status_code=400, detail="Username already exists")
        # Hash password using bcrypt
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(username=username, password_hash=hashed.decode('utf-8'))
        db.add(user)
        db.commit()
        return {"message": "User registered successfully"}
    finally:
        db.close()


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return {"user_id": user.id, "username": user.username}
    finally:
        db.close()

@app.get("/playlists")
def get_playlists():
    db = SessionLocal()
    try:
        playlists = db.query(Playlist).all()
        return [{"id": p.id, "name": p.name, "cover_image": p.cover_image} for p in playlists]
    finally:
        db.close()

@app.get("/playlist/{playlist_id}")
def get_songs(playlist_id: int):
    db = SessionLocal()
    try:
        songs = db.query(Song).filter(Song.playlist_id == playlist_id).all()
        return [{"id": s.id, "title": s.title, "artist": s.artist, "file_path": s.file_path} for s in songs]
    finally:
        db.close()

@app.get("/favorites/{user_id}")
def get_favorites(user_id: int):
    db = SessionLocal()
    try:
        favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()
        result = []
        for fav in favorites:
            song = db.query(Song).filter(Song.id == fav.song_id).first()
            if song:  # Add safety check
                result.append({"id": song.id, "title": song.title, "artist": song.artist, "file_path": song.file_path})
        return result
    finally:
        db.close()

@app.post("/favorite")
def add_favorite(user_id: int = Form(...), song_id: int = Form(...)):
    db = SessionLocal()
    try:
        if db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.song_id == song_id).first():
            raise HTTPException(status_code=400, detail="Already in favorites")
        fav = Favorite(user_id=user_id, song_id=song_id)
        db.add(fav)
        db.commit()
        return {"message": "Song added to favorites"}
    finally:
        db.close()

@app.delete("/favorite")
def remove_favorite(user_id: int = Form(...), song_id: int = Form(...)):
    db = SessionLocal()
    try:
        fav = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.song_id == song_id).first()
        if not fav:
            raise HTTPException(status_code=404, detail="Favorite not found")
        db.delete(fav)
        db.commit()
        return {"message": "Removed from favorites"}
    finally:
        db.close()
