from flask import Flask, render_template, request # импортируем необходимые иструменты
import psycopg2

app = Flask(__name__) # создаём приложение

conn = psycopg2.connect(database="service_db", # подключение к базе данных
                        user="postgres",
                        password="123456789",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['GET']) # декоратор
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST']) # декоратор
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username:
        return render_template('login.html', error="Пожалуйста введите логин")
    if not password:
        return render_template('login.html', error="Пожалуйста введите пароль")

    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))

    records = list(cursor.fetchall())
    if not records:
        return render_template('login.html', error="Введенного пользователя не существует")
    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])