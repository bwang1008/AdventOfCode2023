import math
import queue
import time
from typing import Dict, List, Tuple

from loguru import logger

DEBUG: bool = False

REJECT: str = "R"
ACCEPT: str = "A"
STARTING_WORKFLOW_NAME: str = "in"

MIN_RATING: int = 1
MAX_RATING: int = 4000

LETTER_ORDERING: str = "xmas"


class Range:
    def __init__(self, r_min, r_max):
        self.r_min = r_min
        self.r_max = r_max

    def __str__(self) -> str:
        return f"[{self.r_min}, {self.r_max})"

    def __len__(self) -> int:
        return self.r_max - self.r_min


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

    def pass_through(self, ranges: List[Range]) -> List[Tuple[str, List[Range]]]:
        answer: List[Tuple[str, List[Range]]] = []

        for rule in self.rules:
            condition: Tuple[str, str, int] = rule[0]
            dest: str = rule[1]

            affected_range_index = LETTER_ORDERING.find(condition[0])
            affected_range: Range = ranges[affected_range_index]

            ranges_copy: List[Range] = ranges.copy()
            op_is_lower: bool = condition[1] == "<"

            if affected_range.r_min <= condition[2] < affected_range.r_max:
                split_lower_range: Range = (
                    Range(affected_range.r_min, condition[2])
                    if op_is_lower
                    else Range(affected_range.r_min, condition[2] + 1)
                )
                split_upper_range: Range = (
                    Range(condition[2], affected_range.r_max)
                    if op_is_lower
                    else Range(condition[2] + 1, affected_range.r_max)
                )

                ranges_copy[affected_range_index] = (
                    split_lower_range if op_is_lower else split_upper_range
                )
                answer.append((dest, ranges_copy))
                ranges[affected_range_index] = (
                    split_upper_range if op_is_lower else split_lower_range
                )
            elif (condition[2] < affected_range.r_min and not op_is_lower) or (
                affected_range.r_max <= condition[2] and op_is_lower
            ):
                # have 'x>1000' and range is [2000, 3000)
                # or 'x<1000' and range is [500, 600)
                answer.append((dest, ranges_copy))
                break

        return answer

    def __str__(self) -> str:
        return f"Workflow{{{self.name}}} = {self.rules}"


def run_ranges(name_to_workflow: Dict[str, Workflow]) -> int:
    answer: int = 0

    q: queue.Queue = queue.Queue()
    q.put(
        (
            STARTING_WORKFLOW_NAME,
            [Range(MIN_RATING, MAX_RATING + 1) for i in range(len(LETTER_ORDERING))],
        )
    )

    while not q.empty():
        name, xmas_ranges = q.get()

        logger.debug(f"Working with {name} + {[str(s) for s in xmas_ranges]}")

        if name == ACCEPT:
            old: int = answer
            answer += math.prod(len(letter_range) for letter_range in xmas_ranges)
            logger.info(f"Added {answer - old}")
            continue

        current_workflow: Workflow = name_to_workflow[name]
        resulting_work: List[Tuple[str, List[Range]]] = current_workflow.pass_through(
            xmas_ranges
        )

        logger.debug(
            f"Resulted in => {[(k, [str(s) for s in v]) for k, v in resulting_work]}"
        )

        for work in resulting_work:
            if work[0] != REJECT:
                q.put(work)

    return answer


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day19.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    name_to_workflow: Dict[str, Workflow] = {}

    for line in input_lines:
        if len(line) == 0:
            break
        brace_index: int = line.find("{")
        name: str = line[:brace_index]
        rules: List[str] = line[1 + brace_index : -1].split(",")
        name_to_workflow[name] = Workflow(name, rules)

    answer: int = run_ranges(name_to_workflow)
    logger.info(f"{answer=}")  # 117954800808317

    # that is, 117_954_800_808_317


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
