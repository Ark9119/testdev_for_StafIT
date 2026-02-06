# Тестовое задание для компании StafIT
## Анализ макроэкономических данных
Выполненил: Кузнецов Иван
Телеграм: https://t.me/Ark9119
Email: Ark9119@yandex.ru
GitHub: https://github.com/Ark9119


## Задание:
[![TASK](https://img.shields.io/badge/task-View-blue)](task)


## О проекте:
Скрипт читает файлы с экономическими данными по странам и формирует отчеты по заданным параметрам.

## Запуск:
Название файлов (может быть несколько) и название отчета передается в виде параметров:
"--files"
"--report"
Доступные отчёты: average-gdp, average-inflation, average-unemployment, average-population

### Примеры:
"""bash
python main.py --files economic1.csv economic2.csv --report average-gdp
"""
"""bash
python main.py --files economic1.csv economic2.csv --report average-inflation
"""

### Пример вывода:
+-----+---------------+----------+
|   # | country       |      gdp |
|-----+---------------+----------|
|   1 | United States | 23923.7  |
|   2 | China         | 17810.3  |
|   3 | Germany       |  4138.33 |
|   4 | Spain         |  1409.33 |
|   5 | Mexico        |  1392.67 |
|   6 | Indonesia     |  1274.33 |
|   7 | Saudi Arabia  |  1016.33 |
|   8 | Netherlands   |  1006    |
|   9 | Turkey        |   927.33 |
|  10 | Switzerland   |   845    |
+-----+---------------+----------+

### Примеры запуска:
[![Примеры запуска](https://img.shields.io/badge/Launch_examples-View-blue)](Примеры_запуска.jpg)

## Настройка скрипта:
Для добавления возможности выводить новые отчёты:
- в reports.py добавить в словарь новые данные 
"""python
REPORTS = {
    'average-gdp': create_average_report('gdp'),
    'average-inflation': create_average_report('inflation'),
    'average-unemployment': create_average_report('unemployment'),
    'average-population': create_average_report('population'),
    'average-population': create_average_report('<new_data>'),
}
"""
- запуск для вывода новых отчётов:
"""bash
python main.py --files economic1.csv economic2.csv --report average-<new_data>
"""

## Тестирование:
Код покрыт тестами на 87%.
### Запуск тестов:
"""bash
pytest
"""

### Запуск тестов с покрытием:
"""bash
pytest --cov=. --cov-report=term-missing
"""