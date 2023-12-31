"""
rx comes from Conjunction(rs)
Want low pulse on rx

rs is Conjunction of
&bt, &dl, &fr, &rv -> rs -> rx
(inputs to rs, rs, and outputs of rs)
Want high pulses from bt, dl, fr, rv

    bt is Conjunction of
    &mj -> bt -> rs

    dl is Conjunction of
    &qs -> dl -> rs

    fr is Conjunction of
    &rd -> fr -> rs

    rv is Conjunction of
    &cs -> rv -> rs

-> want low pulses from mj, qs, rd, cs

    mj is Conjunction of
    %qm, %js, %pc, %pz, %lr, %xn, %mf, %mr -> &mj -> ...
    8, 2048, 512, 2, 2, 16, 128, 1024
    -> 3739 (sum - 1)

    qs is Conjunction of
    %qc, %hh, %tp, %xq, %ks, %hf, %nd -> &qs
    32, 2, 512, 256, 1024, 128, 2048
    -> 4001

    rd is Conjunction of
    %mb, %cv, %rh, %bz, %xs, %kl, %hk, %lf, %sv -> &rd
    512, 2048, 2, 32, 1024, 256, 64, 2, 4
    -> 3943

    cs is Conjunction of
    %gk, %mn, %md, %cj, %zs, %jb, %bp, %bb, %zm -> &cs
    4, 1024, 2048, 128, 512, 64, 2, 8, 32
    -> 3821

    LCM(3739, 4001, 3943, 3821) = 225386464601017

    That is, 225,386,464,601,017
"""

import time
from queue import Queue
from typing import cast, Dict, List, Set

from loguru import logger

DEBUG: bool = False

LOW_PULSE: int = 0
HIGH_PULSE: int = 1


class CommunicationModule:
    def __init__(self, name: str, output_module_names: List[str]) -> None:
        self.name: str = name
        self.output_module_names: List[str] = output_module_names

    def process_signal(self, pulse: int, from_module_name: str) -> Dict[str, int]:
        output_signals: Dict[str, int] = {}
        for output_module_name in self.output_module_names:
            output_signals[output_module_name] = pulse

        #  logger.debug(
        #  f"Hey CommunicationModule process_signal wants to return {output_signals}"
        #  )

        return output_signals

    def get_state_as_str(self) -> None:
        return self.name


class FlipFlopModule(CommunicationModule):
    def __init__(self, name: str, output_module_names: List[str]) -> None:
        super().__init__(name, output_module_names)
        self.switch_status_on = False

    def process_signal(self, pulse: int, from_module_name: str) -> Dict[str, int]:
        if pulse == LOW_PULSE:
            self.switch_status_on = not self.switch_status_on
            return super().process_signal(
                HIGH_PULSE if self.switch_status_on else LOW_PULSE, self.name
            )

        return {}

    def get_state_as_str(self) -> None:
        return f'{self.switch_status_on}'


class ConjunctionModule(CommunicationModule):
    def __init__(self, name: str, output_module_names: List[str]) -> None:
        super().__init__(name, output_module_names)
        self.input_history: Dict[str, int] = {}

    def add_input_connector(self, name) -> None:
        self.input_history[name] = LOW_PULSE

    def process_signal(self, pulse: int, from_module_name: str) -> Dict[str, int]:
        #  logger.warning(f'ConjunctionModule process_signal on {pulse=} from {from_module_name}: {self.input_history=}')
        self.input_history[from_module_name] = pulse
        all_inputs_high: bool = all(
            p == HIGH_PULSE for p in self.input_history.values()
        )
        return super().process_signal(
            LOW_PULSE if all_inputs_high else HIGH_PULSE, self.name
        )

    def get_state_as_str(self) -> None:
        input_states: int = 0
        for index, k in enumerate(sorted(self.input_history.keys())):
            v = self.input_history[k]
            if v == HIGH_PULSE:
                input_states += (2 ** index)

        return f'{input_states:{len(self.input_history)}b}'


