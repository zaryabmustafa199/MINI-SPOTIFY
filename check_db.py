import sqlite3

conn = sqlite3.connect('backend/database.db')
c = conn.cursor()

print("Database Contents:")
print("\nPlaylists:")
for row in c.execute('SELECT id, name FROM playlists'):
    print(f"  {row[0]}: {row[1]}")

print("\nSongs:")
for row in c.execute('SELECT id, title, playlist_id FROM songs'):
    print(f"  {row[0]}: {row[1]} (playlist {row[2]})")

print("\nUsers:")
for row in c.execute('SELECT id, username FROM users'):
    print(f"  {row[0]}: {row[1]}")

conn.close()
