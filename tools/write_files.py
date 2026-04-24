from git import Repo
from tools.path_safety import is_path_safe
from tools.doctests import doctests

def write_files(files, commit_message):
    repo = Repo(".")
    written = []

    for file in files:
        path = file["path"]
        contents = file["contents"]

        if not is_path_safe(path):
            return "Error: unsafe path"

        with open(path, "w", encoding="utf8") as f:
            f.write(contents)

        repo.index.add([path])
        written.append(path)

    repo.index.commit(f"[docchat] {commit_message}")

    output = f"Wrote files: {', '.join(written)}"

    for path in written:
        if path.endswith(".py"):
            output += "\n\nDoctest output:\n"
            output += doctests(path)

    return output


def write_file(path, contents, commit_message):
    return write_files(
        [{"path": path, "contents": contents}],
        commit_message,
    )