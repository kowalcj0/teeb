# -*- coding: utf-8 -*-
import os

from pytest import fixture


@fixture
def single_file_multiple_tracks():
    cue_file = "ISO-8859_text_with_CRLF_line_terminators.cue"
    return os.path.join("tests", "files", cue_file)


@fixture
def multiple_files_single_track():
    cue_file = "ASCII_text.cue"
    return os.path.join("tests", "files", cue_file)


@fixture
def multiple_files_multiple_tracks():
    cue_file = "Non-ISO_extended-ASCII_text_with_CRLF.cue"
    return os.path.join("tests", "files", cue_file)
