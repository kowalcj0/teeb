#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import sys
from pathlib import Path
from subprocess import Popen
from typing import List, Text

from send2trash import send2trash
from teeb.cueparser import CueParser
from teeb.prompt import prompt
from wand.image import Image

ignored_extensions = [
    "accurip",
    "exe",
    "inf",
    "log",
    "m3u",
    "m3u8",
    "md5",
    "rtf",
    "part",
    "pls",
    "sfv",
    "x32",
]
change_extension_mapping = {
    "jpeg": "jpg",
}
redundant_text_files = [
    "dr_analysis.txt",
    "eac_screen.png",
    "folder.aucdtect.txt",
    "gap_test.png",
    "torrent downloaded from demonoid.com.txt",
    "cduniverse.txt",
    "fingerprint.ffp.txt",
    "fingerprint.txt",
    "foo_dr.txt",
    "audiochecker.txt",
]
audio_extentions = [
    "ape",
    "flac",
    "m4a",
    "mp3",
    "ogg",
    "wav",
    "wma",
    "wv",
    "tak",
]

album_art_extentions_to_convert = [
    "bmp",
    "png",
    "tif",
    "tiff",
]
# TODO
lossless_extensions = [
    "ape",
    "m4a",
    "tak",
    "wav",
    "wv",
]


def find_extra_files(directory: Text) -> List[Text]:
    """Find extra files """
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            extension = Path(filename).suffix[1:]
            if extension.lower() in ignored_extensions:
                filepath = os.path.join(sub_dir, filename)
                result.append(filepath)
    return result


def delete_extra_files(directory):
    filepaths = find_extra_files(directory)
    if not filepaths:
        print(f"No extra files found in: {directory}")
    else:
        print(f"Found {len(filepaths)} extra files:")
        for path in filepaths:
            print(path)

        decision = prompt("Delete all extra files?", ["y", "n", "q"])
        if decision == "y":
            for path in filepaths:
                try:
                    os.remove(path)
                except OSError as err:
                    print(err)
            print("Deleted all extra files")
        elif decision == "q":
            print("Quit")
            sys.exit(0)
        else:
            print("Skipped deleting extra files")


def find_extra_text_files(directory):
    """Find extra files """
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            if filename.lower() in redundant_text_files:
                filepath = os.path.join(sub_dir, filename)
                result.append(filepath)
    return result


def delete_extra_text_files(directory):
    filepaths = find_extra_text_files(directory)
    if not filepaths:
        print(f"No extra text files found in: {directory}")
    else:
        print(f"Found {len(filepaths)} extra text files:")
        for path in filepaths:
            print(path)

        decision = prompt("Delete all extra text files?", ["y", "n", "q"])
        if decision == "y":
            for path in filepaths:
                try:
                    os.remove(path)
                except OSError as err:
                    print(err)
            print("Deleted all extra text files")
        elif decision == "q":
            print("Quit")
            sys.exit(0)
        else:
            print("Skipped deleting extra text files")


def find_files_with_upper_case_extention(directory):
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            extension = Path(filename).suffix[1:]
            if extension.lower() != extension:
                filepath = sub_dir + os.sep + filename
                result.append(filepath)
    return result


def lower_extentions(directory):
    filepaths = find_files_with_upper_case_extention(directory)
    if not filepaths:
        print(f"No files found with upper case extensions in: {directory}")
    else:
        print(f"Found {len(filepaths)} files with upper case extensions:")
        for path in filepaths:
            print(path)

        decision = prompt("Change all extensions to lower case?", ["y", "n", "q"])
        if decision == "y":
            for path in filepaths:
                extension = Path(path).suffix.lower()
                new_path = path[: len(path) - len(extension)] + extension.lower()
                try:
                    os.rename(path, new_path)
                except OSError as err:
                    print(err)
            print("Changed extensions to lower case")
        elif decision == "q":
            print("Quit")
            sys.exit(0)
        else:
            print("Skipped changing extensions to lower case")


