# Manual Login Flask App

Minimal Flask login form. User email va parolni kiritadi, server `admin.txt` fayliga saqlaydi, keyin "Hello, World!" sahifasiga o'tadi.

## Project Structure

```
.
├── app.py              # Flask ilovasi
├── requirements.txt    # Python kutubxonalar
├── .env.example        # Environment variable template
├── admin.txt           # Saqlangan loginlar (avtomatik yaratiladi)
├── templates/
│   ├── login.html      # Login formasi
│   └── hello.html      # "Hello, World!" sahifasi
└── static/
    ├── css/style.css
    └── js/main.js
```

## Setup

```bash
pip install -r requirements.txt
```

`.env` fayl yaratish:

```bash
cp .env.example .env
```

`.env` ichiga `SECRET_KEY` yozing (ixtiyoriy, bo'lmasa avtomatik generatsiya qilinadi):

```
SECRET_KEY=
```

## Ishga tushirish

```bash
python app.py
```

Brauzerda http://localhost:5000

## Qanday ishlaydi

1. User `http://localhost:5000/` ochadi → login formasi ko'rinadi
2. Email va parolni yozadi → "Kirish" tugmasini bosadi
3. Server ma'lumotlarni `admin.txt` ga qo'shib yozadi (append)
4. Session'ga saqlaydi → `/hello` sahifasiga yo'naltiradi
5. `/hello` da "Hello, World!" chiqadi

## admin.txt formati

Har bir kirish yangi qatorga yoziladi:

```
[2026-06-30 12:34:56] Email: user@example.com | Parol: mypassword
```
