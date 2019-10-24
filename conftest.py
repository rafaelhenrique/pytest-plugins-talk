import ast
import inspect
from time import time
from _pytest import runner


MEASURES = {}


def pytest_runtest_call(item):
    # Beautiful names
    #
    # test_filename = item.module.__file__
    # test_name = item.name
    # test_fullname = f"{test_filename}::{test_name}"

    # elapsed time
    start = time()
    runner.pytest_runtest_call(item)
    elapsed_time = time() - start

    # lines of code
    item_source_code = inspect.getsource(item._getobj())
    lines_of_code = len(item_source_code.split('\n')) - 1

    # check conditionals and loops
    root = ast.parse(item_source_code)
    ifs_used = len([node for node in ast.walk(root) if isinstance(node, ast.If)])
    for_used = len([node for node in ast.walk(root) if isinstance(node, ast.For)])
    while_used = len([node for node in ast.walk(root) if isinstance(node, ast.While)])

    # write measures
    MEASURES[item.name] = {
        "LOC": lines_of_code,
        "elapsed_time": elapsed_time,
        "ifs_used": ifs_used,
        "for_used": for_used,
        "while_used": while_used,
    }


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # command line options
    max_loc = config.getoption("--max-loc")
    max_if = config.getoption("--max-if")
    max_for = config.getoption("--max-for")
    max_while = config.getoption("--max-while")
    max_elapsed_time = config.getoption("--max-elapsed-time")

    # colors
    green = {"green": True, "bold": True}
    red = {"red": True, "bold": True}
    bold = {"bold": True}

    writer = terminalreporter
    writer.section("test measures")
    for item, values in MEASURES.items():
        writer.line("\n" + item, **bold)
        for measure, value in values.items():
            red_conditions = any([
                measure == 'LOC' and value >= max_loc,
                measure == 'ifs_used' and value >= max_if,
                measure == 'for_used' and value >= max_for,
                measure == 'while_used' and value >= max_while,
                measure == 'elapsed_time' and value >= max_elapsed_time,
            ])

            if red_conditions:
                writer.line(f"{measure}: {value}", **red)
            else:
                writer.line(f"{measure}: {value}", **green)


def pytest_addoption(parser):
    parser.addoption(
        "--max-loc", action="store", type=int, default=10,
        help="Max line of code per test"
    )
    parser.addoption(
        "--max-if", action="store", type=int, default=5,
        help="Max quantity of if instructions per test"
    )
    parser.addoption(
        "--max-for", action="store", type=int, default=10,
        help="Max quantity of for instructions per test"
    )
    parser.addoption(
        "--max-while", action="store", type=int, default=10,
        help="Max quantity of while instructions per test"
    )
    parser.addoption(
        "--max-elapsed-time", action="store", type=float, default=5,
        help="Max elapsed time per test"
    )