def find_non_audio_files_with_upper_case_characters(directory):
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            extension = Path(filename).suffix[1:]
            not_an_audio_file = extension.lower() not in audio_extentions
            same_as_to_lower = filename.lower() != filename
            if not_an_audio_file and same_as_to_lower:
                filepath = sub_dir + os.sep + filename
                result.append(filepath)
    return result


def non_audio_files_to_lower_case(directory):
    filepaths = find_non_audio_files_with_upper_case_characters(directory)
    if not filepaths:
        print(f"No non-audio files found with upper case characters in: {directory}")
    else:
        print(f"Found {len(filepaths)} non-audio files with upper case charactres:")
        for path in filepaths:
            print(path)

        decision = prompt(
            "Change all non-audio file names to lower case?", ["y", "n", "q"]
        )
        if decision == "y":
            for path in filepaths:
                new_name = Path(path).name.lower()
                new_path = path[: len(path) - len(new_name)] + new_name
                try:
                    os.rename(path, new_path)
                except OSError as err:
                    print(err)
            print("Changed all non-audio file names to lower case")
        elif decision == "q":
            print("Quit")
            sys.exit(0)
        else:
            print("Skipped changing non-audio file names to lower case")


def find_files_to_change_extension(directory):
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            extension = Path(filename).suffix[1:]
            if extension.lower() in change_extension_mapping.keys():
                filepath = sub_dir + os.sep + filename
                result.append(filepath)
    return result


def change_extensions(directory):
    filepaths = find_files_to_change_extension(directory)
    if not filepaths:
        print(f"No files found to change extensions in: {directory}")
    else:
        print(
            f"Found {len(filepaths)} files to change extensions: "
            f"{change_extension_mapping}"
        )
        for path in filepaths:
            print(path)

        decision = prompt("Change all extensions?", ["y", "n", "q"])
        if decision == "y":
            for path in filepaths:
                extension = Path(path).suffix[1:].lower()
                new_extension = change_extension_mapping[extension.lower()]
                new_path = path[: len(path) - len(extension)] + new_extension
                try:
                    os.rename(path, new_path)
                except OSError as err:
                    print(err)
            print("Changed all extensions")
        elif decision == "q":
            print("Quit")
            sys.exit(0)
        else:
            print("Skipped changing extensions")


def find_directories_and_files_with_white_spaces(directory):
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            filepath = sub_dir + os.sep + filename
            if " " in filepath:
                result.append(filepath)
    return result


def replace_spaces_with_underscores(directory):
    filepaths = find_directories_and_files_with_white_spaces(directory)
    if not filepaths:
        print(f"No directories or files with white spaces found in: {directory}")
    else:
        print(f"Found {len(filepaths)} directories and files with white spaces")
        for path in filepaths:
            print(path)

        decision = prompt("Replace white spaces with underscores?", ["y", "n", "q"])
        if decision == "y":
            for path, folders, files in os.walk(directory):
                for filename in files:
                    os.rename(
                        os.path.join(path, filename),
                        os.path.join(path, filename.replace(" ", "_")),
                    )
                for idx in range(len(folders)):
                    new_name = folders[idx].replace(" ", "_")
                    try:
                        os.rename(
                            os.path.join(path, folders[idx]),
                            os.path.join(path, new_name),
                        )
                    except OSError as err:
                        print(err)
                    folders[idx] = new_name
            print("Replaced all white spaces with underscores")
        elif decision == "q":
            print("Quit")
            sys.exit(0)
        else:
            print("Skipped replacing white spaces with underscores")


def find_album_art_files_to_convert(directory):
    result = []
    for sub_dir, directories, files in os.walk(directory):
        for filename in files:
            extension = Path(filename).suffix[1:]
            if extension.lower() in album_art_extentions_to_convert:
                filepath = sub_dir + os.sep + filename
                result.append(filepath)
    return result


