# Назва проекту

## Встановлення та запуск

### 1. Клонуйте репозиторій
git clone https://github.com/ваш-username/назва-репо.git
cd назва-репо

### 2. Створіть віртуальне середовище
python -m venv venv

### 3. Активуйте віртуальне середовище
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

### 4. Встановіть залежності
pip install -r requirements.txt

### 5. Виконайте міграції
python manage.py migrate

### 6. Створіть суперюзера (опціонально)
python manage.py createsuperuser

### 7. Запустіть сервер
python manage.py runserver
```

**4. Додайте .env.example**
Якщо використовуєте змінні середовища:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3