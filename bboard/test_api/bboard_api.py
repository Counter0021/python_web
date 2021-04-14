# Доска объявлений API
import requests


# Получаем все объявления
def get_all_advertisements():
    response = requests.get(url, headers={'Accept': 'application/json'})
    data = response.json()
    for i in range(len(data)):
        for key, value in data[i].items():
            print(f'{key} - {value}')
        print()


# Получить объявление
def get_advertisement(mode):
    if mode == '1':
        id_number = input('Enter the id of the selected ad: ')
        response = requests.get(url + id_number, headers={'Accept': 'application/json'})
        data = response.json()
        for key, value in data.items():
            print(f'{key} - {value}')

    elif mode == '2':
        id_number = input('Enter the id of the selected ad: ')
        response = requests.get(url + id_number + '/comments', headers={'Accept': 'application/json'})
        data = response.json()
        for i in range(len(data)):
            print(f"{data[i]['author']} - {data[i]['content']}")

    else:
        print('Please enter a valid request.')
        input_modes()


url = 'http://localhost:8000/api/bbs/'
print('''
If you want to receive a specific ad, enter 1.
If you would like to receive comments on a specific ad, enter 2.
''')


# Ввод режима
def input_modes():
    mode = str(input())
    get_all_advertisements()
    get_advertisement(mode)


input_modes()