def convert_album_art_to_jpg(directory):
    filepaths = find_album_art_files_to_convert(directory)
    if not filepaths:
        print("Non album art files found to convert to jpg")
    else:
        print(f"Found {len(filepaths)} album art files to convert to jpg")
        for path in filepaths:
            print(path)

        decision = prompt("Convert all album art to jpg?", ["y", "n", "q"])
        if decision == "y":
            for path in filepaths:
                new_path = path[: len(path) - len(Path(path).suffix)] + ".jpg"
                with Image(filename=path) as image:
                    image.compression_quality = 90
                    image.save(filename=new_path)
                    try:
                        os.remove(path)
                    except OSError as err:
                        print(err)
            print("Converted all album art to jpg")
        elif decision == "q":
            print("Quit")
            sys.exit(0)
        else:
            print("Skipped converting all album art to jpg")


def find_album_art_jpg_files(directory):
    result = []
    for sub_dir, _, files in os.walk(directory):
        for file in files:
            extension = Path(file).suffix[1:]
            filename = Path(file).name
            if extension == "jpg":
                suggestions = suggest_new_filenames(filename)
                if suggestions:
                    result.append((file, suggestions))
    return result


def suggest_new_filenames(filename) -> str:
    clean_names = [
        "inlay.jpg",
        "cover.jpg",
        "cover_out.jpg",
        "inside.jpg",
        "back.jpg",
        "matrix.jpg",
        "obi.jpg",
        "disc.jpg",
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
    ]
    if filename in clean_names:
        return None

    suggestions = set()
    if "inlay" in filename:
        suggestions.add("inlay.jpg")
    if "przod" in filename:
        suggestions.add("cover.jpg")
    if "folder" in filename:
        suggestions.add("cover.jpg")
    if "front" in filename:
        suggestions.add("cover.jpg")
    if "cover" in filename:
        suggestions.add("cover.jpg")
    if "cover" in filename and "out" in filename:
        suggestions.add("cover_out.jpg")
    if "srodek" in filename:
        suggestions.add("inside.jpg")
    if "inside" in filename:
        suggestions.add("inside.jpg")
    if "tyl" in filename:
        suggestions.add("back.jpg")
    if "cd" in filename:
        suggestions.add("cd.jpg")
    if "disc" in filename:
        suggestions.add("disc.jpg")
    if "matrix" in filename:
        suggestions.add("matrix.jpg")
    if "obi" in filename:
        suggestions.add("obi.jpg")
    if "back" in filename:
        suggestions.add("back.jpg")

    return list(suggestions) if list(suggestions) != [filename] else None


def clean_up_jpg_album_art_file_names(directory):
    filepaths = find_album_art_jpg_files(directory)
    if not filepaths:
        print(f"No jpg album art files found to clean-up in: {directory}")
    else:
        print(
            f"Found {len(filepaths)} suggestions for changing jpg album art file names"
        )
        decision = prompt(
            "Proceed with album art file name change suggestions?", ["y", "n", "q"]
        )
        if decision == "y":
            for sub_dir, _, files in os.walk(directory):
                album_art_files = []
                for file in files:
                    extension = Path(file).suffix[1:]
                    filename = Path(file).name
                    if extension == "jpg":
                        suggestions = suggest_new_filenames(filename)
                        if suggestions:
                            album_art_files.append((file, suggestions))
                if album_art_files:
                    print(f"\n\nSuggestions for album art in: {sub_dir}")
                    for filename, suggestions in album_art_files:
                        if len(suggestions) == 1:
                            print(f"    {filename} -> {suggestions[0]}")
                        else:
                            txt_suggestions = "; ".join(
                                f"({idx+1}): {sug}"
                                for idx, sug in enumerate(suggestions)
                            )
                            print(f"    {filename} -> {txt_suggestions}")

                    decision = prompt(
                        "Apply suggested file name changes?", ["y", "n", "s", "q"]
                    )

                    if decision == "y":
                        for filename, suggestions in album_art_files:
                            if len(suggestions) > 1:
                                options = ["n", "s", "q"]
                                options.extend(
                                    [str(n) for n in range(1, len(suggestions) + 1)]
                                )
                                num = prompt(
                                    f"Choose suggestion for {filename}?", options
                                )
                                if num not in ["n", "q"]:
                                    num = int(num) - 1
                                    suggestion = suggestions[num]
                                elif num == "n":
                                    continue
                                elif num == "s":
                                    return
                                else:
                                    sys.exit(0)
                            else:
                                suggestion = suggestions[0]
                            old_path = os.path.join(sub_dir, filename)
                            new_path = os.path.join(sub_dir, suggestion)
                            if os.path.exists(new_path):
                                print(f"File already exists: {new_path}")
                            else:
                                try:
                                    os.rename(old_path, new_path)
                                except OSError as err:
                                    print(err)
                    elif decision == "q":
                        print("Quit")
                        sys.exit(0)
                    elif decision == "s":
                        print("Skip this step")
                        return
                    else:
                        continue
            print("Cleaned up all jpg album art file names")
        elif decision == "q":
            print("Quit")
            sys.exit(0)
        else:
            print("Skipped cleaning up jpg album art file names")


