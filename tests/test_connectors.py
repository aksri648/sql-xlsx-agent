import pytest
from backend.connectors.sqlite_connector import SQLiteConnector


@pytest.fixture
def sqlite_connector(tmp_path):
    db_path = tmp_path / "test.db"
    return SQLiteConnector(str(db_path))


def test_sqlite_connection(sqlite_connector):
    assert sqlite_connector.test_connection() is True


def test_sqlite_disconnect(sqlite_connector):
    sqlite_connector.connect()
    sqlite_connector.disconnect()
    assert sqlite_connector.engine is None