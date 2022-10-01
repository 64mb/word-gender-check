
# -*- coding: utf-8 -*-
import requests
import json

GENDERS = [
    'мужской',
    'женский',
    'средний',
    'множественное',
]


def get_gender(text):
    gender = -1
    result = requests.post('http://sklonenie-slova.ru/service/getRodSlova', {'v': text}, headers={
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }).text

    result = json.loads(result)['result'].lower()
    if 'мужского' in result:
        gender = 0
    if 'женского' in result:
        gender = 1
    if 'среднего' in result:
        gender = 2
    if 'множественное' in result:
        gender = 3

    return gender


def main():
    result_file = open('result.txt', 'w', encoding='utf-8')

    input_file = open('input.csv', 'r', encoding='utf-8').read().split('\n')
    input_file = [seed.split(';') for seed in input_file]

    progress = 0
    for item in input_file:
        word = item[0]
        gender = int(item[1])

        check_gender = get_gender(word)
        if gender != check_gender:
            check_gender_str = 'не определен'
            if check_gender != -1:
                check_gender_str = GENDERS[check_gender]

            s_out = '[word]: ' + word + ' [current]: ' + \
                GENDERS[gender] + ' [check]: ' + check_gender_str + '\n'

            print('[word]: ' + word + ' [current]: ' +
                  GENDERS[gender] + ' [check]: ' + check_gender_str)
            result_file.write(s_out)

        progress += 1
        print('progress: ' + str(progress) + '/' + str(len(input_file)))

    result_file.close()


main()
