import ast
import inspect
from time import time
from _pytest import runner
runner.pytest_runtest_call_orig = runner.pytest_runtest_call


MEASURES = {}


def pytest_runtest_call(item):
    # Beautiful names
    #
    # test_filename = item.module.__file__
    # test_name = item.name
    # test_fullname = f"{test_filename}::{test_name}"

    # elapsed time
    start = time()
    runner.pytest_runtest_call_orig(item)
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
    green = {"green": True, "bold": True}
    red = {"red": True, "bold": True}
    bold = {"bold": True}
    writer = terminalreporter
    writer.section("test measures")
    for item, values in MEASURES.items():
        writer.line("\n" + item, **bold)
        for measure, value in values.items():
            red_conditions = any([
                measure == 'LOC' and value > 10,
                measure == 'ifs_used' and value >= 1,
                measure == 'for_used' and value >= 1,
                measure == 'while_used' and value >= 1,
                measure == 'elapsed_time' and value >= 5,
            ])

            if red_conditions:
                writer.line(f"{measure}: {value}", **red)
            else:
                writer.line(f"{measure}: {value}", **green)
