import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool


@pytest.fixture
def engine(postgresql):
    """Create an SQLAlchemy engine with a disposable PostgreSQL database."""
    return create_engine('postgresql+psycopg://',
                         poolclass=StaticPool,
                         creator=lambda: postgresql)


@pytest.fixture
def session(engine, record_property):
    """Create an SQLAlchemy session with a disposable PostgreSQL database."""
    with Session(engine) as session:
        yield session
        record_property('database_size', get_database_size(session))


def get_database_size(session):
    (database_size,), = session.execute(text(
        '''SELECT pg_size_pretty(sum(pg_relation_size(C.oid)))
            FROM pg_class C
            LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
            WHERE nspname NOT IN ('pg_catalog', 'information_schema')'''))
    return database_size


def pytest_terminal_summary(terminalreporter):
    terminalreporter.section('database size')
    for report in terminalreporter.getreports(''):
        try:
            database_size = dict(report.user_properties)['database_size']
        except KeyError:
            pass
        else:
            terminalreporter.line(f'{report.nodeid}: {database_size}')
