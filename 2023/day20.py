from __future__ import annotations
from collections import Counter, OrderedDict, defaultdict, deque
from dataclasses import dataclass
from math import lcm
from time import time
from typing import cast

YEAR = 2023
DAY = 20
NAME = "Pulse Propagation"

DEBUG_PRINT_PULSES = False


class Module:
    def __init__(self, name: str):
        self.name = name
        self.input_modules: OrderedDict[str, Module] = OrderedDict()
        self.output_modules: OrderedDict[str, Module] = OrderedDict()
        self.pulses_sent: Counter = Counter()

    def add_input(self, module: Module) -> None:
        self.input_modules[module.name] = module

    def add_output(self, module: Module) -> None:
        self.output_modules[module.name] = module

    def eval(self, pulse: Pulse) -> list[Pulse]:
        raise NotImplementedError


@dataclass
class Pulse:
    src: Module
    dst: Module
    value: int


class FlipFlop(Module):
    def __init__(self, name: str):
        super(FlipFlop, self).__init__(name)
        self.state: int = 0

    def eval(self, pulse: Pulse) -> list[Pulse]:
        results = []

        if pulse.value == 0:
            self.state = (self.state + 1) % 2
            for module in self.output_modules.values():
                result = Pulse(src=self, dst=module, value=self.state)
                results.append(result)
                self.pulses_sent[self.state] += 1

        return results


class Conjunction(Module):
    def __init__(self, name: str):
        super(Conjunction, self).__init__(name)
        self.state: int = 0
        self.input_module_last_states: dict[str, int] = {}

    def add_input(self, module: Module) -> None:
        super(Conjunction, self).add_input(module)
        self.input_module_last_states[module.name] = 0

    def eval(self, pulse: Pulse) -> list[Pulse]:
        results = []

        self.input_module_last_states[pulse.src.name] = pulse.value

        all_inputs_high = (
            sum(self.input_module_last_states.values()) ==
            len(self.input_module_last_states)
        )
        if all_inputs_high:
            self.state = 0
        else:
            self.state = 1

        for module in self.output_modules.values():
            result = Pulse(src=self, dst=module, value=self.state)
            results.append(result)
            self.pulses_sent[self.state] += 1

        return results


class Broadcaster(Module):
    def __init__(self, name: str):
        super(Broadcaster, self).__init__(name)

    def eval(self, pulse: Pulse) -> list[Pulse]:
        results = []

        for module in self.output_modules.values():
            result = Pulse(src=self, dst=module, value=pulse.value)
            results.append(result)
            self.pulses_sent[pulse.value] += 1

        return results


class Untyped(Module):
    def __init__(self, name: str):
        super(Untyped, self).__init__(name)

    def eval(self, pulse: Pulse) -> list[Pulse]:
        return []


class Button(Module):
    def __init__(self, name: str):
        super(Button, self).__init__(name)

    def press(self) -> list[Pulse]:
        results = []

        value = 0
        for module in self.output_modules.values():
            result = Pulse(src=self, dst=module, value=value)
            results.append(result)
            self.pulses_sent[value] += 1

        return results


def setup_modules(input: str) -> dict[str, Module]:
    # Mapping of module names to Module instances
    names_to_modules: dict[str, Module] = {}

    # Unique module names encountered - used below to create modules that are
    # only referenced in outputs
    names = set()

    # Mapping of input module names to their outputs, used to connect modules
    # once all have been instantiated
    input_names_to_output_names: dict[str, list[str]] = defaultdict(list)

    # First pass to bootstrap modules and get the full set of connections
    for line in input.strip().split("\n"):
        parts = line.split(" -> ")
        in_description, out_description = parts[0], parts[1]
        output_names = out_description.split(", ")

        if in_description.startswith("%"):
            input_name = in_description[1:]
            names_to_modules[input_name] = FlipFlop(input_name)
        elif in_description.startswith("&"):
            input_name = in_description[1:]
            names_to_modules[input_name] = Conjunction(input_name)
        elif in_description.startswith("broadcaster"):
            input_name = in_description
            names_to_modules[input_name] = Broadcaster(input_name)
        else:
            raise RuntimeError(f"Unhandled line '{line}'")

        input_names_to_output_names[input_name] += output_names

        names.add(input_name)
        for output_name in output_names:
            names.add(output_name)

    # Create modules only referenced in outputs (output, rx, etc.)
    untyped_module_names = names - set(names_to_modules.keys())
    for n in untyped_module_names:
        names_to_modules[n] = Untyped(n)

    # Add button module and ensure its connected to the broadcaster module by
    # adding an explicit connection
    # NOTE: Only needed for Part 1 but doesn't affect Part 2
    button = Button("button")
    names_to_modules[button.name] = button
    input_names_to_output_names["button"].append("broadcaster")

    # Make module connections
    for input_name, output_names in input_names_to_output_names.items():
        input_module = names_to_modules[input_name]
        for output_name in output_names:
            output_module = names_to_modules[output_name]
            input_module.add_output(output_module)
            output_module.add_input(input_module)

    return names_to_modules