def find_nested_album_art(directory):
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
                filter(lambda f: Path(f).suffix[1:] in audio_extentions, files)
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
                            lambda f: Path(f).suffix[1:] in audio_extentions,
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


def move_album_art_files_to_album_dir(directory):
    art_directories = find_nested_album_art(directory)
    if art_directories["case1"]:
        print(
            f"Let's deal with {len(art_directories['case1'])} album art directories "
            "of first type"
        )
        decision = prompt(
            "Move all album art files to parent directory?", ["y", "n", "s", "q"]
        )
        if decision == "y":
            for art_dir in art_directories["case1"]:
                sub_dir = art_dir["art_dir"]
                parent = art_dir["parent_dir"]
                for filename in art_dir["art_files"]:
                    ext = Path(filename).suffix
                    name = Path(filename).name.replace(ext, "")
                    old_path = os.path.join(sub_dir, filename)
                    new_path = os.path.join(parent, filename)
                    if name.isdigit():
                        print(
                            f"Numeric art file name: {name} will rename to "
                            f"'booklet-{filename}'"
                        )
                        new_path = os.path.join(parent, f"booklet-{filename}")
                    if os.path.exists(new_path):
                        print(f"File already exists: {new_path}")
                        old_size = Path(new_path).stat().st_size // 8
                        new_size = Path(old_path).stat().st_size // 8
                        if old_size != new_size:
                            replace_decision = prompt(
                                f"Replace '{new_path}' ({new_size} bytes) with "
                                f"'{old_path}' ({old_size} bytes)?",
                                ["d", "y", "n", "s", "q"],
                            )
                            if replace_decision == "y":
                                try:
                                    print(f"Moved '{new_path}' to trashbin")
                                    send2trash(new_path)
                                    os.rename(old_path, new_path)
                                    print(f"Moved '{old_path}' to '{new_path}'")
                                except OSError as err:
                                    print(err)
                            elif replace_decision == "d":
                                send2trash(old_path)
                                print(f"Moved '{old_path}' to trashbin")
                            elif replace_decision == "q":
                                print("Quit")
                                sys.exit(0)
                            elif replace_decision == "s":
                                print("Skip this step")
                                return
                            else:
                                continue
                        else:
                            send2trash(old_path)
                            print(
                                f"Moved '{old_path}' to trashbin as it's the same "
                                "size as the file with the same name in the parent "
                                "directory"
                            )
                    else:
                        try:
                            os.rename(old_path, new_path)
                        except OSError as err:
                            print(err)

                leftover_files = [
                    f
                    for f in os.listdir(sub_dir)
                    if os.path.isfile(os.path.join(sub_dir, f))
                ]
                if not leftover_files:
                    send2trash(sub_dir)
                    print(f"Moved empty art dir '{sub_dir}' to trashbin")
                else:
                    print(
                        f"There are still files in album art directory '{sub_dir}': "
                        f"{leftover_files}"
                    )
        elif decision == "q":
            print("Quit")
            sys.exit(0)
        elif decision == "s":
            print("Skip this step")
            return
    else:
        print("No album art directories of first type! :)")


