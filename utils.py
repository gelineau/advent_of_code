from typing import Iterator, Any
from parse import compile


def read_lines_from_input(filename) -> Iterator[str]:
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()


def read_words_from_input(filename) -> Iterator[list[str]]:
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
