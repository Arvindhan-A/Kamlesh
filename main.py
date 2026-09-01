import os
import json
import time
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
application = app  # WSGI application alias
app.secret_key = os.environ.get("SECRET_KEY", "kamleshvar_birthday_key_2026_arvindhan")
app.config["MAX_CONTENT_LENGTH"] = 60 * 1024 * 1024  # 60MB max upload

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STORIES_FILE = os.path.join(DATA_DIR, "stories.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
UPLOAD_DIR = os.path.join(app.static_folder, "uploads")
PHOTO_DIR = os.path.join(app.static_folder, "photos")
VIDEO_DIR = os.path.join(app.static_folder, "videos")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

ALLOWED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
ALLOWED_VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv"}

DEFAULT_SETTINGS = {
    "qr_code_url": "https://kamlesh.gaiasentinel.online",
    "site_title": "Happy Birthday Kammu 🎂",
    "admin_password": os.environ.get("ADMIN_PASSWORD", "arvindhan")
}

SURPRISE_MESSAGE = (
    "You spent years in the driver’s seat steering through every road and midnight turn we ever took—"
    "while I sat behind contributing zero GPS and 100% moral support. Consider this archive "
    "Arvindhan’s way of finally taking the wheel. Happy Birthday, Kamleshvar! 🎂🛵✨"
)

PHOTO_METADATA = {
    "kamlesh_cycle_sunny.jpg": {
        "title": "Sunny Day & The Cycle",
        "caption": "Kamleshvar in his natural element enjoying the sunshine and cycle ride 🚲☀️",
        "date": "Archival Snapshot · Summer Vibes"
    },
    "michael_movie_theatre.jpg": {
        "title": "Michael Movie Night",
        "caption": "Arvindhan and Kamleshvar catching the Michael movie in the theatre 🍿🎬",
        "date": "Cinema Night · Michael Outing"
    },
    "michael_movie_outing.jpg": {
        "title": "Michael Movie Outing",
        "caption": "Pre-show vibes and hanging out before the movie starts 🎟️🥤",
        "date": "Movie Day · Good Times"
    },
    "classmates_group_photo.jpg": {
        "title": "All Classmates With Kamleshvar",
        "caption": "The whole gang together with Kamleshvar in school 🏫✨",
        "date": "Class 11 & Classmates · Iconic"
    },
    "hema_ts_cs_teacher_group.jpg": {
        "title": "With Hema TS (CS Teacher)",
        "caption": "Group photo with Hema TS ma'am — where our CS journey originally kicked off in June 2025! 💻👩‍🏫",
        "date": "Class 11 CS Lab · June 2025"
    },
    "marina_beach_cycling_first_hangout.jpg": {
        "title": "First Hangout · Marina Beach",
        "caption": "Our very first official hangout — early morning cycling along Marina Beach! The start of countless adventures 🏖️🚲",
        "date": "First Hangout · Sunrise Cycling"
    },
    "nextgen_2026_event_organizers.jpg": {
        "title": "NextGen 26'1 Event Organizers",
        "caption": "Pulling off NextGen 26'1 together — from backstage chaos and tech setups to running the entire event like absolute champions! 🎤🚀",
        "date": "NextGen 26'1 · Event Operation Legends"
    }
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Merge with defaults in case of missing keys
            for k, v in DEFAULT_SETTINGS.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception as e:
        print(f"Error loading settings: {e}")
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving settings: {e}")


def load_stories():
    if not os.path.exists(STORIES_FILE):
        return []
    try:
        with open(STORIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading stories: {e}")
        return []


def save_stories(stories):
    try:
        with open(STORIES_FILE, "w", encoding="utf-8") as f:
            json.dump(stories, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving stories: {e}")


@app.route("/")
def home():
    exts = (".png", ".jpg", ".jpeg", ".gif", ".webp")
    photo_files = sorted(f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(exts)) if os.path.isdir(PHOTO_DIR) else []

    photos_data = []
    for f in photo_files:
        meta = PHOTO_METADATA.get(f, {
            "title": "Cherished Memory",
            "caption": "Good times and unforgettable laughs with Kamleshvar.",
            "date": "Archival Photo · Memories"
        })
        photos_data.append({
            "filename": f,
            "title": meta["title"],
            "caption": meta["caption"],
            "date": meta["date"]
        })

    stories = load_stories()
    settings = load_settings()
    user_reactions = session.get("reacted_posts", {})

    return render_template(
        "index.html",
        stories=stories,
        photos=photos_data,
        surprise_message=SURPRISE_MESSAGE,
        user_reactions=user_reactions,
        qr_code_url=settings.get("qr_code_url", DEFAULT_SETTINGS["qr_code_url"]),
        settings=settings
    )


@app.route("/api/stories", methods=["POST"])
def add_story():
    author = request.form.get("author", "").strip()
    role = request.form.get("role", "Friend").strip()
    title = request.form.get("title", "").strip()
    text = request.form.get("text", "").strip()
    avatar = request.form.get("avatar", "🎂").strip()

    if not author or not text:
        return jsonify({"success": False, "error": "Author name and memory text are required."}), 400

    media_type = None
    media_url = None

    if "media" in request.files:
        file = request.files["media"]
        if file and file.filename:
            orig_filename = secure_filename(file.filename)
            ext = os.path.splitext(orig_filename)[1].lower()

            if ext in ALLOWED_IMAGE_EXTS:
                media_type = "image"
            elif ext in ALLOWED_VIDEO_EXTS:
                media_type = "video"
            else:
                return jsonify({"success": False, "error": f"Unsupported file type ({ext}). Use image or video."}), 400

            unique_filename = f"{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
            filepath = os.path.join(UPLOAD_DIR, unique_filename)
            file.save(filepath)
            media_url = f"/static/uploads/{unique_filename}"

    new_story = {
        "id": f"story_{int(time.time())}_{uuid.uuid4().hex[:6]}",
        "author": author,
        "role": role or "Friend",
        "title": title or "A Memory with Kamleshvar",
        "text": text,
        "avatar": avatar or "🎂",
        "media_type": media_type,
        "media_url": media_url,
        "reactions": {"heart": 1, "fire": 0, "salute": 0},
        "created_at": datetime.now().strftime("%b %d, %Y · %I:%M %p")
    }

    stories = load_stories()
    stories.insert(0, new_story)
    save_stories(stories)

    return jsonify({"success": True, "story": new_story})


@app.route("/api/stories/<story_id>/react", methods=["POST"])
def react_to_story(story_id):
    data = request.get_json() or {}
    rx_type = data.get("type", "heart")
    if rx_type not in ["heart", "fire", "salute"]:
        rx_type = "heart"

    # Session limit enforcement
    user_reactions = session.get("reacted_posts", {})
    story_rx = user_reactions.get(story_id, [])

    stories = load_stories()
    target_story = None
    for s in stories:
        if s.get("id") == story_id:
            target_story = s
            break

    if not target_story:
        return jsonify({"success": False, "error": "Story not found"}), 404

    if "reactions" not in target_story:
        target_story["reactions"] = {"heart": 0, "fire": 0, "salute": 0}

    is_active = False
    if rx_type in story_rx:
        # User already reacted with this type in this session -> Toggle off (decrement)
        target_story["reactions"][rx_type] = max(0, target_story["reactions"].get(rx_type, 1) - 1)
        story_rx.remove(rx_type)
        is_active = False
    else:
        # Add reaction
        target_story["reactions"][rx_type] = target_story["reactions"].get(rx_type, 0) + 1
        story_rx.append(rx_type)
        is_active = True

    user_reactions[story_id] = story_rx
    session["reacted_posts"] = user_reactions
    session.modified = True

    save_stories(stories)
    return jsonify({
        "success": True,
        "active": is_active,
        "reactions": target_story["reactions"]
    })


# =========================================================
# ADMIN PORTAL (EDIT STORIES, DELETE & CONFIGURE QR LINK)
# =========================================================
@app.route("/admin", methods=["GET", "POST"])
def admin():
    settings = load_settings()
    admin_pw = settings.get("admin_password", DEFAULT_SETTINGS["admin_password"])

    if request.method == "POST":
        password = request.form.get("password", "").strip()
        if password == admin_pw:
            session["is_admin"] = True
            return redirect(url_for("admin"))
        else:
            return render_template("admin.html", is_admin=False, error="Incorrect Admin Password", settings=settings)

    is_admin = session.get("is_admin", False)
    stories = load_stories() if is_admin else []
    return render_template(
        "admin.html",
        is_admin=is_admin,
        stories=stories,
        settings=settings,
        qr_code_url=settings.get("qr_code_url", DEFAULT_SETTINGS["qr_code_url"])
    )


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("home"))


@app.route("/api/admin/settings", methods=["POST"])
def admin_update_settings():
    if not session.get("is_admin"):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    data = request.get_json() or {}
    qr_code_url = data.get("qr_code_url", "").strip()
    admin_password = data.get("admin_password", "").strip()

    settings = load_settings()
    if qr_code_url:
        settings["qr_code_url"] = qr_code_url
    if admin_password:
        settings["admin_password"] = admin_password

    save_settings(settings)
    return jsonify({"success": True, "settings": settings})


@app.route("/api/admin/stories/<story_id>/edit", methods=["POST"])
def admin_edit_story(story_id):
    if not session.get("is_admin"):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    data = request.get_json() or {}
    author = data.get("author", "").strip()
    role = data.get("role", "").strip()
    title = data.get("title", "").strip()
    text = data.get("text", "").strip()
    avatar = data.get("avatar", "🎂").strip()

    if not author or not text:
        return jsonify({"success": False, "error": "Author and text cannot be blank"}), 400

    stories = load_stories()
    target = None
    for s in stories:
        if s.get("id") == story_id:
            s["author"] = author
            s["role"] = role
            s["title"] = title
            s["text"] = text
            s["avatar"] = avatar
            target = s
            break

    if not target:
        return jsonify({"success": False, "error": "Story not found"}), 404

    save_stories(stories)
    return jsonify({"success": True, "story": target})


@app.route("/api/admin/stories/<story_id>/delete", methods=["POST"])
def admin_delete_story(story_id):
    if not session.get("is_admin"):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    stories = load_stories()
    initial_len = len(stories)
    deleted_story = None

    for i, s in enumerate(stories):
        if s.get("id") == story_id:
            deleted_story = stories.pop(i)
            break

    if not deleted_story or len(stories) == initial_len:
        return jsonify({"success": False, "error": "Story not found"}), 404

    # Remove attached file if it exists in uploads
    if deleted_story.get("media_url") and deleted_story["media_url"].startswith("/static/uploads/"):
        filename = os.path.basename(deleted_story["media_url"])
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing uploaded file {file_path}: {e}")

    save_stories(stories)
    return jsonify({"success": True})


if __name__ == "__main__":
    import sys
    host = os.environ.get("HOST", "0.0.0.0")
    port_str = os.environ.get("PORT", "1051")
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port_str = sys.argv[1]
    try:
        port = int(port_str)
    except ValueError:
        port = 1051
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in ("true", "1", "yes")
    print(f"🚀 Starting Kamleshvar Birthday Server on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)
