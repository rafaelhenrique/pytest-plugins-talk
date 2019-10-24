from time import time
from _pytest import runner


MEASURES = {}


def pytest_runtest_call(item):
    # elapsed time
    start = time()
    runner.pytest_runtest_call(item)
    elapsed_time = time() - start

    # write measures
    MEASURES[item.name] = {
        "elapsed_time": elapsed_time,
    }


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    writer = terminalreporter
    writer.section("test measures")
    for item, values in MEASURES.items():
        writer.line("\n" + item)
        writer.line(f"{values}")
