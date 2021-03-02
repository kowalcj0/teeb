# -*- coding: utf-8 -*-
"""
Modified version of a Cue Sheet parser from idlesign.
https://github.com/idlesign/deflacue/blob/master/deflacue/deflacue.py

Improvements:
    * turned get_global_context & context_tracks into .meta & .tracks properties
    * auto text encoding detection with chardet
    * support Cue Sheets with multiple FILE entries
    * support extra fields: ISRC, PREGAP etc
"""
import logging
from copy import deepcopy

import chardet


class CueParser:
    """Simple Cue Sheet file parser."""

    def __init__(self, cue_file):
        self._context_global = {
            "PERFORMER": "Unknown",
            "SONGWRITER": None,
            "ALBUM": "Unknown",
            "GENRE": "Unknown",
            "DATE": None,
            "FILE": None,
            "COMMENT": None,
        }
        self._context_tracks = []

        self._current_context = self._context_global
        with open(cue_file, "rb") as file:
            self.encoding = chardet.detect(file.read())["encoding"]
        try:
            with open(cue_file, "r", encoding=self.encoding) as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            raise UnicodeDecodeError(
                "Unable to read data from .cue file. Please set correct encoding."
            )

        for line in lines:
            if line.strip():
                command, args = line.strip().split(" ", 1)
                logging.debug(f"Command `{command}`. Args: {args}")
                method = getattr(self, f"_cmd_{command.lower()}", None)
                if method is not None:
                    method(args)
                else:
                    print(
                        f"Unknown command `{command}`. Skipping ...",
                    )

        for idx, track_data in enumerate(self._context_tracks):
            track_end_pos = None
            try:
                track_end_pos = self._context_tracks[idx + 1]["POS_START_SAMPLES"]
            except IndexError:
                pass
            track_data["POS_END_SAMPLES"] = track_end_pos

        unique_track_files = list(set(track["FILE"] for track in self.tracks))
        if [self._context_global["FILE"]] != unique_track_files:
            logging.debug(
                "Remove global FILE entry as it's different from track specific ones"
            )
            del self._context_global["FILE"]
        else:
            logging.debug(
                "Remove track FILE entries as they're the same as the global one"
            )
            for idx in range(len(self.tracks)):
                del self.tracks[idx]["FILE"]

    @property
    def meta(self):
        """Returns a dictionary with global CD data."""
        return self._context_global

    @property
    def tracks(self):
        """Returns a list of dictionaries with individual
        tracks data. Note that some of the data is borrowed from global data.
        """
        return self._context_tracks

    def _unquote(self, in_str):
        return in_str.strip(' "')

    def _timestr_to_sec(self, timestr):
        """Converts `mm:ss:` time string into seconds integer."""
        splitted = timestr.split(":")[:-1]
        splitted.reverse()
        seconds = 0
        for i, chunk in enumerate(splitted, 0):
            factor = pow(60, i)
            if i == 0:
                factor = 1
            seconds += int(chunk) * factor
        return seconds

    def _timestr_to_samples(self, timestr):
        """Converts `mm:ss:ff` time string into samples integer, assuming the
        CD sampling rate of 44100Hz."""
        seconds_factor = 44100
        # 75 frames per second of audio
        frames_factor = seconds_factor // 75
        full_seconds = self._timestr_to_sec(timestr)
        frames = int(timestr.split(":")[-1])
        return full_seconds * seconds_factor + frames * frames_factor

    def _in_global_context(self):
        return self._current_context == self._context_global

    def _cmd_rem(self, args):
        try:
            sub_command, sub_args = args.split(" ", 1)
        except ValueError:
            print(f"Found empty: {args}")
        else:
            if sub_args.startswith('"'):
                sub_args = self._unquote(sub_args)
            self._current_context[sub_command.upper()] = sub_args

    def _cmd_performer(self, args):
        unquoted = self._unquote(args)
        self._current_context["PERFORMER"] = unquoted

    def _cmd_title(self, args):
        unquoted = self._unquote(args)
        if self._in_global_context():
            self._current_context["ALBUM"] = unquoted
        else:
            self._current_context["TITLE"] = unquoted

    def _cmd_isrc(self, args):
        unquoted = self._unquote(args)
        self._current_context["ISRC"] = unquoted

    def _cmd_comment(self, args):
        unquoted = self._unquote(args)
        self._current_context["COMMENT"] = unquoted

    def _cmd_catalog(self, args):
        unquoted = self._unquote(args)
        self._current_context["CATALOG"] = unquoted

    def _cmd_flags(self, args):
        unquoted = self._unquote(args)
        self._current_context["FLAGS"] = unquoted

    def _cmd_pregap(self, args):
        unquoted = self._unquote(args)
        self._current_context["PREGAP"] = unquoted

    def _cmd_file(self, args):
        filename = self._unquote(args.rsplit(" ", 1)[0])
        self._current_file_context = filename
        if not self._current_context["FILE"]:
            self._current_context["FILE"] = filename

    def _cmd_index(self, args):
        time_str = args.split()[1]
        self._current_context["INDEX"] = time_str
        self._current_context["POS_START_SAMPLES"] = self._timestr_to_samples(time_str)

    def _cmd_track(self, args):
        num, _ = args.split()
        new_track_context = deepcopy(self._context_global)
        self._context_tracks.append(new_track_context)
        self._current_context = new_track_context
        self._current_context["TRACK_NUM"] = int(num)
        if self._current_context["FILE"] != self._current_file_context:
            self._current_context["FILE"] = self._current_file_context
