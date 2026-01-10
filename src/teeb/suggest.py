from pathlib import Path


def new_art_file_name(filename: str) -> list[str]:
    """Suggest a file name change.

    Returns a sorted list of file name suggestions.
    """
    clean_names = [
        "inlay",
        "cover",
        "cover_out",
        "inside",
        "back",
        "matrix",
        "obi",
        "disc",
        "cd",
        "cd1",
        "cd2",
        "cd3",
        "cd4",
        "cd5",
        "cd6",
        "cd7",
        "cd8",
        "cd9",
        "cd_1",
        "cd_2",
        "cd_3",
        "cd_4",
        "cd_5",
        "cd_6",
        "cd_7",
        "cd_8",
        "cd_9",
    ]

    file_path = Path(filename)
    name = file_path.stem
    extension = Path(file_path).suffix.lower()

    if name in clean_names:
        return []

    suggestions: set[str] = set()
    if "inlay" in filename:
        suggestions.add("inlay")
    if "przod" in filename:
        suggestions.add("cover")
    if "folder" in filename:
        suggestions.add("cover")
    if "front" in filename:
        suggestions.add("cover")
    if "cover" in filename:
        suggestions.add("cover")
    if "cover" in filename and "out" in filename:
        suggestions.add("cover_out")
    if "srodek" in filename:
        suggestions.add("inside")
    if "inside" in filename:
        suggestions.add("inside")
    if "tyl" in filename:
        suggestions.add("back")
    if "cd" in filename:
        suggestions.add("cd")
    if "disc" in filename:
        suggestions.add("disc")
    if "matrix" in filename:
        suggestions.add("matrix")
    if "obi" in filename:
        suggestions.add("obi")
    if "back" in filename:
        suggestions.add("back")

    suggestions: set[str] = {f"{name}{extension}" for name in suggestions}

    return sorted(list(suggestions))
