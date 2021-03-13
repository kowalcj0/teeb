# -*- coding: utf-8 -*-
"""Unit tests for dir & file find functions.

UTF8 Visual Spoofing done with https://www.irongeek.com/homoglyph-attack-generator.php
"""
import os
import random
import string
from typing import (
    List,
    Tuple,
)
from unittest import mock

import pytest
from _pytest.fixtures import SubRequest

import teeb.default
import teeb.find

# Type for directory tree structure returned by os.walk()
DirectoryTree = List[List[Tuple[str, List, List[str]]]]

ABSOLUTE_ALBUM_PATH = "/absolute/path/to/album"
DOTTED_RELATIVE_ALBUM_PATH = "./album"
RELATIVE_ALBUM_PATH = "album"
CURRENT_DIRECTORY = "."
CURRENT_SLASHED_DIRECTORY = "./"
ALBUM_PATH_WITH_UTF8_CHARS = "/ｕｔｆ８/рɑｔｈ tо/ＡＬᏴ⋃ⅿ"


@pytest.fixture(
    params=[
        ABSOLUTE_ALBUM_PATH,
        DOTTED_RELATIVE_ALBUM_PATH,
        RELATIVE_ALBUM_PATH,
        CURRENT_DIRECTORY,
        CURRENT_SLASHED_DIRECTORY,
        ALBUM_PATH_WITH_UTF8_CHARS,
    ]
)
def album_with_ignored_files(request: SubRequest) -> DirectoryTree:
    """A parametrized fixture that makes mocked os.walk() to return directory tree.

    A directory tree is represented as a list of tuples.
    Returned value has to be a nested list, because it's expected from mocked os.walk()
    to return a list of tuples.

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
        ALBUM_PATH_WITH_UTF8_CHARS,
    ]
)
def album_with_extra_text_files(request: SubRequest) -> DirectoryTree:
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
        ALBUM_PATH_WITH_UTF8_CHARS,
    ]
)
def album_with_mixed_case_file_extensions(request: SubRequest) -> DirectoryTree:
    """Return directory tree with files having upper case extensions"""
    letters = string.ascii_uppercase + string.ascii_lowercase
    return [
        [
            (
                request.param,
                [],
                [f"file.{''.join(random.choices(letters, k=3))}" for _ in range(3)],
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
        ALBUM_PATH_WITH_UTF8_CHARS,
    ]
)
def album_with_files_that_need_an_extension_change(
    request: SubRequest,
) -> DirectoryTree:
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
        ALBUM_PATH_WITH_UTF8_CHARS,
    ]
)
def album_with_directory_and_file_paths_containing_spaces(
    request: SubRequest,
) -> DirectoryTree:
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


@pytest.fixture(
    params=[
        ABSOLUTE_ALBUM_PATH,
        DOTTED_RELATIVE_ALBUM_PATH,
        RELATIVE_ALBUM_PATH,
        CURRENT_DIRECTORY,
        CURRENT_SLASHED_DIRECTORY,
        ALBUM_PATH_WITH_UTF8_CHARS,
    ]
)
def album_with_art_files_that_need_conversion(request: SubRequest) -> DirectoryTree:
    """Return a directory tree with album art files that need to be converted from e.g.
    bmp to jpg."""
    return [
        [
            (
                request.param,
                [],
                [
                    f"file.{extension}"
                    for extension in teeb.default.album_art_extentions_to_convert
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
        ALBUM_PATH_WITH_UTF8_CHARS,
    ]
)
def album_with_art_files_that_dont_need_filename_change(
    request: SubRequest,
) -> DirectoryTree:
    """Return a directory tree with album art files that need a file name change."""
    return [
        [
            (
                request.param,
                [],
                [
                    "back.jpg",
                    "cd.jpg",
                    "cd1.jpg",
                    "cd2.jpg",
                    "cd3.jpg",
                    "cd4.jpg",
                    "cd5.jpg",
                    "cd6.jpg",
                    "cd7.jpg",
                    "cd8.jpg",
                    "cd9.jpg",
                    "cd_1.jpg",
                    "cd_2.jpg",
                    "cd_3.jpg",
                    "cd_4.jpg",
                    "cd_5.jpg",
                    "cd_6.jpg",
                    "cd_7.jpg",
                    "cd_8.jpg",
                    "cd_9.jpg",
                    "cover.jpg",
                    "cover_out.jpg",
                    "disc.jpg",
                    "inlay.jpg",
                    "inside.jpg",
                    "matrix.jpg",
                    "obi.jpg",
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
        ALBUM_PATH_WITH_UTF8_CHARS,
    ]
)
def album_with_art_files_that_need_filename_change(
    request: SubRequest,
) -> DirectoryTree:
    """Return a directory tree with album art files that need a file name change."""
    return [
        [
            (
                request.param,
                [],
                [
                    "whatever-inlay_filename.jpg",
                    "album-inlay.jpg",
                    "booklet-inlay.jpg",
                    "album-przod.jpg",
                    "przod.jpg",
                    "album_folder.jpg",
                    "folder.jpg",
                    "some.album.front.jpg",
                    "front.jpg",
                    "srodek.jpg",
                    "tyl.jpg",
                    "some-inlay.jpg",
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
        ALBUM_PATH_WITH_UTF8_CHARS,
    ]
)
def directory_with_one_cue_and_one_audio_file(request: SubRequest) -> DirectoryTree:
    """Return a directory tree with one CUE file and one audio file."""
    return [
        [
            (
                request.param,
                [],
                [
                    "file.cue",
                    f"file.{random.choice(teeb.default.audio_extentions)}",
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
        ALBUM_PATH_WITH_UTF8_CHARS,
    ]
)
def directory_with_one_cue_and_multiple_audio_file(
    request: SubRequest,
) -> DirectoryTree:
    """Return a directory tree with one CUE file and multiple audio files."""
    audio_extension = random.choice(teeb.default.audio_extentions)
    return [
        [
            (
                request.param,
                [],
                ["file.cue"]
                + [
                    f"file_{idx}.{audio_extension}"
                    for idx in range(1, random.randint(3, 10))
                ],
            ),
        ]
    ]


@pytest.fixture(
    params=[
        ABSOLUTE_ALBUM_PATH,
        DOTTED_RELATIVE_ALBUM_PATH,
        RELATIVE_ALBUM_PATH,
        ALBUM_PATH_WITH_UTF8_CHARS,
    ]
)
def empty_directory(request: SubRequest) -> DirectoryTree:
    """Return a directory tree with no files."""
    return [
        [
            (request.param, [], []),
        ]
    ]


@pytest.fixture(
    params=[
        CURRENT_DIRECTORY,
        CURRENT_SLASHED_DIRECTORY,
    ]
)
def empty_current_directory(request: SubRequest) -> DirectoryTree:
    """Return a directory tree with no files."""
    return [
        [
            (request.param, [], []),
        ]
    ]


@pytest.fixture(
    params=[
        ABSOLUTE_ALBUM_PATH,
        DOTTED_RELATIVE_ALBUM_PATH,
        RELATIVE_ALBUM_PATH,
        ALBUM_PATH_WITH_UTF8_CHARS,
    ]
)
def empty_directories(request: SubRequest) -> DirectoryTree:
    """Return a directory tree with multiple empty directories."""
    return [
        [
            (request.param, ["empty_2", "empty_1", "empty_3"], []),
            (f"{request.param}/empty_2", [], []),
            (f"{request.param}/empty_1", [], []),
            (f"{request.param}/empty_3", [], []),
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


def test_album_art_files_to_convert(album_with_art_files_that_need_conversion):
    """Check if album art files that need conversion to e.g. jpg are being found"""
    for instance in album_with_art_files_that_need_conversion:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.album_art_files_to_convert(album_path)
            assert result is not None
            assert result == [
                os.path.join(album_path, f"file.{extension}")
                for extension in teeb.default.album_art_extentions_to_convert
            ]


def test_album_art_jpg_files_that_dont_need_file_name_change(
    album_with_art_files_that_dont_need_filename_change,
):
    """An album art file with correct name shouldn't need a file name change."""
    for instance in album_with_art_files_that_dont_need_filename_change:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.album_art_jpg_files(album_path)
            assert result == []


