# -*- coding: utf-8 -*-
import os
import random
import string
from typing import List
from unittest import mock

import pytest

import teeb.default
import teeb.find

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
                [f"file.{extension}" for extension in teeb.default.ignored_extensions],
            ),
        ]
    ]


@pytest.fixture(
    params=[
        ABSOLUTE_ALBUM_PATH,
        DOTTED_RELATIVE_ALBUM_PATH,
        RELATIVE_ALBUM_PATH,
        CURRENT_DIRECTORY,
        CURRENT_SLASHED_DIRECTORY,
    ]
)
def album_with_extra_text_files(request) -> List[List[tuple]]:
    """A parametrized fixture that makes mocked os.walk() to return directory tree."""
    return [
        [
            (
                request.param,
                [],
                [filename for filename in teeb.default.redundant_text_files],
            ),
        ]
    ]


@pytest.fixture(
    params=[
        ABSOLUTE_ALBUM_PATH,
        DOTTED_RELATIVE_ALBUM_PATH,
        RELATIVE_ALBUM_PATH,
        CURRENT_DIRECTORY,
        CURRENT_SLASHED_DIRECTORY,
    ]
)
def album_with_mixed_case_file_extensions(request) -> List[List[tuple]]:
    """Return directory tree with files having upper case extensions"""
    return [
        [
            (
                request.param,
                [],
                [
                    f"file.{''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=3))}"
                    for _ in range(3)
                ],
            ),
        ]
    ]


@pytest.fixture(
    params=[
        ABSOLUTE_ALBUM_PATH,
        DOTTED_RELATIVE_ALBUM_PATH,
        RELATIVE_ALBUM_PATH,
        CURRENT_DIRECTORY,
        CURRENT_SLASHED_DIRECTORY,
    ]
)
def album_with_files_that_need_an_extension_change(request) -> List[List[tuple]]:
    """Return a directory tree with files that need their extension changed."""
    return [
        [
            (
                request.param,
                [],
                [
                    f"file.{extension}"
                    for extension in teeb.default.change_extension_mapping
                ],
            ),
        ]
    ]


@pytest.fixture(
    params=[
        f"{ABSOLUTE_ALBUM_PATH} with spaces in path/",
        f"{DOTTED_RELATIVE_ALBUM_PATH} with spaces in path ",
        f"{RELATIVE_ALBUM_PATH} with spaces in path /",
    ]
)
def album_with_directory_and_file_paths_containing_spaces(request) -> List[List[tuple]]:
    """Return a directory tree with directory and file paths containing spaces."""
    return [
        [
            (
                request.param,
                [],
                [
                    "file name with spaces in it.ext",
                    "another_file.name with spaces .ext",
                ],
            ),
        ]
    ]


def test_find_extra_files(album_with_ignored_files):
    """Test find_extra_files called for every type of album path"""
    for instance in album_with_ignored_files:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.extra_files(album_path)
            assert result is not None
            assert result == [
                os.path.join(album_path, f"file.{extension}")
                for extension in teeb.default.ignored_extensions
            ]


def test_find_extra_text_files(album_with_extra_text_files):
    """Test find_extra_text_files called for every type of album path"""
    for instance in album_with_extra_text_files:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.extra_text_files(album_path)
            assert result is not None
            assert result == [
                os.path.join(album_path, filename)
                for filename in teeb.default.redundant_text_files
            ]


def test_files_with_upper_case_extension(album_with_mixed_case_file_extensions):
    """Check if files with upper case extensions are found"""
    for instance in album_with_mixed_case_file_extensions:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.files_with_upper_case_extension(album_path)
            assert result is not None
            for file_path in result:
                assert any(c.isupper() for c in file_path[-3:])
                assert file_path.startswith(os.path.join(album_path, "file."))


def test_files_to_change_extension(album_with_files_that_need_an_extension_change):
    """Check if files that need their extension changed are being found"""
    for instance in album_with_files_that_need_an_extension_change:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.files_to_change_extension(album_path)
            assert result is not None
            assert result == [
                os.path.join(album_path, f"file.{old}")
                for old, _ in teeb.default.change_extension_mapping.items()
            ]


def test_directory_and_file_paths_with_spaces(
    album_with_directory_and_file_paths_containing_spaces,
):
    """Check if directory and file paths containing spaces are being found"""
    for instance in album_with_directory_and_file_paths_containing_spaces:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.directory_and_file_paths_with_spaces(album_path)
            assert result is not None
            for path in result:
                assert " " in path
