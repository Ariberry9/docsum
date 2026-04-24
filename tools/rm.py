import os
import glob
from git import Repo
from tools.path_safety import is_path_safe

def rm(path: str) -> str:
    repo = Repo(".")
    matches = glob.glob(path)

    if not matches:
        return f"No files matched {path}"

    removed = []

    for p in matches:
        if not is_path_safe(p):
            return "Error: unsafe path"

        if os.path.isfile(p):
            os.remove(p)
            repo.index.remove([p])
            removed.append(p)

    if removed:
        repo.index.commit(f"[docchat] rm {path}")

    return "Removed: " + ", ".join(removed)