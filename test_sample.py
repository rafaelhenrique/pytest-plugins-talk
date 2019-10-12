from time import sleep


def slow_function():
    sleep(1)
    return 'done'


def fast_function():
    sleep(1)
    return 'done'


def test_slow_function():
    assert slow_function() == 'done'


def test_fast_function():
    assert fast_function() == 'done'


# This is a awful test ... please dont copy that!
def test_slow_function_with_conditionals():
    if slow_function() == 'done':
        assert True
    else:
        assert False


# This is a awful test ... please dont copy that!
def test_slow_function_with_loops():
    for i in range(1):
        pass

    i = 0
    while i > 1:
        i += 1

    assert slow_function() == 'done'
