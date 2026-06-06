import pytest
import pandas as pd
from backend.services.file_handler import FileHandler


def test_get_schema():
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "salary": [50000, 60000, 70000],
    })

    schema = FileHandler.get_schema(df)

    assert schema["row_count"] == 3
    assert schema["column_count"] == 3
    assert len(schema["columns"]) == 3

    name_col = next(c for c in schema["columns"] if c["name"] == "name")
    assert name_col["dtype"] == "object"
    assert name_col["unique_count"] == 3


def test_profile_dataset():
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
    })

    profile = FileHandler.profile_dataset(df)

    assert "schema" in profile
    assert "dtypes" in profile
    assert "memory_usage" in profile
    assert isinstance(profile["memory_usage"], int)