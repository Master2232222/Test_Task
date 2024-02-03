from flask import Flask, render_template, request, make_response
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


@app.route('/')# Определение маршрута
def hello_world():
    return render_template('sign_up_and_sign_in.html')


@app.route('/registor', methods=["POST"])# Определение маршрута и метода запроса
def registor():#Функция внесения данных в бд
    login = request.form['login']#получение значения поля "логин" из запроса
    email = request.form['email']#получение значения поля "электронная_почта" из запроса
    conn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="test_task")#установка соединения с базой данных MySQL
    cursor = conn.cursor()#создание курсора для выполнения SQL-запросов
    query1 = "SELECT count(*) FROM users WHERE электронная_почта = %s"# создание SQL-запроса для проверки наличия пользователя с таким же адресом электронной почты
    cursor.execute(query1, (email,))#выполнение SQL-запроса с передачей значения переменной email
    result = cursor.fetchone()#получение результата выполнения SQL-запроса
    if result[0] != 0:#проверка, есть ли уже пользователь с таким же адресом электронной почты
        response1 = f"{login}, вы уже зарегистрированы"#формирование ответа, если пользователь уже зарегистрирован
        return response1#возвращаем ответ
    password = request.form['password']#получение значения поля "пароль" из запроса
    password = generate_password_hash(password)#хэширование пароля пользователя
    myconn1 = mysql.connector.connect(host="localhost", user="root", passwd="root", database="test_task")#установка соединения с базой данных MySQL для добавления пользователя
    cur1 = myconn1.cursor()#создание курсора для выполнения SQL-запросов
    #созданиеSQL - запроса для добавления нового пользователя в базу данных
    sql1 = f"""INSERT INTO `users`( `логин`, `электронная_почта`, `пароль`)
    VALUES ('{login}', '{email}', '{password}')"""
    try:
        cur1.execute(sql1)# выполнение SQL-запроса для добавления пользователя
        myconn1.commit()#подтверждение изменений в базе данных
    except:#обработка исключения, если произошла ошибка при добавлении пользователя
        myconn1.rollback()#отмена изменений в базе данных
        myconn1.close()#
    response = make_response(f'{login} ,Все прошло успешно!!!')#формирование ответа сервера
    response.set_cookie('username', login)# установка cookie с именем пользователя
    return response#возврат ответа сервера


#Обрабатываем регистрацию новых пользователей
#Извлекаем логин пользователя, адрес электронной почты и пароль из запроса, проверяем, зарегистрирован ли адрес электронной почты, хэшируем пароль, а затем вставляем информацию о пользователе в таблицу "users" в базу данных 'my_translator'


@app.route('/check_user', methods=["POST"])# Определение маршрута и метода запроса
def check_user():
    target_email = request.form['target_email']# Получение значения электронной почты из формы запроса
    target_password = request.form['target_password']# Получение значения пароля из формы запроса
    conn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="test_task")#Установка соединения с базой данных
    try:
        cursor = conn.cursor() # Создание курсора для выполнения SQL-запросов
        # SQL-запрос для выборки данных из таблицы users
        query = "SELECT * FROM users WHERE электронная_почта = %s"
        cursor.execute(query, (target_email, )) # Выполнение SQL-запроса с передачей значения электронной почты
        result = cursor.fetchone()# Получение результата выполнения SQL-запроса
        if result == None:# Проверка, есть ли пользователь в базе данных
            return f"Вас нет в базе данных,вы должны зарегистрироватся"# Возвращение сообщения о необходимости регистрации
        else:
            if result[2].lower() == target_email.lower() and check_password_hash(result[3], target_password):# Проверка соответствия электронной почты и пароля
                response = make_response(f"{target_email}, вы вошли в аккаунт")# Создание ответа сервера
                response.set_cookie('email', target_email)# Установка cookie с электронной почтой пользователя
                return response# Возвращение ответа сервера
            else:
                return 'ошибка' # Возвращение сообщения об ошибке
    except mysql.connector.Error as err:# Обработка ошибок при работе с базой данных
        return "Ошибка при работе с базой данных:", {err} # Возвращение сообщения об ошибке
    finally:
        if conn:
            conn.close() # Закрытие соединения с базой данных
#обрабатываем процесс аутентификации пользователя
#Извлекаем адрес электронной почты пользователя и пароль из запроса, запрашиваем таблицу "users" в базе данных 'my_translator', чтобы проверить, существует ли пользователь и совпадает ли пароль с хэшированным паролем


if __name__ == '__main__':
    app.run()
