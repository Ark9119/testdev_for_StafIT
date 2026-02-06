import csv
import argparse
import sys

from tabulate import tabulate
from reports import REPORTS


def load_data(files):
    '''Загрузка и валидация данных из CSV-файлов.'''
    data = []
    for path in files:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if 'country' not in reader.fieldnames:
                    raise ValueError(f'Отсутствует колонка "country" в {path}')
                data.extend(reader)
        except FileNotFoundError:
            raise FileNotFoundError(f'Файл не найден: {path}')
    return data


def main():
    '''Точка входа скрипта обработки макроэкономических данных.'''
    parser = argparse.ArgumentParser(
        description='Генерация макроэкономических отчётов'
    )
    parser.add_argument('--files', nargs='+', required=True,
                        help='Пути к CSV-файлам с данными')
    parser.add_argument('--report', required=True,
                        help='Тип отчёта (например: average-gdp)')
    args = parser.parse_args()

    if args.report not in REPORTS:
        print(
            f'Error: Отчёт "{args.report}" не поддерживается.\n'
            f'Доступные отчёты: {", ".join(REPORTS.keys())}',
            file=sys.stderr
        )
        sys.exit(1)

    try:
        data = load_data(args.files)
        result = REPORTS[args.report](data)
    except (FileNotFoundError, ValueError) as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

    metric = REPORTS[args.report].metric
    table = [
        [i, country, f'{value:.2f}']
        for i, (country, value) in enumerate(result, 1)
    ]
    print(tabulate(table, headers=['#', 'country', metric], tablefmt='psql'))


if __name__ == '__main__':
    main()
