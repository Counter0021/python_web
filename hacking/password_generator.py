# Генерация паролей
from random import choice


# Генерация хороших паролей
# Сложно взламываемые пароли
def good_password_generator(length=10):
    alphabet = 'abcdefghijklmnopqrstuvwxyz' + 'abcdefghijklmnopqrstuvwxyz'.upper() + '1234567890!@#$%^&*()_+-='
    password = ''
    for i in range(length):
        password += choice(alphabet)
    print(password)


# Генерация плохих паролей
def bad_password_generator():
    global counter
    print(passwords_bad[counter])
    counter += 1


# Плохие пароли
with open('passwords.txt') as file:
    content = file.read()
    passwords_bad = content.split('\n')
counter = 0

good_password_generator()
bad_password_generator()
