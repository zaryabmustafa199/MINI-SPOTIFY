# Project Documentation: Mini Spotify

## 1. Project Overview
This project is a web-based music streaming application ("Mini Spotify") that allows users to browse playlists, play songs, register/login, and manage a list of favorite songs. It consists of a **FastAPI (Python)** backend that serves a REST API and static files (audio/images), and a **Vanilla HTML/JS** frontend that interacts with this backend.

---

## 2. Project Structure & File Functionality

### **Backend (`/backend`)**
The logic hub of the application. It handles data persistence, user authentication, and serving media files.

#### **`backend/app.py`**
The main entry point for the backend server.
*   **Purpose**: Defines the API endpoints, database models, and server configuration.
*   **Key Components**:
    *   **Imports**: Uses `FastAPI` for the web framework, `SQLAlchemy` for the database, and `bcrypt` for password hashing.
    *   **Database Setup**: Connects to `database.db`. Creates a session factory `SessionLocal`.
    *   **Models (SQLAlchemy Classes)**:
        *   `User`: `id`, `username`, `password_hash`.
        *   `Playlist`: `id`, `name`, `cover_image`.
        *   `Song`: `id`, `title`, `artist`, `playlist_id` (ForeignKey), `file_path`.
        *   `Favorite`: Links `user_id` and `song_id` to store user favorites.
    *   **Static Mounts**: Serves `/audio` and `/images` directories so the frontend can load media directly via URL.
    *   **CORS**: Configured to allow all origins (`*`) so the frontend file can request the backend API without browser restrictions.
    *   **API Routes**:
        *   `POST /register`: Accepts username/password, hashes password, creates user. Checks for duplicates.
        *   `POST /login`: Verifies credentials against the database. Returns user ID/name.
        *   `GET /playlists`: Returns a list of all playlists.
        *   `GET /playlist/{playlist_id}`: Returns all songs belonging to a specific playlist ID.
        *   `GET /favorites/{user_id}`: Returns the list of favorite songs for a specific user.
        *   `POST /favorite`: Adds a song to a user's favorites list. w/ duplicate check.
        *   `DELETE /favorite`: Removes a song from a user's favorites.

#### **`backend/populate_db.py`**
A utility script to initialize the database with starter data.
*   **Purpose**: Populates empty tables with default Playlists and Songs.
*   **Functionality**:
    *   Connects to `database.db`.
    *   Defines a list of hardcoded `Playlist` objects (e.g., Pop, Pakistani, Bollywood).
    *   Defines a list of hardcoded `Song` objects mapped to those playlists.
    *   Checks if items exist; if not, it adds them to the database.

#### **`backend/requirements.txt`**
Dependency list for the Python environment.
*   **Contents**: `fastapi`, `uvicorn` (server), `sqlalchemy` (ORM), `bcrypt` (security), `python-multipart` (form handling), etc.

#### **`backend/database.db`**
The SQLite database file created automatically by SQLAlchemy. Stores all users, songs, playlists, and favorites.

#### **`backend/check_db.py` (located in root in your setup, but logic inspects `backend/database.db`)**
A diagnostic script.
*   **Purpose**: Prints the current contents of the database to the terminal.
*   **Functionality**: Connects to `database.db` and executes raw SQL queries (`SELECT * ...`) to list Playlists, Songs, and Users.

---

### **Frontend (`/frontend`)**
The user interface. It is a Single Page Application (SPA)-like structure using multi-page HTML files that share common styles and logic patterns.

#### **HTML Files**
*   **`index.html`**: The Homepage. Shows the "Playlists" section. Loads `js/home.js`.
*   **`playlist.html`**: The Player view. Shows songs for a specific playlist. Loads `js/playlist.js`.
*   **`library.html`**: The "My Library" page. Shows the user's favorite songs. Loads `js/library.js`.
*   **`login.html`** / **`register.html`**: Authentication forms. Load `js/login.js` / `js/register.js`.

#### **JavaScript Files (`frontend/js/`)**
*   **`home.js`**:
    *   Fetches data from `http://127.0.0.1:8000/playlists`.
    *   Dynamically creates HTML cards (`<div>`) for each playlist and appends them to the DOM.
*   **`playlist.js`** (Assumed functionality based on project type):
    *   Reads `playlist_id` from the URL parameters.
    *   Fetches songs for that playlist from the backend.
    *   Renders a list of songs with "Play" buttons.
    *   Handles audio playback logic.
*   **`library.js`**:
    *   Fetches the user's favorites using their User ID (likely stored in `localStorage`).
    *   Displays the list of favorite songs.
*   **`login.js` / `register.js`**:
    *   Captures form input.
    *   Sends `POST` requests to `/login` or `/register`.
    *   On success, stores user info (like `user_id`) in `localStorage` and redirects the user.

---

## 3. Workflow

1.  **Setup**: The backend server starts and ensures the database tables exist.
2.  **Initialization**: Administrator runs `populate_db.py` once to fill the app with music.
3.  **User Entry**: User opens `index.html`.
    *   The page loads.
    *   `home.js` asks the backend for playlists.
    *   Backend queries DB and returns JSON.
    *   Frontend displays playlist cards.
4.  **Navigation**: User clicks a playlist.
    *   Browser goes to `playlist.html?playlist_id=1`.
    *   `playlist.js` gets ID `1`, requests songs for Playlist 1.
    *   User clicks "Play" -> `audio` tag source is updated to the `file_path` URL (e.g., `http://127.0.0.1:8000/audio/song.mp3`).
5.  **Interaction**: User likes a song.
    *   JS sends `POST /favorite`.
    *   Backend updates `favorites` table.

---

## 4. How to Run the Project

### Prerequisites
*   Python installed.
*   Dependencies installed: `pip install -r backend/requirements.txt`.

### Step 1: Start the Backend
1.  Open a terminal.
2.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
3.  (Optional) Populate data if running for the first time:
    ```bash
    python populate_db.py
    ```
4.  Start the server:
    ```bash
    uvicorn app:app --reload
    ```
    *   The server will run at `http://127.0.0.1:8000`.

### Step 2: Start the Frontend
1.  Navigate to the `frontend` folder.
2.  Simply open `index.html` in your web browser (double-click).
    *   *Note: For better behavior (CORS strictness), it is recommended to use a simple HTTP server (e.g., `python -m http.server 5500`), but direct file opening often works if the API allows it.*

---

## 5. How to Test It

1.  **Verify Data**: Run `python check_db.py` in the terminal. You should see lists of songs and playlists.
2.  **Register/Login**:
    *   Go to `register.html`, create a user.
    *   Go to `login.html`, log in. Check simple alerts or console logs to ensure success.
3.  **Browse & Play**:
    *   On Home, click a Playlist.
    *   On the Playlist page, click a song title/play button.
    *   **Test**: Ensure audio plays. If not, check if the mp3 file actually exists in `backend/audio/`.
4.  **Favorites**:
    *   Click "Add to Favorites" (if UI exists).
    *   Go to "Library".
    *   **Test**: The song should appear there.
