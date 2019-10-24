import ast
import inspect
from time import time
from _pytest import runner


MEASURES = {}


def pytest_runtest_call(item):
    # Beautiful names of tests :)
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
    # markup = {"green": True, "bold": True}
    bold = {"bold": True}
    writer = terminalreporter
    writer.section("test measures")
    for item, values in MEASURES.items():
        writer.line("\n" + item, **bold)
        for measure, value in values.items():
            writer.line(f"{measure}: {value}")
