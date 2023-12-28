import time
from typing import Dict, List, Tuple

from loguru import logger

DEBUG: bool = False

REJECT: str = "R"
ACCEPT: str = "A"
STARTING_WORKFLOW_NAME: str = "in"


class Workflow:
    def __init__(self, name: str, rules: List[str]):
        """Pass in ('pz', ['a<2006:qkq', 'rfg'])"""
        self.name: str = name
        self.rules: List[Tuple[Tuple[str, str, int], str]] = []

        for rule in rules:
            if rule.find(":") != -1:
                condition, destination = rule.split(":", 1)
                op_index: int = condition.find("<")
                if op_index == -1:
                    op_index = condition.find(">")

                self.rules.append(
                    (
                        (
                            condition[:op_index],
                            condition[op_index : op_index + 1],
                            int(condition[op_index + 1 :]),
                        ),
                        destination,
                    )
                )
            else:
                self.rules.append((("x", ">", -1), rule))

    def pass_through(self, x: int, m: int, a: int, s: int) -> str:
        for rule in self.rules:
            condition: Tuple[str, str, int] = rule[0]
            dest: str = rule[1]

            lhs: int = x
            if condition[0] == "x":
                lhs = x
            elif condition[0] == "m":
                lhs = m
            elif condition[0] == "a":
                lhs = a
            elif condition[0] == "s":
                lhs = s

            if condition[1] == "<" and lhs < condition[2]:
                return dest
            elif condition[1] == ">" and lhs > condition[2]:
                return dest

        return self.rules[-1][1]

    def __str__(self) -> str:
        return f"Workflow{{{self.name}}} = {self.rules}"


def should_accept_part(
    name_to_workflow: Dict[str, Workflow], x: int, m: int, a: int, s: int
) -> bool:
    current_workflow_name: str = STARTING_WORKFLOW_NAME
    while current_workflow_name != REJECT and current_workflow_name != ACCEPT:
        old_name: str = current_workflow_name
        current_workflow: Workflow = name_to_workflow[current_workflow_name]
        current_workflow_name = current_workflow.pass_through(x, m, a, s)

        #  logger.debug(f"Flowed from {old_name} to {current_workflow_name}")

    return current_workflow_name == ACCEPT


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day19.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    name_to_workflow: Dict[str, Workflow] = {}

    xmas: List[Tuple[int, int, int, int]] = []
    found_empty: bool = False
    for line in input_lines:
        if len(line) == 0:
            found_empty = True
            continue
        if found_empty:
            parts: List[int] = [int(s[2:]) for s in line[1:-1].split(",")]
            xmas.append((parts[0], parts[1], parts[2], parts[3]))
        else:
            brace_index: int = line.find("{")
            name: str = line[:brace_index]
            rules: List[str] = line[1 + brace_index : -1].split(",")
            name_to_workflow[name] = Workflow(name, rules)

    answer: int = sum(
        sum(xma) for xma in xmas if should_accept_part(name_to_workflow, *xma)
    )
    logger.info(f"{answer=}")  # 383682


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
