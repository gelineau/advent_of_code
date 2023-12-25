from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from pprint import pprint
from typing import Iterator, List, Optional, Any

import networkx
from parse import compile
from grid import Grid

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input


def read_input(filename: str):
    template = "{origin}: {destinations_string}"
    for values in read_dicts_from_input(filename, template):
        yield values["origin"], values["destinations_string"].split()


def star(filename: str):
    input = list(read_input(filename))
    last_id = -1
    to_id = {}
    for origin, destinations in input:
        last_id += 1
        to_id[origin] = last_id
        for destination in destinations:
            last_id += 1
            to_id[destination] = last_id

    graph = networkx.Graph()
    for id in to_id.values():
        graph.add_node(id)

    for origin, destinations in input:
        for destination in destinations:
            graph.add_edge(to_id[origin], to_id[destination])

    communities = networkx.community.kernighan_lin_bisection(graph)
    print([len(community) for community in communities])
    for communities in networkx.community.girvan_newman(graph):
        print([len(community) for community in communities])
        if len(communities) >= 4:
            break

    # 539490 too high
