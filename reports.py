from collections import defaultdict
import math


def create_average_report(metric):
    '''Создание отчёта по показателям.'''
    def report(data):
        country_values = defaultdict(list)
        for row in data:
            try:
                value = float(row[metric])
                if not math.isnan(value):
                    country_values[row['country']].append(value)
            except (KeyError, ValueError, TypeError):
                continue
        return sorted(
            [
                (country, sum(values) / len(values))
                for country, values in country_values.items()
                if values
            ],
            key=lambda x: x[1],
            reverse=True,
        )
    report.metric = metric
    return report


REPORTS = {
    'average-gdp': create_average_report('gdp'),
    'average-inflation': create_average_report('inflation'),
    'average-unemployment': create_average_report('unemployment'),
    'average-population': create_average_report('population'),
}
