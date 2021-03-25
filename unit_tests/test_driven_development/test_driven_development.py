# TDD - Test Driven Development
# Разработка приложений, управляемая тестами
# В начале пишем тесты


# Приветствовать
def greet(name, is_enemy):
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
