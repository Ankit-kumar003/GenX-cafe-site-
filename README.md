# ☕ Gen X Cafe — Full Stack Web Application

A production-ready cafe website with AI chatbot, admin dashboard, online reservations, and full menu management.

## Tech Stack
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Backend:** Python Flask
- **Database:** MySQL
- **AI:** GROQ API (llama3-70b-8192)
- **Auth:** Flask Session + Werkzeug password hashing

## Quick Setup

### 1. Clone & Install
```bash
git clone <repo>
cd genxcafe
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your MySQL credentials and GROQ API key
```

### 3. Setup Database
```bash
mysql -u root -p < schema.sql
```

### 4. Run
```bash
python app.py
```

Visit: http://localhost:5000

## Admin Login
- URL: http://localhost:5000/login
- Email: `admin@genxcafe.com`
- Password: `Admin@123`

> **Note:** After first login, reset the admin password via the Users panel.

## Features
| Feature | Description |
|---|---|
| Public Website | Home, Menu, Booking, About, Contact |
| AI Chatbot | GROQ-powered Barista Bot on all pages |
| Admin Dashboard | Stats, charts (Chart.js), CRUD management |
| Reservations | Double-booking prevention, availability check |
| Menu Management | Category filter, search, image upload |
| Dark/Light Mode | Persisted via localStorage |
| Responsive | Mobile-first Bootstrap 5 design |

## Project Structure
```
genxcafe/
├── app.py              # Flask entry point
├── config.py           # Configuration
├── schema.sql          # Database schema + seed data
├── requirements.txt
├── .env.example
├── routes/
│   ├── public.py       # Public pages
│   ├── auth.py         # Login/logout
│   ├── admin.py        # Admin CRUD
│   └── chatbot.py      # GROQ AI chatbot
├── models/
│   └── db.py           # MySQL helper
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── menu.html
│   ├── booking.html
│   ├── about.html
│   ├── contact.html
│   ├── auth/
│   └── admin/
├── static/
│   ├── css/main.css
│   ├── css/admin.css
│   ├── js/main.js
│   ├── js/admin.js
│   └── images/
└── uploads/            # User-uploaded menu images
```

## Environment Variables
| Key | Description |
|---|---|
| `SECRET_KEY` | Flask session secret |
| `MYSQL_HOST` | MySQL host (default: localhost) |
| `MYSQL_USER` | MySQL username |
| `MYSQL_PASSWORD` | MySQL password |
| `MYSQL_DB` | Database name (default: genxcafe) |
| `GROQ_API_KEY` | Get from https://console.groq.com |

## Get GROQ API Key
1. Visit https://console.groq.com
2. Sign up / Login
3. Create API Key
4. Add to `.env` as `GROQ_API_KEY=gsk_...`
