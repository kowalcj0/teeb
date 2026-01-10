"""Unit tests for file name suggestion functions."""

from typing import (
    List,
    Optional,
)

import pytest

import teeb.suggest


@pytest.mark.parametrize(
    ["filename", "expected_suggestions"],
    [
        ("back.jpg", []),
        ("cd.jpg", []),
        ("cd1.jpg", []),
        ("cd2.jpg", []),
        ("cd3.jpg", []),
        ("cd4.jpg", []),
        ("cd5.jpg", []),
        ("cd6.jpg", []),
        ("cd7.jpg", []),
        ("cd8.jpg", []),
        ("cd9.jpg", []),
        ("cd_1.jpg", []),
        ("cd_2.jpg", []),
        ("cd_3.jpg", []),
        ("cd_4.jpg", []),
        ("cd_5.jpg", []),
        ("cd_6.jpg", []),
        ("cd_7.jpg", []),
        ("cd_8.jpg", []),
        ("cd_9.jpg", []),
        ("cover.jpg", []),
        ("cover_out.jpg", []),
        ("disc.jpg", []),
        ("inlay.jpg", []),
        ("inside.jpg", []),
        ("matrix.jpg", []),
        ("obi.jpg", []),
        ("whatever-inlay_filename.jpg", ["inlay.jpg"]),
        ("album-inlay.jpg", ["inlay.jpg"]),
        ("booklet-inlay.jpg", ["inlay.jpg"]),
        ("album-przod.jpg", ["cover.jpg"]),
        ("przod.jpg", ["cover.jpg"]),
        ("album_folder.jpg", ["cover.jpg"]),
        ("folder.jpg", ["cover.jpg"]),
        ("some.album.front.jpg", ["cover.jpg"]),
        ("front.jpg", ["cover.jpg"]),
        ("srodek.jpg", ["inside.jpg"]),
        ("tyl.jpg", ["back.jpg"]),
        ("back_inlay.jpg", ["back.jpg", "inlay.jpg"]),
    ],
)
def test_new_art_file_name(filename: str, expected_suggestions: Optional[List[str]]):
    suggestions = teeb.suggest.new_art_file_name(filename)
    assert suggestions == expected_suggestions
