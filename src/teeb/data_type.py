from dataclasses import dataclass


@dataclass
class CuedAlbum:
    dir: str
    cues: list[str]
    audio_files: list[str]
