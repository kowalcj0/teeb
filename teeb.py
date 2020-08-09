#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

from teeb.teeb import (
    change_extensions,
    clean_up_jpg_album_art_file_names,
    convert_album_art_to_jpg,
    delete_extra_files,
    delete_extra_text_files,
    lower_extentions,
    non_audio_files_to_lower_case,
    replace_spaces_with_underscores,
    what_to_do_with_cue,
)


def main(directory):
    delete_extra_files(directory)
    delete_extra_text_files(directory)
    lower_extentions(directory)
    change_extensions(directory)
    non_audio_files_to_lower_case(directory)
    replace_spaces_with_underscores(directory)
    convert_album_art_to_jpg(directory)
    what_to_do_with_cue(directory)
    clean_up_jpg_album_art_file_names(directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="dir to organise")
    args = parser.parse_args()
    directory = args.dir
    main(directory)
