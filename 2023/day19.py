from dataclasses import dataclass, field
from functools import partial
from pathlib import Path
from time import time
from typing import Callable, Optional

YEAR = 2023
DAY = 19
NAME = "Aplenty"

DEBUG_PRINT = False


def merge_dicts(a: dict, b: dict) -> dict:
    c = a.copy()
    c.update(b)
    return c


def product(values: list[int]) -> int:
    """
    Like sum() but for multiplication. Not tested with floats.

    >>> product([0,1,2])
    0
    >>> product([1,2,3])
    6
    """
    if len(values) == 1:
        return values[0]
    else:
        return values[0] * product(values[1:])


@dataclass(frozen=True)
class Range:
    min: int
    max: int


@dataclass
class Rule:
    result: str
    category: Optional[str]
    comparison: Optional[str]
    value: Optional[int]
    condition: Optional[Callable[[int], bool]]

    def evaluate(self, part: dict) -> Optional[str]:
        if self.category is not None:
            assert self.condition is not None
            if self.condition(part[self.category]):
                return self.result
            else:
                return None
        else:
            return self.result


@dataclass
class Node:
    name: str
    rules: list[Rule] = field(default_factory=list)


def parse_workflow(s: str) -> tuple[str, list[Rule]]:
    begin = s.find("{")
    end = s.rfind("}")
    name = s[:begin]

    rules = []
    rule_strings = s[begin+1:end].split(",")
    for rule_string in rule_strings:
        if ":" in rule_string:
            definition, result = rule_string.split(":")
            category = definition[0]
            comparison = definition[1]
            against = int(definition[2:])

            # NOTE: Rule conditions as partially evaluated lambda functions
            # This is a neat way to do Part 1 but is not so useful for Part 2,
            # where we need the comparison type and the comparison value while
            # traversing a DAG representing the workflows
            if comparison == "<":
                condition = partial(lambda a, b: a < b, b=against)
            elif comparison == ">":
                condition = partial(lambda a, b: a > b, b=against)
            else:
                raise RuntimeError(
                    f"Unsupported comparison type '{comparison}'")

            rule = Rule(
                result=result,
                category=category,
                comparison=comparison,
                value=against,
                condition=condition,
            )
        else:
            rule = Rule(
                result=rule_string,
                category=None,
                comparison=None,
                value=None,
                condition=None,
            )

        rules.append(rule)

    return name, rules


def parse_part(s: str) -> dict:
    part = {}

    ratings = s.strip("{}").split(",")
    for rating in ratings:
        category, value_str = rating.split("=")
        part[category] = int(value_str)

    return part


def worklow_DAG(workflows: dict[str, list[Rule]]) -> dict[str, Node]:
    workflow_names_to_nodes = {}

    for name, rules in workflows.items():
        node = Node(name)
        for rule in rules:
            node.rules.append(rule)
        workflow_names_to_nodes[name] = node

    workflow_names_to_nodes["A"] = Node(name="A")
    workflow_names_to_nodes["R"] = Node(name="R")

    return workflow_names_to_nodes


def workflow_DAG_eval(graph: dict[str, Node],
                      workflow: str,
                      rating_ranges: dict[str, Range],
                      depth: int = 0) -> int:
    total = 0

    node = graph[workflow]

    if DEBUG_PRINT:
        print("  " * depth + node.name + " " + str(rating_ranges))

    if node.name == "A":
        total += product([v.max - v.min + 1 for v in rating_ranges.values()])
        return total
    else:
        for rule in node.rules:
            if rule.category is not None:
                assert rule.comparison is not None
                assert rule.value is not None
                original_category_range = rating_ranges[rule.category]
                if rule.comparison == "<":
                    # Range for the next workflow branch
                    updated_category_subrange_a = Range(
                        min=original_category_range.min,
                        max=min(original_category_range.max, rule.value - 1)
                    )
                    # Remaining range used for next rule evaluation
                    updated_category_subrange_b = Range(
                        min=rule.value,
                        max=original_category_range.max,
                    )
                elif rule.comparison == ">":
                    # Range for the next workflow branch
                    updated_category_subrange_a = Range(
                        min=max(original_category_range.min, rule.value + 1),
                        max=original_category_range.max
                    )
                    # Remaining range used for next rule evaluation
                    updated_category_subrange_b = Range(
                        min=original_category_range.min,
                        max=rule.value,
                    )
                else:
                    raise RuntimeError(
                        f"Unsupported comparison type '{rule.comparison}'")

                updated_ranges_a = merge_dicts(
                    rating_ranges,
                    {rule.category: updated_category_subrange_a}
                )
                updated_ranges_b = merge_dicts(
                    rating_ranges,
                    {rule.category: updated_category_subrange_b}
                )

                # Conditional rules are evaluated using the updated range
                # defined by the condition
                total += workflow_DAG_eval(
                    graph, rule.result, updated_ranges_a, depth+1)

                # Rating ranges are continuously updated as each rule is
                # evaluated with each rule getting the latest updated range
                # (essentially the remainder of the previous rule condition)
                rating_ranges = updated_ranges_b
            else:
                # Unconditional rules are evaluated using the current
                # (remaining) range
                total += workflow_DAG_eval(
                    graph, rule.result, rating_ranges, depth+1)

    return total


def part1(input: str) -> int:
    workflows = {}
    parts = []

    for line in input.strip().split("\n"):
        if line == "":
            continue

        if line.startswith("{"):
            part = parse_part(line)
            parts.append(part)
        else:
            name, rules = parse_workflow(line)
            workflows[name] = rules

    total = 0
    for part in parts:
        current_workflow = "in"
        evaluating_part = True
        while evaluating_part:
            for rule in workflows[current_workflow]:
                result = rule.evaluate(part)
                if result is not None:
                    if result == "A":
                        total += sum(part.values())
                        evaluating_part = False
                    elif result == "R":
                        evaluating_part = False
                    else:
                        current_workflow = result
                    break
    return total


def part2(input: str) -> int:
    workflows = {}
    for line in input.strip().split("\n"):
        if not line.startswith("{"):
            name, rules = parse_workflow(line)
            workflows[name] = rules

    graph = worklow_DAG(workflows)
    root = "in"
    rating_ranges = {
        "x": Range(min=1, max=4000),
        "m": Range(min=1, max=4000),
        "a": Range(min=1, max=4000),
        "s": Range(min=1, max=4000),
    }
    total = workflow_DAG_eval(graph, root, rating_ranges)
    return total


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day19_example.txt", part1, 19114),
        ("Part 1", "inputs/day19_full.txt", part1, 409898),
        ("Part 2", "inputs/day19_example.txt", part2, 167409079868000),
        ("Part 2", "inputs/day19_full.txt", part2, 113057405770956),
    ):
        path = Path(__file__).parent / filename
        with open(path) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
