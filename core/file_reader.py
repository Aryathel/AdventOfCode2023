def file_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        return file.readlines()
