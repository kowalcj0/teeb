# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List


@dataclass
class CuedAlbum:
    dir: str
    cues: List[str]
    audio_files: List[str]
