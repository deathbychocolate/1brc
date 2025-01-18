"""The only test file we will ever need."""

from typing import Generator

import pytest


class TestMain:

    @pytest.fixture(scope=session)
    def setup_teardown(self) -> Generator:
        yield ""

    def test_should_run(self, setup_teardown) -> None:
        assert False
