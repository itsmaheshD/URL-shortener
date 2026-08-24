import os
from uuid import uuid4

import pytest
from sqlmodel import Session, create_engine

from url_designer.infrastructure.database.models.url_record import UrlRecord
from url_designer.infrastructure.database.repositories.url_repository import URLRepository


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

pytestmark = pytest.mark.skipif(
    not TEST_DATABASE_URL,
    reason="TEST_DATABASE_URL must be configured for database integration tests.",
)


def test_create_persists_url_record() -> None:
    engine = create_engine(TEST_DATABASE_URL)
    short_code_url = f"test{uuid4().hex[:12]}"

    with Session(engine) as session:
        repository = URLRepository(session)
        persisted_record = repository.create(
            UrlRecord(
                original_url="https://example.com/integration-test",
                short_code_url=short_code_url,
            )
        )

    assert persisted_record.id is not None
    assert persisted_record.original_url == "https://example.com/integration-test"
    assert persisted_record.short_code_url == short_code_url
