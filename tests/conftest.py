import pytest
import sys
import os
import types

# Provide a minimal hmmlearn stub so importing src.stock_analysis does not fail
try:
    import hmmlearn  # type: ignore
except ImportError:  # pragma: no cover - environment may lack hmmlearn
    hmmlearn = types.ModuleType("hmmlearn")
    hmm_mod = types.ModuleType("hmm")

    class DummyGaussianHMM:
        def __init__(self, *args, **kwargs):
            pass

        def fit(self, *args, **kwargs):
            pass

        def score(self, *args, **kwargs):
            return 0.0

    hmm_mod.GaussianHMM = DummyGaussianHMM
    hmmlearn.hmm = hmm_mod
    sys.modules["hmmlearn"] = hmmlearn
    sys.modules["hmmlearn.hmm"] = hmm_mod


@pytest.fixture
def sample_stock_data():
    """Return a sample stock DataFrame suitable for testing."""
    pd = pytest.importorskip("pandas")
    dates = pd.date_range("2020-01-01", periods=30)
    data = {
        "Open": range(1, 31),
        "High": [x + 0.5 for x in range(1, 31)],
        "Low": [x - 0.5 for x in range(1, 31)],
        "Close": [x + 0.2 for x in range(1, 31)],
        "Volume": [1000 + x for x in range(30)],
        "Adj Close": [x + 0.2 for x in range(1, 31)],
    }
    return pd.DataFrame(data, index=dates)

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



@pytest.fixture
def patch_data_reader(monkeypatch, sample_stock_data):
    """Patch pandas_datareader to return local sample data."""
    pdr = pytest.importorskip("pandas_datareader")
    sub = sample_stock_data
    def fake_reader(*args, **kwargs):
        if str(args[2]) == "2020-13-01":
            raise ValueError("Invalid date")
        return sub
    monkeypatch.setattr(pdr.data, "DataReader", fake_reader)
