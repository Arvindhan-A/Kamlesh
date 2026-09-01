# 🎂 Happy Birthday Kamleshvar · The Passenger Chronicles (June 2025–2026)

An interactive single-page birthday web archive and community memory vault built by **Arvindhan** for **Kamleshvar's** birthday.

---

## ✨ Features

- 🛵 **The Passenger Chronicles**: Featuring genuine archival footage of Kamleshvar driving while Arvindhan sits in the passenger seat (`/static/videos/bike_ride.mp4`).
- 💻 **CS Lab Origin & Evolution**: Interactive Python code terminal and archival photos commemorating the journey with CS Teacher **Hema TS ma'am** from Class 11 in June 2025 to self-hosting server masters today.
- 🎤 **NextGen 26'1 Event Operations**: Visual retrospective on co-organizing and directing the flagship school event.
- 📅 **Interactive Birthday Calendar Flip Widget**: 3D desk calendar with realistic flip mechanics, Web Audio page turns, and era milestones.
- 🕯️ **Interactive Birthday Candles**: 4 blowout candles with realistic flame flicker, wispy smoke particles, puff sound, wish unlocking, and confetti cannons.
- 🏷️ **14-Sticker Memory Tag Cloud & Audit Metrics**: Interactive badge pills unlocking instant memory toasts and friendship audits.
- 📸 **Polaroid Gallery & Lightbox**: 7 high-resolution curated polaroid cards with organic tilt angles and zoom inspection.
- ✍️ **Community Guestbook Studio**: Interactive memory creation with 10 avatars, prompt starters, photo/video attachments, live card preview, draft auto-saving, and session-limited reaction counters (❤️, 🔥, 🫡).
- ⚜️ **Vintage Wax Seal & Grand Finale Letter**: 3D wax seal button unlocking an emotional unfolded brotherhood letter with audio fanfare.
- 📄 **A4 Printable Keepsake Card with Dynamic QR Code**: Single-page dense printable keepsake card containing 6 polaroids, metrics, story chapters, and a **scannable QR code whose destination URL can be changed live from the Admin Dashboard**.
- ⚙️ **Arvindhan's Admin Studio**: Password-protected portal to edit or delete stories, manage attachments, and configure the A4 QR Code target address.

---

## 🍓 Hosting on Raspberry Pi 5 (Single Port)

This application is built to run effortlessly as a single-port service on a Raspberry Pi 5 (or any Linux server).

### 1. Quick Start

```bash
# Clone the repository
git clone https://github.com/Arvindhan-A/Kamlesh.git
cd Kamlesh

# Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch server on single port (0.0.0.0:5000)
./run_server.sh
```

### 2. Custom Port & Environment Variables

You can specify a custom port or host:
```bash
PORT=8080 HOST=0.0.0.0 ./run_server.sh
```

### 3. Systemd Auto-Start on Boot (Raspberry Pi 5)

To keep the server permanently running on your Pi:

```bash
# Copy systemd service file
sudo cp kamlesh.service /etc/systemd/system/

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable kamlesh.service
sudo systemctl start kamlesh.service

# Check live status
sudo systemctl status kamlesh.service
```

---

## ⚙️ Admin Portal & QR Code Setup

1. Open `http://<your-pi-ip>:5000/admin` in your browser.
2. Enter the admin password (`arvindhan`).
3. Set the **A4 QR Code Target URL** to your Raspberry Pi IP or domain (e.g., `http://192.168.1.100:5000` or `https://kamlesh.yourdomain.com`).
4. Scan the live preview QR code on screen to verify.
5. Click **Download / Print A4 Keepsake Card** on the main site to export/print your personalized keepsake PDF with the scannable QR code!

---

## 🛡️ License & Credits

Curated and crafted with pride & zero driving skills by **Arvindhan** for **Kamleshvar**.
Class 11 → Class 12 & Forever.
