import requests

alphabet = '0123456789' + 'abcdefghijklmnopqrstuvwxyz'

# 1000
#
# 3E8
#
# 1000 = 62 * 16 + 8
# 62 = 3 * 16 + 14
# 3 = 0 * 16 + 3

counter = 0
length = 0

len_alphabet = len(alphabet)
login = 'cat'

while True:
    result = ''
    n = counter
    while len(result) < length:
        integer = n // len_alphabet
        rest = n % len_alphabet
        result = alphabet[rest] + result
        n = integer

    response = requests.post('http://127.0.0.1:5000/auth', json={'login': login, 'password': result})
    if response.status_code == 200:
        print(f'Good {login}: {result}')
        break

    if alphabet[-1] * length == result:
        length += 1
        counter = 0
    else:
        counter += 1
