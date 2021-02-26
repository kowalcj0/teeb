# -*- coding: utf-8 -*-
import os

import pytest
from teeb.cueparser import CueParser


def test_single_file_multiple_tracks(single_file_multiple_tracks):
    cue = CueParser(single_file_multiple_tracks)
    assert len(cue.tracks) == 19
    assert cue.meta["FILE"]  # assert 1 global FILE
    for track in cue.tracks:
        assert "FILE" not in track


def test_multiple_files_single_track(multiple_files_single_track):
    cue = CueParser(multiple_files_single_track)
    assert len(cue.tracks) == 2
    assert "FILE" not in cue.meta  # assert no global FILE
    for track in cue.tracks:
        assert track["FILE"]


def test_multiple_files_multiple_tracks(multiple_files_multiple_tracks):
    cue = CueParser(multiple_files_multiple_tracks)
    assert len(cue.tracks) == 10
    assert "FILE" not in cue.meta  # assert no global FILE
    for track in cue.tracks:
        assert track["FILE"]
    # assert same FILE for track 1 & 2
    assert cue.tracks[0]["FILE"] == cue.tracks[1]["FILE"]
    # assert different FILE for remaining tracks
    assert cue.tracks[0]["FILE"] != cue.tracks[2]["FILE"]
    # assert there are 8 distinct FILE entries for tracks 3-10
    assert len(set(track["FILE"] for track in cue.tracks[2:])) == 8


@pytest.mark.parametrize(
    "filename, encoding",
    [
        ("ASCII_text.cue", "ascii"),
        ("ASCII_text_with_CRLF_line_terminators.cue", "ascii"),
        ("ISO-8859_text_with_CRLF_line_terminators.cue", "ISO-8859-1"),
        ("Little-endian_UTF-16_Unicode_text_with_CRLF_line_terminators.cue", "UTF-16"),
        ("Non-ISO_extended-ASCII_text_with_CRLF.cue", "Windows-1252"),
        ("UTF-8_Unicode_text.cue", "utf-8"),
        ("UTF-8_Unicode_text_with_CRLF_line_terminators.cue", "utf-8"),
        ("UTF-8_Unicode_with_BOM_text_with_CRLF_line_terminators.cue", "UTF-8-SIG"),
    ],
)
def test_text_encoding_autodetection(filename, encoding):
    path = os.path.join("tests", "files", filename)
    cue = CueParser(path)
    assert cue.encoding == encoding


@pytest.mark.parametrize(
    "filename, number_of_tracks",
    [
        ("ASCII_text.cue", 2),
        ("ASCII_text_with_CRLF_line_terminators.cue", 4),
        ("ISO-8859_text_with_CRLF_line_terminators.cue", 19),
        ("Little-endian_UTF-16_Unicode_text_with_CRLF_line_terminators.cue", 4),
        ("Non-ISO_extended-ASCII_text_with_CRLF.cue", 10),
        ("UTF-8_Unicode_text.cue", 14),
        ("UTF-8_Unicode_text_with_CRLF_line_terminators.cue", 11),
        ("UTF-8_Unicode_with_BOM_text_with_CRLF_line_terminators.cue", 10),
    ],
)
def test_number_of_parsed_tracks(filename, number_of_tracks):
    path = os.path.join("tests", "files", filename)
    cue = CueParser(path)
    assert len(cue.tracks) == number_of_tracks
