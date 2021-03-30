# -*- coding: utf-8 -*-
"""Unit tests for dir & file find functions.

UTF8 Visual Spoofing done with https://www.irongeek.com/homoglyph-attack-generator.php
"""
import os
import random
import string
from pathlib import PosixPath
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


def get_file_names(
    *,
    add_all: bool = False,
    audio: bool = True,
    art: bool = True,
    ignored: bool = False,
    text: bool = False,
    change_extension: bool = False,
    art_to_convert: bool = False,
) -> List[str]:
    if add_all:
        audio = art = ignored = text = change_extension = art_to_convert = True

    file_names = []
    if audio:
        audio_extension = random.choice(teeb.default.audio_extentions)
        audio_files = [f"{idx+1:02}-track_title.{audio_extension}" for idx in range(3)]
        file_names.extend(audio_files)
    if art:
        art_files = ["cover.jpg", "back.jpg", "cd.jpg", "inlay.jpg"]
        file_names.extend(art_files)
    if ignored:
        ignored = [f"file.{extension}" for extension in teeb.default.ignored_extensions]
        file_names.extend(ignored)
    if text:
        file_names.extend(teeb.default.redundant_text_files)
    if change_extension:
        files_with_extension_to_change = [
            f"file.{extension}" for extension in teeb.default.change_extension_mapping
        ]
        file_names.extend(files_with_extension_to_change)
    if art_to_convert:
        files_to_convert = [
            f"file.{extension}"
            for extension in teeb.default.album_art_extentions_to_convert
        ]
        file_names.extend(files_to_convert)
    return file_names


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
                get_file_names(add_all=True),
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
                get_file_names(add_all=True),
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
    file_names = [f"file.{''.join(random.choices(letters, k=3))}" for _ in range(3)]
    file_names.append(f"file.{random.choice(teeb.default.audio_extentions).upper()}")
    tree = [[(request.param, [], file_names)]]
    return tree


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
            (request.param, [], get_file_names(add_all=True)),
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
                    "file_name_with_underscores.ext",
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
            (request.param, [], get_file_names(art_to_convert=True)),
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
                    "album.nfo",
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
def album_layout_preferred(request: SubRequest) -> DirectoryTree:
    """Return a directory tree with preferred album layout."""
    return [
        [
            (
                request.param,
                [],
                get_file_names(),
            )
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
def album_layout_preferred_no_album_art(request: SubRequest) -> DirectoryTree:
    """Return a directory tree with preferred album layout."""
    return [
        [
            (
                request.param,
                [],
                get_file_names(art=False),
            )
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
def album_layout_case_1(request: SubRequest) -> DirectoryTree:
    return [
        [
            (
                request.param,
                ["album_art"],
                ["02-track_02.flac", "03-track_03.flac", "01-track_01.flac"],
            ),
            (f"{request.param}/album_art", [], ["cover.jpg", "back.jpg"]),
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
def album_layout_case_1a(request: SubRequest) -> DirectoryTree:
    return [
        [
            (request.param, ["album_art"], ["box.jpg"]),
            (f"{request.param}/album_art", [], ["cover.jpg", "back.jpg"]),
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
def album_layout_case_2a(request: SubRequest) -> DirectoryTree:
    return [
        [
            (f"{request.param}", ["album_art", "cd1", "cd2"], []),
            (f"{request.param}/album_art", [], ["cover.jpg", "back.jpg"]),
            (f"{request.param}/cd1", [], ["01-track_1.flac", "02-track_2.flac"]),
            (f"{request.param}/cd2", [], ["01-track_1.flac", "02-track_2.flac"]),
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
def album_layout_case_2b(request: SubRequest) -> DirectoryTree:
    return [
        [
            (f"{request.param}", ["album_art", "cd1", "cd2"], []),
            (f"{request.param}/album_art", [], ["cover.jpg", "back.jpg"]),
            (
                f"{request.param}/cd1",
                [],
                ["cover.jpg", "01-track_1.flac", "02-track_2.flac"],
            ),
            (
                f"{request.param}/cd2",
                [],
                ["cover.jpg", "01-track_1.flac", "02-track_2.flac"],
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
def album_layout_case_2c(request: SubRequest) -> DirectoryTree:
    return [
        [
            (f"{request.param}", ["album_art", "cd1", "cd2"], ["box_cover.jpg"]),
            (f"{request.param}/album_art", [], ["cover.jpg", "box_back.jpg"]),
            (
                f"{request.param}/cd1",
                ["album_art"],
                ["cover.jpg", "01-track_1.flac", "03-track_3.flac", "02-track_2.flac"],
            ),
            (
                f"{request.param}/cd1/album_art",
                [],
                ["booklet.jpg", "cover.jpg", "back.jpg"],
            ),
            (
                f"{request.param}/cd2",
                ["album_art"],
                ["01-track_1.flac", "03-track_3.flac", "02-track_2.flac"],
            ),
            (
                f"{request.param}/cd2/album_art",
                [],
                ["booklet.jpg", "cover.jpg", "back.jpg"],
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
def album_layout_case_2d(request: SubRequest) -> DirectoryTree:
    return [
        [
            (f"{request.param}/", ["cd2", "album_art", "cd1"], ["box_cover.jpg"]),
            (f"{request.param}/album_art", [], ["cover.jpg", "box_back.jpg"]),
            (
                f"{request.param}/cd1",
                [],
                ["01-track_1.flac", "03-track_3.flac", "02-track_2.flac"],
            ),
            (
                f"{request.param}/cd2",
                [],
                ["01-track_1.flac", "03-track_3.flac", "02-track_2.flac"],
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
def album_layout_case_2e(request: SubRequest) -> DirectoryTree:
    return [
        [
            (f"{request.param}/", ["album_art"], ["box_cover.jpg"]),
            (f"{request.param}/album_art", [], ["cover.jpg", "box_back.jpg"]),
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
            assert any(
                PosixPath(file_path).suffix[1:].lower() in teeb.default.audio_extentions
                for file_path in result
            )
            for file_path in result:
                assert any(c.isupper() for c in PosixPath(file_path).suffix[1:])
                assert file_path.startswith(os.path.join(album_path, "file."))


def test_non_audio_files_with_upper_case_characters(
    album_with_mixed_case_file_extensions,
):
    """Check if non-audio files with upper case characters are found."""
    for instance in album_with_mixed_case_file_extensions:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.non_audio_files_with_upper_case_characters(album_path)
            assert result is not None
            for file_path in result:
                assert any(c.isupper() for c in PosixPath(file_path).suffix[1:])
                assert all(
                    ext.lower() not in teeb.default.audio_extentions
                    for ext in PosixPath(file_path).suffix[1:]
                )
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


def test_cue_files_and_audio_files_against_dir_without_cue_file(album_layout_preferred):
    """An album dir without a CUE file"""
    for instance in album_layout_preferred:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.cue_files_and_audio_files(album_path)
            assert not result


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


def test_empty_directories_against_regular_album_dir(album_layout_preferred):
    """No empty directories should be found"""
    for instance in album_layout_preferred:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            with mock.patch("os.listdir", return_value=[album_path]):
                result = teeb.find.empty_directories(album_path)
                assert not result


def test_nested_album_art_preferred_layout(album_layout_preferred):
    """No nested album art of any type should be reported for preferred album layout."""
    for instance in album_layout_preferred:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.nested_album_art(album_path)
            assert result == {"case1": [], "case2": []}


def test_nested_album_art_preferred_layout_no_art(album_layout_preferred_no_album_art):
    """No nested album art of any type should be reported for preferred album layout."""
    for instance in album_layout_preferred_no_album_art:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            result = teeb.find.nested_album_art(album_path)
            assert result == {"case1": [], "case2": []}


def test_nested_album_art_album_layout_case_1(album_layout_case_1):
    """Find nested album art of case 1."""
    for instance in album_layout_case_1:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            files_in_parent_directory = instance[0][2]
            with mock.patch("os.listdir", return_value=files_in_parent_directory):
                with mock.patch("os.path.isfile", return_value=True):
                    result = teeb.find.nested_album_art(album_path)
                    expected = {
                        "case1": [
                            {
                                "art_dir": f"{album_path}/album_art",
                                "art_files": ["cover.jpg", "back.jpg"],
                                "parent_dir": PosixPath(album_path),
                            }
                        ],
                        "case2": [],
                    }
                    assert result == expected


def test_nested_album_art_album_layout_case_1a(album_layout_case_1a):
    """Find a nested dedicated album art in a directory without audio files."""
    for instance in album_layout_case_1a:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            files_in_parent_directory = instance[0][2]
            with mock.patch("os.listdir", return_value=files_in_parent_directory):
                with mock.patch("os.path.isfile", return_value=True):
                    result = teeb.find.nested_album_art(album_path)
                    assert result == {"case1": [], "case2": []}


def test_nested_album_art_album_layout_case_2a(album_layout_case_2a):
    """Find nested album art of case 2a."""
    for instance in album_layout_case_2a:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            directories_in_album_directory = instance[0][1]
            with mock.patch("os.listdir", return_value=directories_in_album_directory):
                with mock.patch("os.path.isfile", return_value=False):
                    result = teeb.find.nested_album_art(album_path)
                    expected = {
                        "case1": [],
                        "case2": [
                            {
                                "art_dir": f"{album_path}/album_art",
                                "art_files": ["cover.jpg", "back.jpg"],
                                "parent_dir": PosixPath(album_path),
                            }
                        ],
                    }
                    assert result == expected


def test_nested_album_art_album_layout_case_2b(album_layout_case_2b):
    """Find nested album art of case 2b.
    Album art found in the disc directories is omitted as it's in the right place.
    """
    for instance in album_layout_case_2b:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            directories_in_album_directory = instance[0][1]
            with mock.patch("os.listdir", return_value=directories_in_album_directory):
                with mock.patch("os.path.isfile", return_value=False):
                    result = teeb.find.nested_album_art(album_path)
                    expected = {
                        "case1": [],
                        "case2": [
                            {
                                "art_dir": f"{album_path}/album_art",
                                "art_files": ["cover.jpg", "back.jpg"],
                                "parent_dir": PosixPath(album_path),
                            }
                        ],
                    }
                    assert result == expected


def test_nested_album_art_album_layout_case_2c(album_layout_case_2c):
    """Find nested album art of case 2c.
    In this case album art is found:
    * in a dedicated directory on the same level as disc directories
    * in a dedicated directory in every disc directory
    """
    for instance in album_layout_case_2c:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            expected = {
                "case1": [],
                "case2": [
                    {
                        "art_dir": f"{album_path}/album_art",
                        "art_files": ["cover.jpg", "box_back.jpg"],
                        "parent_dir": PosixPath(album_path),
                    },
                    {
                        "art_dir": f"{album_path}/cd1/album_art",
                        "art_files": ["booklet.jpg", "cover.jpg", "back.jpg"],
                        "parent_dir": PosixPath(f"{album_path}/cd1"),
                    },
                    {
                        "art_dir": f"{album_path}/cd2/album_art",
                        "art_files": ["booklet.jpg", "cover.jpg", "back.jpg"],
                        "parent_dir": PosixPath(f"{album_path}/cd2"),
                    },
                ],
            }
            directories_in_album_directory = instance[0][1]
            with mock.patch("os.listdir", return_value=directories_in_album_directory):
                with mock.patch("os.path.isfile", return_value=False):
                    result = teeb.find.nested_album_art(album_path)
                    assert result == expected


def test_nested_album_art_no_audio_files_in_parent_directory(album_layout_case_2d):
    """Find dedicated album art directory at the root album directory."""
    for instance in album_layout_case_2d:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            expected = {
                "case1": [],
                "case2": [
                    {
                        "art_dir": f"{album_path}album_art",
                        "art_files": ["cover.jpg", "box_back.jpg"],
                        "parent_dir": PosixPath(album_path),
                    },
                ],
            }
            directories_in_album_directory = instance[0][1]
            with mock.patch("os.listdir", return_value=directories_in_album_directory):
                with mock.patch("os.path.isfile", return_value=False):
                    result = teeb.find.nested_album_art(album_path)
                    assert result == expected


def test_nested_album_art_no_audio_files(album_layout_case_2e):
    """Find dedicated album art directory at the root album directory."""
    for instance in album_layout_case_2e:
        with mock.patch("os.walk", return_value=instance):
            album_path = instance[0][0]
            directories_in_album_directory = instance[0][1]
            with mock.patch("os.listdir", return_value=directories_in_album_directory):
                with mock.patch("os.path.isfile", return_value=False):
                    result = teeb.find.nested_album_art(album_path)
                    assert result == {"case1": [], "case2": []}