def determine_target_bit_pattern(module: Module,
                                 target_conjugations: set[str],
                                 depth: int = 0) -> int:
    """
    From the starting module, recursively follow only FlipFlops while building
    up the bit pattern determine by FlipFlip nodes that have an output node
    that is one of the target Conjugation nodes.
    This returns the target value used as one of four values to determine the
    least common multiple
    NOTE: Part 2 only. This relies on a known structure of FlipFlop and
    Conjugation nodes in order to work.
    """
    n = 0

    for output in module.output_modules.values():
        if output.name in target_conjugations:
            n |= 1 << depth
        if isinstance(output, FlipFlop):
            n |= determine_target_bit_pattern(
                output, target_conjugations, depth+1)

    return n


def part1(input: str) -> int:
    names_to_modules = setup_modules(input)

    for i in range(1000):
        button = cast(Button, names_to_modules["button"])
        initial = button.press()
        pulse_queue = deque(initial)
        while pulse_queue:
            pulse = pulse_queue.popleft()
            if DEBUG_PRINT_PULSES:
                print(f"{pulse.src.name}" +
                      f" {'-high' if pulse.value else '-low'}->" +
                      f" {pulse.dst.name}")
            next_pulses = pulse.dst.eval(pulse)

            # NOTE: It feels like we need to be aware of conjunction modules
            # and ensuring that they're only evaluated once all their inputs
            # have been evaluated for the 'current loop' (as we may end up
            # going round part of the circuit again before the state settles),
            # so we want some way to ensure this. However, a topological sort
            # on the nodes is awkward as we don't have an acyclic graph, but
            # we also seem to get the right results without any special
            # attention paid to the ordering of 'next' pulses ¯\_(ツ)_/¯
            for next_pulse in next_pulses:
                pulse_queue.append(next_pulse)

        if DEBUG_PRINT_PULSES:
            print("-" * 100)

    # Sum pulses across all modules
    pulse_counter: Counter = Counter()
    for module in names_to_modules.values():
        pulse_counter.update(module.pulses_sent)

    total = pulse_counter[0] * pulse_counter[1]
    return total


def part2(input: str) -> int:
    names_to_modules = setup_modules(input)

    # Traversing the module structure from rx back to the conjugation modules
    # that are part of the binary shift registers so we can use them as target
    # nodes to determine the bit pattern (and thus the value) we need to use
    # to compute the lowest common multiple.
    rx = names_to_modules["rx"]
    before_rx = list(rx.input_modules.values())[0]

    # Set of conjugation module names we know to look for when determining the
    # bit pattern for each shift register
    target_conjugations = set()
    for module in before_rx.input_modules.values():
        target_conjugations.add(list(module.input_modules.values())[0].name)

    lcms = []
    roots = names_to_modules["broadcaster"].output_modules.values()
    for root in roots:
        value = determine_target_bit_pattern(root, target_conjugations)
        lcms.append(value)

    return lcm(*lcms)


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day20_example1.txt", part1, 32000000),
        ("Part 1", "inputs/day20_example2.txt", part1, 11687500),
        ("Part 1", "inputs/day20_full.txt", part1, 817896682),
        ("Part 2", "inputs/day20_full.txt", part2, 250924073918341),
    ):
        with open(filename) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
