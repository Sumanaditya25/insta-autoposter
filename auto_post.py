# auto_post.py - CLOUD VERSION (Render.com)
from instagrapi import Client
import os
from datetime import datetime

# === GET FROM RENDER ENVIRONMENT VARIABLES ===
USERNAME = os.getenv('IG_USERNAME')
PASSWORD = os.getenv('IG_PASSWORD')
POSTS_FOLDER = "posts"

# Login with session
cl = Client()
session_file = "/tmp/session.json"

try:
    cl.load_settings(session_file)
    print("Session loaded")
except:
    print("No session, logging in...")
cl.login(USERNAME, PASSWORD)
cl.dump_settings(session_file)

# Find next post
def get_next_post():
    files = sorted([f for f in os.listdir(POSTS_FOLDER) if f.endswith(('.jpg', '.mp4'))])
    for media_file in files:
        base = media_file.split('.')[0]
        txt_file = f"{base}.txt"
        media_path = os.path.join(POSTS_FOLDER, media_file)
        txt_path = os.path.join(POSTS_FOLDER, txt_file)
        
        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as f:
                caption = f.read().strip()
            return media_path, caption, base
    return None, None, None

# Upload
media_path, caption, post_id = get_next_post()
if not media_path:
    print("All 50 posts uploaded!")
    exit(0)

print(f"Uploading {post_id}...")

if media_path.endswith(".jpg"):
    cl.photo_upload(path=media_path, caption=caption)
elif media_path.endswith(".mp4"):
    cl.video_upload(path=media_path, caption=caption)

# Move to posted
os.makedirs("posted", exist_ok=True)
os.rename(media_path, f"posted/{os.path.basename(media_path)}")
os.rename(f"{POSTS_FOLDER}/{post_id}.txt", f"posted/{post_id}.txt")

print(f"Posted {post_id} to Instagram + Threads (auto-cross-post)")
