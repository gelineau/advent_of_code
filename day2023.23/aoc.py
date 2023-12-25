from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pathlib import Path
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile
import time


import star2_2


filenames_star2 = [
    "puzzle_simpletest2.txt",
    "puzzle_test.txt",
    "puzzle.txt",
]
for filename in filenames_star2:
    if Path(filename).stat().st_size == 0:
        continue
    print("\n", "*=2=" * 80, "\n")
    start = time.time()
    print(f"{filename=} {star2_2.star(filename)=}")
    print(f"{time.time()-start:.2f} seconds")