def process_command(command, *, stdout=None):
    """Executes shell command with subprocess.Popen.
    Returns tuple, where first element is a process return code,
    and the second is a tuple of stdout and stderr output.
    """
    print(f"Executing shell command: {command}")
    prc = Popen(command, shell=True, stdout=stdout)
    std = prc.communicate()
    return prc.returncode, std


def find_cue_files_and_audio_files(directory):
    result = []
    for sub_dir, _, files in os.walk(directory):
        cues = [f for f in files if Path(f).suffix[1:] == "cue"]
        if cues:
            audio_files = list(
                filter(lambda f: Path(f).suffix[1:] in audio_extentions, files)
            )
            cue_dir = {
                "dir": sub_dir,
                "cues": cues,
                "audio_files": audio_files,
            }
            result.append(cue_dir)

    return result


def find_empty_directories(directory):
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


def delete_empty_directories(directory):
    empty_directories = find_empty_directories(directory)
    if empty_directories:
        print(f"Found {len(empty_directories)} empty directories.")
        print("\n".join(empty_directories))
        decision = prompt("Delete all empty directories?", ["y", "n", "s", "q"])
        if decision == "y":
            for sub_dir in empty_directories:
                try:
                    send2trash(sub_dir)
                    print(f"Moved '{sub_dir}' to trashbin")
                except OSError as err:
                    print(err)
        elif decision == "s":
            print("Skip this step")
            return
        elif decision == "q":
            print("Quit")
            sys.exit(0)
    else:
        print("No empty directories found")


