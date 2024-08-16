from collections.abc import Generator
from unittest.mock import Mock

import pytest
from fastapi import Request

from app.common.fastapi.context import request_ctx


@pytest.fixture
def mock_request() -> Mock:
    return Mock(spec=Request)


@pytest.fixture(scope="function")
def mock_request_ctx(mock_request: Mock) -> Generator[None, None, None]:
    token = request_ctx.set(mock_request)
    yield
    request_ctx.reset(token)
