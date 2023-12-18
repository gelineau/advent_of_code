from pathlib import Path
from typing import Iterator, Any
from parse import compile


def read_lines_from_input(filename: str) -> Iterator[str]:
    _check_input_end(filename)
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()


def read_words_from_input(filename: str) -> Iterator[list[str]]:
    for line in read_lines_from_input(filename):
        yield line.split()


def read_dicts_from_input(
    filename: str, template: str, debug=False
) -> Iterator[dict[str, Any]]:
    parsing_template = compile(template)
    for line in read_lines_from_input(filename):
        if debug:
            print(line)
        result = parsing_template.parse(line)
        if result is None:
            raise ValueError(f"could not parse `{line}` with template `{template}`")
        yield result.named


def read_text_from_input(filename: str) -> str:
    _check_input_end(filename)
    return Path(filename).read_text()


def read_line_groups_from_input(filename: str) -> Iterator[list[str]]:
    groups = read_text_from_input(filename).split("\n\n")
    for group in groups:
        yield group.split("\n")


def _check_input_end(filename: str):
    if Path(filename).read_text().endswith("\n"):
        raise ValueError("le fichier de données se termine par \\n")
