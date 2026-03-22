import pytest
from report_tool import get_median_coffee_report


@pytest.fixture
def sample_data():
    """Фикстура с базовыми данными для тестов."""
    return [
        {"student": "Иван Кузнецов", "coffee_spent": "600"},
        {"student": "Иван Кузнецов", "coffee_spent": "700"},
        {"student": "Динар Каримов", "coffee_spent": "710"},
        {"student": "Динар Каримов", "coffee_spent": "800"},
        {"student": "Анна Смирнова", "coffee_spent": "500"},
        {"student": "Иван Кузнецов", "coffee_spent": "650"},
        {"student": "Иван Кузнецов", "coffee_spent": "750"},
        {"student": "Динар Каримов", "coffee_spent": "400"},
    ]


def test_median_calculation_odd(sample_data):
    """Тест медианы для нечетного количества записей (Иван: 600, 650, 700)."""
    report, _ = get_median_coffee_report(sample_data)
    ivan_row = next(item for item in report if item[0] == "Иван Кузнецов")
    assert ivan_row[1] == 675.0


def test_median_calculation_even():
    """Тест медианы для четного количества записей (среднее между двумя центральными)."""
    data = [
        {"student": "Тест", "coffee_spent": "100"},
        {"student": "Тест", "coffee_spent": "200"},
    ]
    report, _ = get_median_coffee_report(data)
    assert report[0][1] == 150.0


def test_sorting_order(sample_data):
    """Проверка сортировки по убыванию трат."""
    report, _ = get_median_coffee_report(sample_data)
    assert report[0][0] == "Динар Каримов"
    assert report[1][0] == "Иван Кузнецов"


def test_invalid_data_handling():
    """Проверка, что скрипт игнорирует некорректные значения трат."""
    data = [
        {"student": "Иван", "coffee_spent": "not_a_number"},
        {"student": "Иван", "coffee_spent": "500"},
    ]
    report, _ = get_median_coffee_report(data)
    assert len(report) == 1
    assert report[0][1] == 500.0


def test_empty_data():
    """Проверка работы с пустым списком данных."""
    report, _ = get_median_coffee_report([])
    assert report == []
