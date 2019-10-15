import ast
import inspect
from time import time
from _pytest import runner
runner.pytest_runtest_call_orig = runner.pytest_runtest_call


MEASURES = {}


def pytest_runtest_call(item):
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
    writer = terminalreporter
    writer.section("test measures")
    for item, values in MEASURES.items():
        writer.line("\n" + item)
        writer.line(f"{values}")
