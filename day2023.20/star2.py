from collections import Counter, deque
from dataclasses import dataclass, field
from functools import lru_cache
from itertools import repeat, groupby
from pprint import pprint
from typing import Iterator, List, Optional, Any
from parse import compile
from grid import Grid

from utils import read_dicts_from_input, read_lines_from_input, read_words_from_input

high = True
low = False
flip_flop = "%"
conjunction = "&"
broadcaster = "broadcaster"


@dataclass
class Module:
    module_type: str
    name: str
    destinations: list[str]
    state = low
    state_per_origin: dict = field(default_factory=dict)

    def produce(self, origin, pulse_type) -> Optional[bool]:
        if self.module_type == broadcaster:
            return pulse_type
        if self.module_type == flip_flop:
            if pulse_type == high:
                return None
            if pulse_type == low:
                self.state = not self.state
                return self.state
        if self.module_type == conjunction:
            # print(f"state of {self.name} before: {self.state_per_origin}")
            self.state_per_origin[origin] = pulse_type
            if all(self.state_per_origin.values()):
                self.state = high
                return low
            self.state = low
            return high

        if self.module_type == "rx" and pulse_type == low:
            raise ValueError

        return None

    def receive(self, origin, pulse_type):
        new_type = self.produce(origin, pulse_type)
        if new_type is None:
            return
        for destination in self.destinations:
            yield self.name, destination, new_type

    def add_origin(self, origin):
        self.state_per_origin[origin] = low

    def number_high(self):
        return f"{sum(1 for state in self.state_per_origin.values() if state)}/{len(self.state_per_origin)}"


class State:
    def __init__(self, modules: list[Module]):
        self.pulses_queue = deque()
        self.modules = {module.name: module for module in modules}
        self.low_number = 0
        self.high_number = 0
        print(modules)
        for module in modules:
            for destination in module.destinations:
                # print(f"adding {destination=} for {module.name}")
                try:
                    self.modules[destination].add_origin(module.name)
                except KeyError:
                    pass
                # print(self.modules["inv"].state_per_origin)

    def consume(self, i=-1):
        while self.pulses_queue:
            source, destination, event_type = self.pulses_queue.popleft()
            if source == "kd" and destination == "ts" and (event_type == low):
                print("event detected, i=", i, event_type)
            if event_type == high:
                self.high_number += 1
            else:
                self.low_number += 1
            # print(f"{source} -{'high' if event_type else 'low'}-> {destination}")
            # print(f"{self.low_number=} {self.high_number=}")

            for name, destination, new_type in self.modules[destination].receive(
                source, event_type
            ):
                self.pulses_queue.append((name, destination, new_type))

    def debug(self):
        return ", ".join(
            str(self.modules[name].number_high()) for name in ["zz", "mh", "cm", "kd"]
        )


def read_input(filename: str):
    template = "{name_string} -> {destinations_string}"
    for values in read_dicts_from_input(filename, template):
        if values["name_string"] == "broadcaster":
            module_type = name = "broadcaster"
        else:
            module_type = values["name_string"][0]
            name = values["name_string"][1:]
        destinations = values["destinations_string"].split(", ")
        yield Module(module_type, name, destinations)
    yield Module("button", "button", ["broadcaster"])
    yield Module("output", "output", [])
    yield Module("rx", "rx", [])


def star(filename: str):
    modules = list(read_input(filename))
    state = State(modules)

    for i in range(50_000):
        try:
            state.pulses_queue.append(("button", "broadcaster", low))
            state.consume(i)

        except ValueError:
            return i


#
# print(math.lcm(8038, 7886, 7894, 8014))
# 501257920131584 too high

# math.lcm(4019,3943,3947,4018)
# 251316985661182


# 251316985661181 too high

# math.lcm(4019,3943,3947,4007)
# 250628960065793

# 250628960065792 wrong
