from flask import Flask, render_template, request, redirect, url_for, flash
from flask_argon2 import Argon2
import sqlite3
import os
import secrets
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = secrets.token_hex(16) 
argon2 = Argon2(app)

# Настройки базы
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'users.db')

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,   -- email пользователя
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

# Конфигурация Flask-Mail (пароль приложения Gmail)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='hubaibohdan258@gmail.com',      # замени на свою почту
    MAIL_PASSWORD='nllw wyub eeom ujbo',         # пароль приложения Gmail
    MAIL_DEFAULT_SENDER='hubaibohdan258@gmail.com'
)

mail = Mail(app)

# В памяти храним токены сброса пароля (для простоты, в реальном проекте лучше БД)
reset_tokens = {}

def send_email(to_email, subject, body):
    msg = Message(subject=subject, recipients=[to_email], body=body)
    mail.send(msg)

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Проверка email
        if '@' not in username:
            flash("❌ Введите корректный email", "danger")
            return render_template('register.html', username=username, password=password, confirm_password=confirm_password)

        # Проверка совпадения
        if password != confirm_password:
            flash("❌ Пароли не совпадают", "danger")
            return render_template('register.html', username=username, password=password, confirm_password=confirm_password)

        # Проверка длины
        if len(password) < 6:
            flash("❌ Пароль должен быть не менее 6 символов", "danger")
            return render_template('register.html', username=username, password=password, confirm_password=confirm_password)

        # Хеширование и сохранение
        hashed = argon2.generate_password_hash(password)

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            conn.commit()
        except sqlite3.IntegrityError:
            flash("❌ Такой пользователь уже существует", "danger")
            return render_template('register.html', username=username)
        finally:
            conn.close()

        flash("✅ Регистрация прошла успешно!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/users', methods=['GET', 'POST'])
def users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            email = request.form.get('email')
            if email:
                cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (email, ''))
                conn.commit()

        elif action == 'delete':
            user_id = request.form.get('user_id')
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()

        elif action == 'update':
            user_id = request.form.get('user_id')
            new_email = request.form.get('new_email')
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_email, user_id))
            conn.commit()

    # фильтрация по email
    search_query = request.args.get('search', '')
    if search_query:
        cursor.execute("SELECT id, username FROM users WHERE username LIKE ? ORDER BY id ASC", (f'%{search_query}%',))
    else:
        cursor.execute("SELECT id, username FROM users ORDER BY id ASC")

    all_users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=all_users, search_query=search_query)


# ---------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password')

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return '❌ Пользователь не найден', 404

        stored_hash = row[0]
        if argon2.check_password_hash(stored_hash, password):
            return '✅ Успешный вход'
        else:
            return '❌ Неверный пароль', 401

    return render_template('login.html')

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()

        if '@' not in username:
            return "❌ Введите корректный email для сброса пароля", 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            token = secrets.token_urlsafe(16)
            reset_tokens[token] = username
            reset_link = url_for('reset_password', token=token, _external=True)

            send_email(
                to_email=username,
                subject="Сброс пароля",
                body=f"Чтобы сбросить пароль, перейдите по ссылке:\n{reset_link}"
            )

            return "✅ Ссылка для сброса пароля отправлена на вашу почту."
        else:
            return "❌ Пользователь не найден", 404

    return render_template('reset_password_request.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    username = reset_tokens.get(token)

    if not username:
        return "❌ Неверная или просроченная ссылка", 400

    if request.method == 'POST':
        new_password = request.form.get('password')
        if not new_password:
            return "❌ Введите новый пароль", 400

        hashed = argon2.generate_password_hash(new_password)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed, username))
        conn.commit()
        conn.close()

        del reset_tokens[token]

        return "✅ Пароль успешно изменён! Можете войти с новым паролем."

    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
