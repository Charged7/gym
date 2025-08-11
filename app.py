from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_argon2 import Argon2
import sqlite3
import os
import secrets
from flask_mail import Mail, Message
import re
import json
from markupsafe import Markup
import time
import urllib.parse


app = Flask(__name__)
app.secret_key = secrets.token_hex(16) 
argon2 = Argon2(app)

# Настройки базы
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'gym_users.db')

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                gmail TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                phone TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'client'
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
    MAIL_USERNAME='hubaibohdan258@gmail.com',     
    MAIL_PASSWORD='jicq fnow zcrg xbdx',        
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
    return render_template('index.html')

@app.route('/trener_shablon')
def trener_shablon():
    return render_template('trener_shablon.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("POST-запрос получен в /register")  # debug
        name = request.form.get('name', '').strip()
        surname = request.form.get('surname', '').strip()
        gmail = request.form.get('gmail', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        phone = request.form.get('phone', '').strip()

        errors = {}

        # Проверка имени
        for symbol in name:
            if symbol.isdigit() or symbol in "!@#$%^&*()?/;:][}{":
                errors['name'] = "Використовуйте лише букви."
                break
        
        if not name:
            errors['name'] = "Це поле є обов'язковим."
        elif not re.match(r"^[A-Za-zА-Яа-яЁёІіЇїЄє\s'-]{2,30}$", name):
            errors['name'] = "Введіть коректне ім'я!"

        # Проверка фамилии
        if not surname:
            errors['surname'] = "Це поле є обов'язковим."
        elif not re.match(r"^[A-Za-zА-Яа-яЁёІіЇїЄє\s'-]{2,30}$", surname):
            errors['surname'] = "Введіть коректне прізвище!"

        # Проверка email
        if not gmail:
            errors['gmail'] = "Це поле є обов'язковим."
        elif '@' not in gmail or '.' not in gmail:
            errors['gmail'] = "Введiть коректний email!"

        # Проверка номера
        if not phone:
            errors['phone'] = "Це поле є обов'язковим."
        elif not re.match(r'^\+?\d{10,15}$', phone):
            errors['phone'] = "Введiть коректний номер телефона."

        # Проверка пароля
        if not password:
            errors['password'] = "Це поле є обов'язковим."
        elif len(password) < 6:
            errors['password'] = "Пароль повинен бути не менше 6 символiв!"

        # Проверка совпадения паролей
        if not confirm_password:
            errors['confirm_password'] = "Це поле є обов'язковим."
        elif password != confirm_password:
            errors['confirm_password'] = "Паролi не спiвпадають!"
            return render_template('register.html',gmail=gmail, password=password, errors=errors)

        # Если есть ошибки — возвращаем с ошибками
        if errors:
            return render_template('register.html',
                                   errors=errors,
                                   name=name, 
                                   surname=surname,
                                   gmail=gmail,
                                   phone=phone,
                                   password=password, 
                                   confirm_password=confirm_password)

        # Хеширование и сохранение
        hashed = argon2.generate_password_hash(password)

        # Проверка на существование пользователя
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
            "INSERT INTO users (name, surname, gmail, phone, password) VALUES (?, ?, ?, ?, ?)", 
            (name, surname, gmail, phone, hashed)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            errors['gmail'] = "Пользователь с таким email уже существует!"
            return render_template('register.html', gmail=gmail, errors=errors)
        finally:
            conn.close()

        flash("✅ Регистрация прошла успешно!", "success")
        return redirect(url_for('login'))

    return render_template('register.html', errors= {}, name='', surname='', gmail='', phone='', password='', confirm_password='')


@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = {}
    gmail = ''

    if request.method == 'POST':
        gmail = request.form.get('gmail', '').strip().lower()
        password = request.form.get('password', '')

        # Проверка email
        if '@' not in gmail or '.' not in gmail:
            errors['gmail'] = "Введiть коректний email!"

        # Если email невалиден — сразу показываем ошибку
        if errors:
            return render_template('login.html', gmail=gmail, errors=errors)

        # Проверяем есть ли пользователь
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM users WHERE gmail = ?", (gmail,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            errors['gmail'] = "Користувач не знайдений"
            return render_template('login.html', gmail=gmail, errors=errors)

        stored_hash, role = row

        if not argon2.check_password_hash(stored_hash, password):
            errors['password'] = "Неправильний пароль"
            return render_template('login.html', gmail=gmail, errors=errors)

        # Успешный вход, редирект в зависимости от роли
        if gmail == 'hubaibohdan258@gmail.com':
            return redirect(url_for('admin_cabinet'))  # для админа

        if role == 'trainer':
            return redirect(url_for('trener_cabinet'))  # кабинет тренера
        else:
        # для остальных (например, клиенты)
            return redirect(url_for('users'))

    return render_template('login.html', errors={}, gmail='')


@app.route('/users', methods=['GET', 'POST'])
def users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')
        user_id = request.form.get('user_id')

        if action == 'delete':
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('users'))

        elif action == 'update':
            name = request.form.get('name', '').strip()
            surname = request.form.get('surname', '').strip()
            gmail = request.form.get('gmail', '').strip().lower()
            phone = request.form.get('phone', '').strip()
            role = request.form.get('role', 'client')

            # Добавь тут валидацию по желанию

            cursor.execute(
                "UPDATE users SET name = ?, surname = ?, gmail = ?, phone = ?, role = ? WHERE id = ?",
                (name, surname, gmail, phone, role, user_id)
            )
            conn.commit()
            conn.close()

            # Если запрос AJAX, вернуть текст OK
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return "OK"
            else:
                return redirect(url_for('users'))   

    # фильтрация по email
    search_query = request.args.get('search', '').strip()

    if search_query:
        cursor.execute("""
            SELECT id, name, surname, gmail, phone, role
            FROM users
            WHERE LOWER(gmail) LIKE LOWER(?)
            ORDER BY id ASC
        """, (f'%{search_query}%',))
    else:
        cursor.execute("SELECT id, name, surname, gmail, phone, role FROM users ORDER BY id ASC")

    all_users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=all_users, search_query=search_query, errors={}, gmail='')

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    errors = {}
    gmail = ''
    success_message = ''

    if request.method == 'POST':
        # Проверяем таймер (лимит в 60 секунд)
        last_request_time = session.get('last_reset_request')
        now = time.time()

        if last_request_time and now - last_request_time < 60:
            remaining = int(60 - (now - last_request_time))
            errors['gmail'] = f"⏳ Ви зможете надіслати запит знову через {remaining} сек."
            return render_template('reset_password_request.html', errors=errors, gmail=gmail)

        gmail = request.form.get('gmail', '').strip().lower()

        # Валидация email
        if not gmail:
            errors['gmail'] = "Це поле є обов'язковим."
        elif '@' not in gmail or '.' not in gmail:
            errors['gmail'] = "Введiть коректний email!"

        if errors:
            return render_template('reset_password_request.html', errors=errors, gmail=gmail)

        # Проверяем, есть ли пользователь
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE gmail = ?", (gmail,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            errors['gmail'] = "Користувач з таким email не знайдений!"
            return render_template('reset_password_request.html', errors=errors, gmail=gmail)

        # Создаем токен и отправляем письмо
        token = secrets.token_urlsafe(16)
        reset_tokens[token] = gmail
        reset_link = url_for('reset_password', token=token, _external=True)

        send_email(
            to_email=gmail,
            subject="Вiдновлення пароля",
            body=f"Щоб вiдновити пароль, перейдіть за посиланням:\n{reset_link}"
        )

        # Сохраняем время последнего запроса в сессию
        session['last_reset_request'] = now

        success_message = "✅ Посилання для вiдновлення пароля вiдправлене на вашу пошту!"

    return render_template('reset_password_request.html',
                           errors=errors,
                           gmail=gmail,
                           success_message=success_message)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    gmail = reset_tokens.get(token)
    success_message = ''
    errors = {}

    if not gmail:
        return "❌ Неверная или просроченная ссылка", 400

    if request.method == 'POST':
        new_password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        # Проверка пустого пароля
        if not new_password:
            errors['password'] = "Введіть новий пароль!"

        # Проверка подтверждения пароля
        if not confirm_password:
            errors['confirm_password'] = "Введіть підтвердження пароля!"
        elif new_password and confirm_password != new_password:
            errors['confirm_password'] = "Паролі не збігаються!"

        # Если есть ошибки, возвращаем форму с сообщениями
        if errors:
            return render_template(
                'reset_password.html',
                errors=errors,
                success_message='',
                password=new_password,
                confirm_password=confirm_password
            )

        # Хешируем и обновляем пароль в базе
        hashed = argon2.generate_password_hash(new_password)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE gmail = ?", (hashed, gmail))
        conn.commit()
        conn.close()

        # Удаляем токен после успешного сброса
        del reset_tokens[token]

        # Готовим сообщение об успехе
        login_url = url_for('login')
        success_message = Markup(
            f"✅ Пароль успiшно змiнений! "
            f'Можете увiйти з новим паролем. '
            f'<a style="color:blue;" href="{login_url}">Увiйти</a>'
        )

    return render_template('reset_password.html',
                           success_message=success_message,
                           errors=errors)


@app.route('/admin_cabinet')
def admin_cabinet():
    return render_template('admin_cabinet.html')

@app.route('/trener_cabinet')
def trener_cabinet():
    name = request.args.get('name')  # получит ?name=Иван
    return render_template('trener_cabinet.html', name=name)


# Загрузка данных тренеров из JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'static', 'json', 'treners.json')

with open(JSON_PATH, encoding='utf-8') as f:
    trenery_data = json.load(f)

@app.route('/save_geo_data', methods=['POST'])
def save_geo_data():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Нет данных"}), 400
    
    # Логируем в консоль (можно убрать, если не нужно)
    print(f"[GEO-LOG] Получены данные: {data}")
    
    # Записываем в файл (добавляем новую строку с JSON)
    with open('geo_data_logs.json', 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
        f.write('\n')  # Разделитель записей — новая строка
    
    return jsonify({"status": "ok"})

# @app.route('/test_mail')
# def test_mail():
#     try:
#         send_email('hubaibohdan258@gmail.com', 'Тест', 'Это тестовое письмо')
#         return "Письмо отправлено"
#     except Exception as e:
#         return f"Ошибка при отправке письма: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