class MachineNetwork:
    def __init__(self) -> None:
        self.name_to_modules: Dict[str, CommunicationModule] = {}
        self.name_to_queue: Dict[str, Queue] = {}
        self.num_low_pulses: int = 0
        self.num_high_pulses: int = 0
        self.rx_got_low_pulse: bool = False
        self.num_times_pressed: int = 0

        # history_states[module_name][module_state] -> which iteration of button press
        self.history_states: Dict[str, Dict[str, int]] = dict()

    def add_module(self, module1: CommunicationModule) -> None:
        logger.debug(f"Adding module {module1.name} with {module1.output_module_names}")
        self.name_to_modules[module1.name] = module1
        self.name_to_queue[module1.name] = Queue()
        self.history_states[module1.name] = dict()

    def press_button(self) -> None:
        self.num_times_pressed += 1
        if self.num_times_pressed % 1000 == 0:
            logger.info(f'Pressed button {self.num_times_pressed} times')
        if "button" not in self.name_to_modules:
            self.add_module(CommunicationModule("button", ["broadcaster"]))

        button_output: Dict[str, int] = self.name_to_modules["button"].process_signal(
            LOW_PULSE, "button"
        )
        for output_name, output_signal in button_output.items():
            self.name_to_queue[output_name].put((output_signal, "button"))

        #  logger.info("Pressed the button!")
        self.handle_all_signals()

    def handle_all_signals(self) -> None:
        still_need_to_process: bool = True
        while still_need_to_process:
            next_step_queues: Dict[str, Queue] = {
                name: Queue() for name in self.name_to_queue
            }

            still_need_to_process = False
            # process all current signals in queue
            for name, q in self.name_to_queue.items():
                if q.empty():
                    continue
                #  logger.debug(f"Hey look queue[{name}] not empty")
                still_need_to_process = True
                relevant_module: CommunicationModule = self.name_to_modules[name]

                while not q.empty():
                    pulse, from_name = q.get()
                    if pulse == LOW_PULSE:
                        self.num_low_pulses += 1
                    else:
                        self.num_high_pulses += 1

                    output: Dict[str, int] = relevant_module.process_signal(
                        pulse, from_name
                    )
                    # output further signals to separate queue system
                    for output_name, output_signal in output.items():
                        if output_name == 'rx' and output_signal == LOW_PULSE:
                            self.rx_got_low_pulse = True
                        next_step_queues[output_name].put((output_signal, name))

            # now that all of current queue is empty, transfer next_step_queues to current queues to be processed
            self.name_to_queue = next_step_queues

        # button press ended... check state
        for name, my_module in self.name_to_modules.items():
            module_state: str = my_module.get_state_as_str()

            if module_state in self.history_states[name]:
                #  logger.warning(f'Module {name} repeated at {self.history_states[name][module_state]} and {self.num_times_pressed}')
                ...
            else:
                self.history_states[name][module_state] = self.num_times_pressed

    def print_network_history(self) -> None:
        for name in self.history_states:
            logger.info(f'Module {name} has iterations {sorted(self.history_states[name].values())}')


def main() -> None:
    input_file: str = "inputs/dummy.txt" if DEBUG else "inputs/day20.txt"

    input_lines: List[str] = []
    with open(input_file, "r") as fd:
        input_lines = [line.strip() for line in fd.readlines()]

    network: MachineNetwork = MachineNetwork()
    conjuction_names: Set[str] = set()
    output_names: Set[str] = set()

    for line in input_lines:
        parts: List[str] = [s for s in line.split(" ") if s != "->"]
        # remove trailing comma
        relevant_names: List[str] = [s[:-1] if s[-1] == "," else s for s in parts]

        if relevant_names[0][0] == "%":
            network.add_module(
                FlipFlopModule(relevant_names[0][1:], relevant_names[1:])
            )
        elif relevant_names[0][0] == "&":
            network.add_module(
                ConjunctionModule(relevant_names[0][1:], relevant_names[1:])
            )
            conjuction_names.add(relevant_names[0][1:])
        else:
            network.add_module(
                CommunicationModule(relevant_names[0], relevant_names[1:])
            )

        for output_name in relevant_names[1:]:
            output_names.add(output_name)

    #  network.add_module(CommunicationModule("output", []))
    for output_name in output_names:
        if output_name not in network.name_to_modules:
            logger.warning(f"Adding module {output_name}")
            network.add_module(CommunicationModule(output_name, []))

    # add input connectors to conjunction modules
    for name, my_module in network.name_to_modules.items():
        for output_module_name in my_module.output_module_names:
            if output_module_name in conjuction_names:
                #  logger.debug(f'Hmmm module {name} has {output_module_name=}')
                output_module: CommunicationModule = network.name_to_modules[
                    output_module_name
                ]
                output_module = cast(ConjunctionModule, output_module)
                output_module.add_input_connector(name)

    while not network.rx_got_low_pulse and network.num_times_pressed < 10000:
        network.press_button()

    network.print_network_history()

    answer: int = network.num_times_pressed
    logger.info(f"{answer=}")  # 834323022

    breakpoint()


if __name__ == "__main__":
    start_time = time.time()
    main()

    time_took: float = time.time() - start_time
    seconds_took: int = int(time_took)
    logger.info(f"Took {seconds_took}s {1000 * (time_took - seconds_took):.3f}ms")