def test_album_art_jpg_files_that_get_single_file_name_change_suggestion(
    album_with_art_files_that_need_filename_change,
):
    """An album art file with invalid name should need a file name change."""
    for instance in album_with_art_files_that_need_filename_change:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.album_art_jpg_files(album_path)
            assert result
            # Every item on the result list should be a tuple consisting of:
            # a filename & a list with a single suggestion
            for item in result:
                assert len(item[1]) == 1


def test_cue_files_and_audio_files_one_cue_and_one_audio_files(
    directory_with_one_cue_and_one_audio_file,
):
    """An album dir with one CUE file and one audio file"""
    for instance in directory_with_one_cue_and_one_audio_file:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.cue_files_and_audio_files(album_path)
            assert result
            for item in result:
                assert item.dir == album_path
                assert item.cues == ["file.cue"]
                assert len(item.audio_files) == 1
                assert item.audio_files[0].startswith("file.")


def test_cue_files_and_audio_files_one_cue_and_multiple_audio_files(
    directory_with_one_cue_and_multiple_audio_file,
):
    """An album dir with one CUE file and multiple audio files"""
    for instance in directory_with_one_cue_and_multiple_audio_file:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.cue_files_and_audio_files(album_path)
            assert result
            for item in result:
                assert item.dir == album_path
                assert item.cues == ["file.cue"]
                assert len(item.audio_files) > 1
                assert all(
                    audio_file.startswith("file_") for audio_file in item.audio_files
                )


def test_empty_directories_non_current(empty_directory):
    """Find empty directory.

    See https://docs.python.org/3/library/os.html#os.listdir
    """
    for instance in empty_directory:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            with mock.patch("os.listdir", return_value=[album_path]):
                result = teeb.find.empty_directories(album_path)
                assert result


def test_empty_directories_current_dir(empty_current_directory):
    """Ensure that the current or parent directories aren't listed.

    os.listdir does not include the special entries
    '.' and '..' even if they are present in the directory.
    See https://docs.python.org/3/library/os.html#os.listdir
    """
    for instance in empty_current_directory:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            with mock.patch("os.listdir", return_value=[album_path]):
                result = teeb.find.empty_directories(album_path)
                assert result == []


def test_empty_directories_multiple(empty_directories):
    """Find empty directories.

    See https://docs.python.org/3/library/os.html#os.listdir
    """
    for instance in empty_directories:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            with mock.patch("os.listdir", return_value=[album_path]):
                result = teeb.find.empty_directories(album_path)
                assert result
