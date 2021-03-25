# TDD - Test Driven Development
# Разработка приложений, управляемая тестами
# В начале пишем тесты
from random import choice


# Приветствовать
def greet(name, is_enemy):
    # Утверждаем, что если is_enemy не bool объект
    if not isinstance(is_enemy, bool):
        raise ValueError('is_enemy must be a boolean type')
    if is_enemy:
        return f'Hello {name}! I will kill you, bastard!'
    else:
        return f'Hello {name}! How are you?'


# Хавать бургеры
def eat_burgers(number):
    if number > 3:
        return 'Oh! I overate!'
    else:
        return 'Mmm! That was excellent!'


# Летать
def can_fly(name):
    if name == 'Batman':
        return True
    else:
        return False


# Получить оружие
def get_arsenal():
    return choice(('knife', 'handgun', 'machine gun'))
