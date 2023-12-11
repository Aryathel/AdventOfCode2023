from urllib.request import urlopen, Request
from os import getenv, path, environ, mkdir


def root() -> str | None:
    src = './'

    for _ in range(3):
        env = path.join(path.abspath(src), '.env')
        if path.exists(env):
            return path.abspath(src)
        else:
            src = f"../{src}"


def loadenv() -> None:
    src = './'

    for _ in range(3):
        env = path.join(path.abspath(src), '.env')
        if path.exists(env):
            with open(env, "r") as f:
                lines = [l.strip().split("=") for l in f.readlines()]
                for k, v in lines:
                    environ[k] = v
                return
        else:
            src = f"../{src}"

    raise EnvironmentError(".env file not found.")


def save_day_inputs(days: list[int] = None) -> None:
    days = days or list(range(1, 26, 1))

    loadenv()
    rt = root()

    if not path.exists(path.join(rt, 'input')):
        mkdir(path.join(rt, 'input'))

    session_key = getenv("AoC2023SessionKey")
    if not session_key:
        raise EnvironmentError("AoC2023SessionKey environment variables missing.")

    for day in days:
        inp_file = path.join(rt, 'input', f'day_{day}.txt')
        if not path.exists(inp_file):
            req = Request(f"https://adventofcode.com/2023/day/{day}/input")
            req.add_header("Cookie", f"session={session_key}")
            with urlopen(req) as response:
                with open(inp_file, "w+") as input_file:
                    input_file.write(response.read().decode('utf-8').strip())


def get_day_input(day: int) -> str:
    rt = root()

    inp_file = path.join(rt, 'input', f'day_{day}.txt')

    if not path.exists(inp_file):
        save_day_inputs([day])

    if not path.exists(inp_file):
        raise EnvironmentError(f"Failed to load day input for file: {inp_file}")

    with open(inp_file, "r") as inp:
        return inp.read().strip()
