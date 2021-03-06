# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import List

import teeb.default
import teeb.suggest


def extra_files(directory: str) -> List[str]:
    """Find extra files, like .accurip .m3u"""
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            extension = Path(filename).suffix[1:]
            if extension.lower() in teeb.default.ignored_extensions:
                filepath = os.path.join(sub_dir, filename)
                result.append(filepath)
    return result


def extra_text_files(directory):
    """Find extra text files, like: dr_analysis.txt foo_dr.txt"""
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            if filename.lower() in teeb.default.redundant_text_files:
                filepath = os.path.join(sub_dir, filename)
                result.append(filepath)
    return result


def files_with_upper_case_extension(directory):
    """Find files with mixed or uppercase extension, e.g. .Flac .APE .Jpeg .NFO"""
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            extension = Path(filename).suffix[1:]
            if extension.lower() != extension:
                filepath = os.path.join(sub_dir, filename)
                result.append(filepath)
    return result


def non_audio_files_with_upper_case_characters(directory):
    """Find non-audio files with mixed or upper case extension, e.g. .Jpeg"""
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            extension = Path(filename).suffix[1:]
            not_an_audio_file = extension.lower() not in teeb.default.audio_extentions
            same_as_to_lower = filename.lower() != filename
            if not_an_audio_file and same_as_to_lower:
                filepath = os.path.join(sub_dir, filename)
                result.append(filepath)
    return result


def files_to_change_extension(directory):
    """Find files which need their extension changed, e.g. from jpeg to jpg"""
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            extension = Path(filename).suffix[1:]
            if extension.lower() in teeb.default.change_extension_mapping.keys():
                filepath = os.path.join(sub_dir, filename)
                result.append(filepath)
    return result


def directory_and_file_paths_with_spaces(directory):
    """Find directory and file paths containing spaces."""
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(sub_dir, filename)
            if " " in filepath:
                result.append(filepath)
    return result


def album_art_files_to_convert(directory):
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            extension = Path(filename).suffix[1:]
            if extension.lower() in teeb.default.album_art_extentions_to_convert:
                filepath = os.path.join(sub_dir, filename)
                result.append(filepath)
    return result


def album_art_jpg_files(directory):
    result = []
    for sub_dir, _, files in os.walk(directory):
        for file in files:
            extension = Path(file).suffix[1:]
            filename = Path(file).name
            if extension == "jpg":
                suggestions = teeb.suggest.new_art_file_name(filename)
                if suggestions:
                    result.append((file, suggestions))
    return result


def nested_album_art(directory):
    """
    Typical cases:

    #0 - desired layout: album art in the same directory as audio files
    album:
        -album art files: cover.jpg etc

    #1 - album art in dedicated sub-directory
    album:
        -album_art_dir\
                    -album art files: cover.jpg etc

    #2 - album art in a directory on the same level as directories with audio files
    album:
        -album_art_dir\
                    -album art files: cover.jpg etc
        -cd_1\audio files
        -cd_2\audio files

    #2a - multiple album art directories and art files
    album:
        -album_art_dir\
                    -album art files: cover.jpg etc
        -cd_1\audio files
                        -album_art_dir\
                                    -album art files: cover.jpg etc
        -cd_2\audio files
                        -album_art_dir\
                                    -album art files: cover.jpg etc
        -some album art files: box_cover.jpg etc
    """

    def case2(path, parent, f) -> bool:
        is_file = os.path.isfile(os.path.join(parent, f))
        return not is_file and f != path.name

    result = {
        "case1": [],
        "case2": [],
    }
    for sub_dir, _, files in os.walk(directory):
        art_files = [f for f in files if Path(f).suffix[1:] == "jpg"]
        if art_files:
            audio_files = list(
                filter(
                    lambda f: Path(f).suffix[1:] in teeb.default.audio_extentions, files
                )
            )
            if not audio_files:
                path = Path(sub_dir)
                # print(f"\n\nFound art folder without audio files: {sub_dir}")
                parent = path.parent
                parent_files = [
                    f
                    for f in os.listdir(parent)
                    if os.path.isfile(os.path.join(parent, f))
                ]
                if parent_files:
                    parent_audio_files = list(
                        filter(
                            lambda f: Path(f).suffix[1:]
                            in teeb.default.audio_extentions,
                            parent_files,
                        )
                    )
                    if parent_audio_files:
                        print(
                            f"CASE #1: There are audio files in album art "
                            f"parent directory: {parent}\n"
                        )
                        item = {
                            "art_dir": sub_dir,
                            "art_files": art_files,
                            "parent_dir": parent,
                        }
                        result["case1"].append(item)
                    else:
                        parent_directories = [
                            f for f in os.listdir(parent) if case2(path, parent, f)
                        ]
                        if parent_directories:
                            # print(
                            #     f"CASE #2: There are ONLY directories in album art "
                            #     f"parent directory: {parent} -> {parent_directories}"
                            #     "\n"
                            # )
                            item = {
                                "art_dir": sub_dir,
                                "art_files": art_files,
                                "parent_dir": parent,
                            }
                            result["case2"].append(item)
                else:
                    parent_directories = [
                        f for f in os.listdir(parent) if case2(path, parent, f)
                    ]
                    if parent_directories:
                        # print(
                        #     f"CASE #2: There are ONLY directories in album art "
                        #     f"parent directory: {parent} -> {parent_directories}\n"
                        # )
                        item = {
                            "art_dir": sub_dir,
                            "art_files": art_files,
                            "parent_dir": parent,
                        }
                        result["case2"].append(item)

    return result


def cue_files_and_audio_files(directory):
    result = []
    for sub_dir, _, files in os.walk(directory):
        cues = [f for f in files if Path(f).suffix[1:] == "cue"]
        if cues:
            audio_files = list(
                filter(
                    lambda f: Path(f).suffix[1:] in teeb.default.audio_extentions, files
                )
            )
            cue_dir = {
                "dir": sub_dir,
                "cues": cues,
                "audio_files": audio_files,
            }
            result.append(cue_dir)

    return result


def empty_directories(directory):
    result = []
    for sub_dir, _, files in os.walk(directory):
        if not files:
            child_directories = [
                f
                for f in os.listdir(sub_dir)
                if os.path.isdir(os.path.join(sub_dir, f))
            ]
            if not child_directories:
                result.append(sub_dir)
    return sorted(result)