def file_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        return [l.strip() for l in file.readlines()]
