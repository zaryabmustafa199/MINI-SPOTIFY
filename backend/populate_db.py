from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Base, Playlist, Song
import os

# Use same database path as app.py
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Example playlists
# Example playlists
playlists = [
    Playlist(id=1, name="POP MUSIC", cover_image="http://127.0.0.1:8001/images/pop_song.jpg"),
    Playlist(id=2, name="PAKISTANI MUSIC", cover_image="http://127.0.0.1:8001/images/pakistani.jpg"),
    Playlist(id=3, name="BOLLYWOOD MUSIC", cover_image="http://127.0.0.1:8001/images/bollywood.jpg")
]

for p in playlists:
    existing = db.query(Playlist).filter(Playlist.id == p.id).first()
    if not existing:
        db.add(p)
db.commit()

# Example songs (replace with your own audio filenames)
# Note: Ensure these files exist in backend/audio/
songs = [
    Song(title="ALA BARFI", artist="Pritam X Mohit", playlist_id=3, file_path="http://127.0.0.1:8001/audio/Ala%20Barfi%20-%20BarfiPritamMohit%20ChauhanRanbir.mp3"),
    Song(title="CHAN KITHAN", artist="Ali Sethi", playlist_id=2, file_path="http://127.0.0.1:8001/audio/Chan%20Kithan%20%20Ali%20Sethi%20(Official%20Music%20Video).mp3"),
    Song(title="TU JHOOM", artist="Abida X Naseebo", playlist_id=2, file_path="http://127.0.0.1:8001/audio/Coke%20Studio%20%20Season%2014%20%20Tu%20Jhoom%20%20Naseebo%20Lal%20x%20Abida%20Parveen.mp3"),
    Song(title="PIYA GHAR AAYA", artist="Fareed Ayaz", playlist_id=2, file_path="http://127.0.0.1:8001/audio/Coke%20Studio%20Season%2011%20Piya%20Ghar%20Aaya%20Fareed%20Ayaz%20Abu%20Muhammad%20Qawwal%20and%20Brothers.mp3"),
    Song(title="FOR A REASON", artist="Karan Aujla", playlist_id=1, file_path="http://127.0.0.1:8001/audio/For%20A%20Reason%20(Official%20Video)%20Karan%20Aujla%20_%20Tania%20_%20Ikky%20_%20Latest%20Punjabi%20Songs%202025%20[-YlmnPh-6rE].mp3"),
    Song(title="KISKA RASTA DEKHE", artist="Kishore Kumar", playlist_id=3, file_path="http://127.0.0.1:8001/audio/Full%20Video_%20Kiska%20Rasta%20Dekhe%20%20Joshila%20(1973)%20%20Dev%20Anand,%20Hema%20Malini%20%20Kishore%20Kumar%20%20R%20D%20Burman.mp3"),
    Song(title="MERE SAPNO KI RANI", artist="Kishore Kumar", playlist_id=3, file_path="http://127.0.0.1:8001/audio/Kishore%20Kumar%20_%20Mere%20Sapno%20Ki%20Rani%20Kab%20Aayegi%20Tu%20%20Rajesh%20Khanna%20%20Sharmila%20Tagore.mp3"),
    Song(title="MERE MEHBOOB QAYAMAT HOGI", artist="Kishore Kumar", playlist_id=3, file_path="http://127.0.0.1:8001/audio/Mere%20Mehboob%20Qayamat%20Hogi%20%20(Original)%20-%20Mr.%20X%20In%20Bombay%20-%20Kishore%20Kumar's%20Greatest%20Hits%20-%20Old%20Songs.mp3"),
    Song(title="PAAR CHANAA DE", artist="Ali Wasi Kazmi", playlist_id=2, file_path="http://127.0.0.1:8001/audio/Paar%20chanaa%20de%20-%20music%20video%20%20ALI%20WASI%20KAZMI%20%20AMNA%20YOUZASAIF%20%20FAN%20VIDEO.mp3"),
    Song(title="RAANJHANAA", artist="A R Rahman", playlist_id=3, file_path="http://127.0.0.1:8001/audio/Raanjhanaa%20-%20Lyrical%20Video%20%20Dhanush,%20Sonam%20Kapoor%20%20A.%20R.%20Rahman%20%20Jaswinder%20Singh%20&%20Shiraz%20Uppal.mp3"),
    Song(title="RAVI", artist="Sajjad Ali", playlist_id=2, file_path="http://127.0.0.1:8001/audio/Sajjad%20Ali%20-%20RAVI%20(Official%20Video).mp3")
]

for s in songs:
    db.add(s)
db.commit()

print(f"Database populated successfully! Added {len(playlists)} playlists and {len(songs)} songs.")
