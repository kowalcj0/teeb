# -*- coding: utf-8 -*-
import os
from typing import List
from unittest import mock

import pytest
import teeb.cli

ABSOLUTE_ALBUM_PATH = "/absolute/path/to/album"
DOTTED_RELATIVE_ALBUM_PATH = "./album"
RELATIVE_ALBUM_PATH = "album"
CURRENT_DIRECTORY = "."
CURRENT_SLASHED_DIRECTORY = "./"


@pytest.fixture(
    params=[
        ABSOLUTE_ALBUM_PATH,
        DOTTED_RELATIVE_ALBUM_PATH,
        RELATIVE_ALBUM_PATH,
        CURRENT_DIRECTORY,
        CURRENT_SLASHED_DIRECTORY,
    ]
)
def album_with_ignored_files(request) -> List[List[tuple]]:
    """A parametrized fixture that makes mocked os.walk() to return directory tree.

    A directory tree is represented as a list of tuples.
    Returned value has to be a nested list, because it's expected from mocked os.walk() to return a list of tuples.

    Based on:
    * https://stackoverflow.com/a/24533453
    * https://docs.pytest.org/en/stable/fixture.html#parametrizing-fixtures
    """
    return [
        [
            (
                request.param,
                [],
                [f"file.{extension}" for extension in teeb.cli.ignored_extensions],
            ),
        ]
    ]


def test_find_extra_files_absolute_path(album_with_ignored_files):
    """Test find_extra_files called with 3 different album paths"""
    for instance in album_with_ignored_files:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.cli.find_extra_files(album_path)
            assert result == [
                os.path.join(album_path, f"file.{extension}")
                for extension in teeb.cli.ignored_extensions
            ]