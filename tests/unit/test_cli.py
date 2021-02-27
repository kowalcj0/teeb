# -*- coding: utf-8 -*-
from typing import List
from unittest import mock

import pytest
import teeb.cli


@pytest.fixture(autouse=False)
def album_with_files_with_ignored_extensions() -> List[tuple]:
    """Mocked os.walk() that returns a list of tuples representing an album directory with ignored files
    Based on https://stackoverflow.com/a/24533453
    """
    return_value = [
        (
            "./album",
            [],
            [f"file.{extension}" for extension in teeb.cli.ignored_extensions],
        ),
    ]
    with mock.patch("os.walk", return_value=return_value) as mock_walk:
        yield mock_walk


def test_find_extra_files(album_with_files_with_ignored_extensions):
    result = teeb.cli.find_extra_files("./album")
    assert result == [
        f"./album/file.{extension}" for extension in teeb.cli.ignored_extensions
    ]
