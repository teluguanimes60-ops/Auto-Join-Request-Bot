# 🤖 Auto Join Request Bot

A Telegram Bot that automatically accepts join requests for multiple channels.

---

## ✨ Features

- ✅ Auto Accept Join Requests
- ✅ Unlimited Channels
- ✅ Custom Welcome Messages
- ✅ Auto Delete Welcome Messages
- ✅ Per Channel Settings
- ✅ Owner Panel
- ✅ Admin Panel
- ✅ Statistics
- ✅ Broadcast
- ✅ MongoDB Database
- ✅ GitHub + Render Deployment
- ✅ FastAPI Health Check

---

# Requirements

- Python 3.11+
- MongoDB Atlas
- Telegram Bot Token
- API ID
- API HASH

---

# Installation

```bash
git clone https://github.com/USERNAME/Auto-Join-Request-Bot.git

cd Auto-Join-Request-Bot

pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```
API_ID=
API_HASH=
BOT_TOKEN=
MONGO_URI=
OWNER_ID=
PORT=10000
```

---

# Run

```
python bot.py
```

---

# Deploy on Render

- Connect GitHub Repository
- Add Environment Variables
- Deploy

Health Check

```
/health
```

---

# Commands

```
/start
/owner
/stats
/addadmin
/removeadmin
/broadcast
```

---

# Project Structure

```
Auto-Join-Request-Bot
│
├── bot.py
├── config.py
├── buttons.py
├── requirements.txt
├── render.yaml
│
├── database
├── handlers
├── utils
│
└── README.md
```

---

# License

MIT License

---

Made with ❤️ using Pyrogram.
