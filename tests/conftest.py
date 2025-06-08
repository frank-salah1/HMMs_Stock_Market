import pytest
import sys
import os


@pytest.fixture
def sample_stock_data():
    """Return a small sample DataFrame if pandas is available."""
    pd = pytest.importorskip("pandas")
    data = {
        "Open": [1, 2, 3],
        "High": [1.5, 2.5, 3.5],
        "Low": [0.5, 1.5, 2.5],
        "Close": [1.2, 2.2, 3.2],
    }
    return pd.DataFrame(data)

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