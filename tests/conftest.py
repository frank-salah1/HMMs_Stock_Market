import pytest
import os
import pandas as pd

@pytest.fixture
def company_name():
    yield "AAPL"


def cleanup(file_type):
    files = os.listdir(os.getcwd())
    for file in files:
        if file[-(len(file_type)):] == file_type:
            os.remove(os.path.join(os.getcwd(), file))


@pytest.fixture
def valid_start_date():
    yield "2020-11-01"


@pytest.fixture
def invalid_start_date():
    yield "2020-13-01"


@pytest.fixture
def valid_end_date():
    yield "2020-12-05"


@pytest.fixture
def sample_stock_data():
    dates = pd.date_range("2020-11-01", periods=5, freq="D")
    data = {
        "High": [10, 11, 12, 13, 14],
        "Low": [5, 5, 6, 6, 7],
        "Open": [9, 10, 11, 12, 13],
        "Close": [9, 10, 11, 12, 13],
        "Volume": [100] * 5,
        "Adj Close": [9, 10, 11, 12, 13],
    }
    return pd.DataFrame(data, index=dates)


@pytest.fixture
def mock_datareader(monkeypatch, sample_stock_data):
    monkeypatch.setattr(
        "pandas_datareader.data.DataReader",
        lambda *args, **kwargs: sample_stock_data.copy(),
    )
    yield


@pytest.fixture
def input_args(company_name, valid_start_date, valid_end_date):
    yield [
            "../../stock_analysis",
            "-n",
            company_name,
            "-s",
            valid_start_date,
            "-e",
            valid_end_date,
        ]


@pytest.fixture
def cleanup_excel_files():
    yield 
    cleanup(".xlsx")


@pytest.fixture
def cleanup_images():
    yield
    cleanup(".png")