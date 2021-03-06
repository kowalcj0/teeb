# -*- coding: utf-8 -*-
"""Config file for PyTest"""
import os

from pytest import fixture


@fixture
def single_file_multiple_tracks():
    """Return a path to a cue file with multiple tracks defined in it."""
    cue_file = "ISO-8859_text_with_CRLF_line_terminators.cue"
    return os.path.join("tests", "files", cue_file)


@fixture
def multiple_files_single_track():
    """Returns a path to a CUE file with single track per multiple source files."""
    cue_file = "ASCII_text.cue"
    return os.path.join("tests", "files", cue_file)


@fixture
def multiple_files_multiple_tracks():
    """Returns a path to a CUE file with multiple tracks per source file."""
    cue_file = "Non-ISO_extended-ASCII_text_with_CRLF.cue"
    return os.path.join("tests", "files", cue_file)