def what_to_do_with_cue(directory):
    cue_directories = find_cue_files_and_audio_files(directory)
    if not cue_directories:
        print(f"No cue files found in: {directory}")
    else:
        single_cue = [d for d in cue_directories if len(d["cues"]) == 1]
        multi_cue = [d for d in cue_directories if len(d["cues"]) > 1]
        print(
            f"Found {len(single_cue)} directories with single cue file & "
            f"{len(multi_cue)} directories with more than 1 cue file"
        )
        decision = prompt("Proceed with cue clean-up?", ["y", "n", "q"])
        if decision == "y":
            print("Let's start with directories containing more than 1 cue file")
            for cue_dir in multi_cue:
                print(
                    f"\n\nThere are {len(cue_dir['audio_files'])} audio files in "
                    f"{cue_dir['dir']} and {len(cue_dir['cues'])} CUE files"
                )
                for f in sorted(cue_dir["audio_files"]):
                    print(f"* {f}")
                for cue_file in cue_dir["cues"]:
                    cue_path = os.path.join(cue_dir["dir"], cue_file)
                    cue = CueParser(cue_path)
                    if "FILE" in cue.meta:
                        print(
                            f"'{cue_file}' refers to {len(cue.tracks)} tracks in 1 "
                            f"file: {cue.meta['FILE']}"
                        )
                    else:
                        print(
                            f"'{cue_file}' refers to {len(cue.tracks)} tracks in "
                            f"{len(set(t['FILE'] for t in cue.tracks))} file(s)"
                        )
                        print(
                            "Files:\n*",
                            "\n* ".join(
                                set(
                                    t.get("FILE", "NO FILE ENTRY!!!")
                                    for t in sorted(cue.tracks, key=lambda t: t["FILE"])
                                )
                            ),
                        )
                    print(
                        "Titles:\n*",
                        "\n* ".join(
                            t.get("TITLE", "NO TITLE ENTRY!!!")
                            for t in sorted(cue.tracks, key=lambda t: t["TRACK_NUM"])
                        ),
                    )

                for cue_file in cue_dir["cues"]:
                    cue_path = os.path.join(cue_dir["dir"], cue_file)

                    cue_decision = prompt(
                        f"What do you want to do with '{cue_file}'?",
                        ["d", "p", "s", "q"],
                    )

                    if cue_decision == "d":
                        send2trash(cue_path)
                        print(f"Moved '{cue_path}' to trash bin")
                    elif cue_decision == "p":
                        cmd = f"flacon -s '{cue_path}'"
                        return_code, std = process_command(cmd)
                        if return_code == 0:
                            print(f"Flacon successfully processed '{cue_path}'")
                            deleted_cue_decision = prompt(
                                f"Delete '{cue_file}' and source audio?",
                                ["d", "n", "s", "q"],
                            )
                            if deleted_cue_decision in ["d", "y"]:
                                cue_path = os.path.join(cue_dir["dir"], cue_file)
                                cue = CueParser(cue_path)
                                cue_audio_file = (
                                    cue.meta.get("FILE").replace(" ", "_").lower()
                                )
                                cue_audio_file_path = os.path.join(
                                    cue_dir["dir"], cue_audio_file
                                )
                                if not os.path.exists(cue_audio_file_path):
                                    print(
                                        f"Couldn't find audio file '{cue_audio_file}'"
                                        f" specified in '{cue_file}'"
                                    )
                                    for audio_file in cue_dir["audio_files"]:
                                        delete_entry_audio_file = prompt(
                                            "Delete '{audio_file}' and source audio?",
                                            ["d", "s", "q"],
                                        )
                                        if delete_entry_audio_file == "y":
                                            audio_file_path = os.path.join(
                                                cue_dir, audio_file
                                            )
                                            send2trash(audio_file_path)
                                            print(
                                                "Successfully deleted audio source "
                                                f"file: {audio_file}"
                                            )
                                else:
                                    send2trash(cue_audio_file_path)
                                    print(
                                        "Successfully deleted audio source file: "
                                        f"{cue_audio_file}"
                                    )
                                    send2trash(cue_path)
                                    print(f"Successfully deleted cue file: {cue_file}")
                            elif cue_decision == "q":
                                print("Quit")
                                sys.exit(0)
                            else:
                                print(f"Skipped '{cue_file}'")
                                continue
                        else:
                            print(f"Flacon had some issues with '{cue_path}': {std}")
                    elif cue_decision == "q":
                        print("Quit")
                        sys.exit(0)
                    else:
                        print(f"Skipped '{cue_path}'")
                        continue

            print("Let's now deal with directories with single cue file")

            cues_to_split = []
            cues_to_delete = []
            min_audio_files = 1
            for cue_dir in single_cue:
                cue_file = cue_dir["cues"][0]
                cue_path = os.path.join(cue_dir["dir"], cue_file)
                cue = CueParser(cue_path)
                files_equal_tracks = len(cue_dir["audio_files"]) == len(cue.tracks)
                more_files_than_min = len(cue_dir["audio_files"]) > min_audio_files
                if files_equal_tracks and more_files_than_min:
                    cues_to_delete.append(cue_dir)
                else:
                    cues_to_split.append(cue_dir)
            assert len(cues_to_delete) + len(cues_to_split) == len(single_cue)
            if cues_to_delete:
                print(
                    f"Found {len(cues_to_delete)} cue files with more than "
                    f"{min_audio_files} track that looks to be already extracted"
                )
                for cue_dir in cues_to_delete:
                    cue_file = cue_dir["cues"][0]
                    cue_path = os.path.join(cue_dir["dir"], cue_file)
                    cue = CueParser(cue_path)
                    print(
                        f"\n\nThere are {len(cue_dir['audio_files'])} audio files in "
                        f"{cue_dir['dir']}"
                    )
                    for f in sorted(cue_dir["audio_files"]):
                        print(f"* {f}")
                    print(
                        "CUE Titles:\n*",
                        "\n* ".join(
                            f'{t.get("TRACK_NUM")} - {t.get("TITLE", "NO TITLE ENTRY")}'
                            for t in sorted(cue.tracks, key=lambda t: t["TRACK_NUM"])
                        ),
                    )
                delete_extracted_cues = prompt(
                    f"Delete '{len(cues_to_delete)}' already extracted CUE files?",
                    ["d", "s", "q"],
                )
                if delete_extracted_cues in ["d", "y"]:
                    for cue_dir in cues_to_delete:
                        cue_file = cue_dir["cues"][0]
                        cue_path = os.path.join(cue_dir["dir"], cue_file)
                        send2trash(cue_path)
                    print(f"Deleted {len(cues_to_delete)} extracted CUE files")
                elif delete_extracted_cues == "q":
                    print("Quit")
                    sys.exit(0)
                else:
                    print(f"Skipped '{cue_file}'")

            if cues_to_split:
                for cue_dir in cues_to_split:
                    cue_file = cue_dir["cues"][0]
                    cue_path = os.path.join(cue_dir["dir"], cue_file)
                    cue = CueParser(cue_path)
                    print(
                        f"\n\nOnly {len(cue_dir['audio_files'])} audio file "
                        f"'{cue_dir['audio_files'][0]}' in '{cue_dir['dir']}'"
                    )
                    print(
                        f"Looks like it should be split into {len(cue.tracks)} tracks "
                        f"defined in '{cue_file}':"
                    )
                    print(
                        "CUE Tracks:\n*",
                        "\n* ".join(
                            f'{t.get("TRACK_NUM")} - {t.get("TITLE", "NO TITLE ENTRY")}'
                            for t in sorted(cue.tracks, key=lambda t: t["TRACK_NUM"])
                        ),
                    )

                cue_decision = prompt(
                    "Would you like to split those cue files with Flacon and delete "
                    "them afterwards?",
                    ["p", "s", "q"],
                )

                if cue_decision == "p":
                    for cue_dir in cues_to_split:
                        cue_file = cue_dir["cues"][0]
                        cue_path = os.path.join(cue_dir["dir"], cue_file)
                        cue = CueParser(cue_path)
                        cmd = f"flacon -s '{cue_path}'"
                        return_code, std = process_command(cmd)
                        if return_code == 0:
                            print(f"Flacon successfully processed '{cue_path}'")
                            cue_audio_file = (
                                cue.meta.get("FILE").replace(" ", "_").lower()
                            )
                            cue_audio_file_path = os.path.join(
                                cue_dir["dir"], cue_audio_file
                            )
                            if os.path.exists(cue_audio_file_path):
                                send2trash(cue_audio_file_path)
                                print(
                                    "Successfully deleted audio source file: "
                                    f"{cue_audio_file}"
                                )
                                send2trash(cue_path)
                                print(f"Successfully deleted cue file: {cue_file}")
                            else:
                                print(
                                    f"Couldn't find audio file '{cue_audio_file}' "
                                    f"specified in '{cue_file}'"
                                )
                                for audio_file in cue_dir["audio_files"]:
                                    audio_file_path = os.path.join(
                                        cue_dir["dir"], audio_file
                                    )
                                    send2trash(audio_file_path)
                                    print(
                                        "Successfully deleted audio source file: "
                                        f"{audio_file}"
                                    )
                                    send2trash(cue_path)
                                    print(f"Successfully deleted cue file: {cue_file}")
                        else:
                            print(f"Flacon had some issues with '{cue_path}': {std}")
                elif cue_decision == "q":
                    print("Quit")
                    sys.exit(0)
                else:
                    print(f"Skipped '{cue_path}'")

            print("Cleaned up all directories with cue files")
        elif decision == "q":
            print("Quit")
            sys.exit(0)
        else:
            print("Skipped cleaning up directories with cue files")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="dir to organise")
    args = parser.parse_args()
    directory = args.dir

    delete_extra_files(directory)
    delete_extra_text_files(directory)
    lower_extentions(directory)
    change_extensions(directory)
    non_audio_files_to_lower_case(directory)
    replace_spaces_with_underscores(directory)
    convert_album_art_to_jpg(directory)
    move_album_art_files_to_album_dir(directory)
    what_to_do_with_cue(directory)
    clean_up_jpg_album_art_file_names(directory)
    delete_empty_directories(directory)
