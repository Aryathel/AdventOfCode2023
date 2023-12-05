def file_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        return [l.strip() for l in file.readlines()]


def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read().strip()
