# -*- coding: utf-8 -*-
"""Unit tests for file name suggestion functions."""
from typing import (
    List,
    Optional,
)

import pytest

import teeb.suggest


@pytest.mark.parametrize(
    "filename,expected_suggestions",
    [
        ("back.jpg", None),
        ("cd.jpg", None),
        ("cd1.jpg", None),
        ("cd2.jpg", None),
        ("cd3.jpg", None),
        ("cd4.jpg", None),
        ("cd5.jpg", None),
        ("cd6.jpg", None),
        ("cd7.jpg", None),
        ("cd8.jpg", None),
        ("cd9.jpg", None),
        ("cd_1.jpg", None),
        ("cd_2.jpg", None),
        ("cd_3.jpg", None),
        ("cd_4.jpg", None),
        ("cd_5.jpg", None),
        ("cd_6.jpg", None),
        ("cd_7.jpg", None),
        ("cd_8.jpg", None),
        ("cd_9.jpg", None),
        ("cover.jpg", None),
        ("cover_out.jpg", None),
        ("disc.jpg", None),
        ("inlay.jpg", None),
        ("inside.jpg", None),
        ("matrix.jpg", None),
        ("obi.jpg", None),
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
