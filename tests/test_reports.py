from pathlib import Path
import tempfile

import pytest

from main import load_data
from reports import create_average_report, REPORTS


def test_create_average_report_basic():
    '''Тест базового расчёта среднего значения.'''
    data = [
        {'country': 'USA', 'gdp': '100'},
        {'country': 'USA', 'gdp': '200'},
        {'country': 'China', 'gdp': '150'},
    ]
    result = create_average_report('gdp')(data)
    assert result == [('USA', 150.0), ('China', 150.0)]


def test_create_average_report_sorting():
    '''Тест сортировки по убыванию.'''
    data = [
        {'country': 'Small', 'gdp': '50'},
        {'country': 'Large', 'gdp': '500'},
        {'country': 'Medium', 'gdp': '200'},
    ]
    result = create_average_report('gdp')(data)
    assert result == [('Large', 500.0), ('Medium', 200.0), ('Small', 50.0)]


def test_create_average_report_invalid_values():
    '''Тест пропуска некорректных значений.'''
    data = [
        {'country': 'USA', 'gdp': '100'},
        {'country': 'USA', 'gdp': 'invalid'},
        {'country': 'China', 'gdp': ''},
    ]
    result = create_average_report('gdp')(data)
    assert result == [('USA', 100.0)]


def test_create_average_report_empty_result():
    '''Тест обработки данных без валидных значений.'''
    data = [
        {'country': 'USA', 'gdp': 'invalid'},
        {'country': 'China', 'gdp': 'nan'},
    ]
    result = create_average_report('gdp')(data)
    assert result == []


def test_load_data_valid():
    '''Тест загрузки валидных данных.'''
    content = 'country,gdp\nUSA,100\nChina,200\n'

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.csv', delete=False, encoding='utf-8'
    ) as f:
        f.write(content)
        f_path = f.name

    try:
        data = load_data([f_path])
        assert len(data) == 2
        assert data[0]['country'] == 'USA'
        assert data[1]['country'] == 'China'
    finally:
        Path(f_path).unlink()


def test_load_data_missing_country_column():
    '''Тест ошибки при отсутствии колонки "country".'''
    content = 'gdp,inflation\n100,2.0\n'

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.csv', delete=False, encoding='utf-8'
    ) as f:
        f.write(content)
        f_path = f.name

    try:
        with pytest.raises(ValueError, match='country'):
            load_data([f_path])
    finally:
        Path(f_path).unlink()


def test_load_data_file_not_found():
    '''Тест ошибки при отсутствии файла.'''
    with pytest.raises(FileNotFoundError, match='не найден'):
        load_data(['non_existent_file.csv'])


def test_end_to_end_average_gdp():
    '''Интеграционный тест: полный цикл обработки данных.'''
    data1 = [
        {'country': 'USA', 'gdp': '100', 'year': '2021'},
        {'country': 'USA', 'gdp': '200', 'year': '2022'},
    ]
    data2 = [
        {'country': 'China', 'gdp': '150', 'year': '2021'},
        {'country': 'China', 'gdp': '250', 'year': '2022'},
    ]

    result = REPORTS['average-gdp'](data1 + data2)
    assert len(result) == 2
    assert result[0] == ('China', 200.0)
    assert result[1] == ('USA', 150.0)


def test_all_predefined_reports():
    '''Тест всех предопределённых отчётов на корректных данных.'''
    test_data = [
        {
            'country': 'TestLand',
            'gdp': '1000',
            'inflation': '3.5',
            'unemployment': '5.2',
            'population': '50',
            'year': '2023',
        }
    ]

    for report_name, report_fn in REPORTS.items():
        result = report_fn(test_data)
        assert len(result) == 1
        assert result[0][0] == 'TestLand'
        assert isinstance(result[0][1], float)
        assert report_fn.metric in report_name


def test_metric_attribute():
    '''Проверка атрибута метрики у функций отчётов.'''
    assert REPORTS['average-gdp'].metric == 'gdp'
    assert REPORTS['average-inflation'].metric == 'inflation'
    assert REPORTS['average-unemployment'].metric == 'unemployment'
    assert REPORTS['average-population'].metric == 'population'
