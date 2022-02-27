from sys import stdout

from bench.mongo.src.crud import READ_SCENARIOS, WRITE_SCENARIOS

if __name__ == '__main__':
    stdout.write('запускаю тесты Монги на чтение...\n')

    for scenario in READ_SCENARIOS:
        func = scenario.get('func')
        kwargs = scenario.get('kwargs')
        func(**kwargs)

    stdout.write('готово!\n')

    stdout.write('запускаю тесты Монги на запись...\n')

    for scenario in WRITE_SCENARIOS:
        func = scenario.get('func')
        kwargs = scenario.get('kwargs')
        func(**kwargs)

    stdout.write('готово!\n')
