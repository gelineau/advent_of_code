from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pathlib import Path
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile
import time

import star1
import star2


filenames_star1 = [
    "puzzle_s1.txt",
]

for filename in filenames_star1:
    if Path(filename).stat().st_size == 0:
        continue
    print("\n", "#-1-" * 80, "\n")
    start = time.time()
    print(f"{filename=} {star1.star(filename)=}")
    print(f"{time.time()-start:.2f} seconds")

filenames_star2 = [
    # "puzzle_simpletest2.txt",
    "puzzle_test.txt",
    "puzzle.txt",
]
for filename in filenames_star2:
    if Path(filename).stat().st_size == 0:
        continue
    print("\n", "*=2=" * 80, "\n")
    start = time.time()
    print(f"{filename=} {star2.star(filename)=}")
    print(f"{time.time()-start:.2f} seconds")
