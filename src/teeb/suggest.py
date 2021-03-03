# -*- coding: utf-8 -*-


def new_art_file_name(filename: str) -> str:
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
