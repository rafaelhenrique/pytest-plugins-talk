# pytest-plugins-talk
My talk about pytest-plugins

# Install

Install requirements:

```
python3 -m venv .venv
source ~/.venv/bin/activate
pip install -r requirements.txt
```

Run pytest:

```
pytest .
```

# Branchs step-by-step

## [part01-elapsed-time](https://github.com/rafaelhenrique/pytest-plugins-talk/tree/part01-elapsed-time)

Add simple hooks pytest_runtest_call and pytest_terminal_summary to count elapsed time per test.

## [part02-loc](https://github.com/rafaelhenrique/pytest-plugins-talk/tree/part02-loc)

Add line counter on pytest_runtest_call.

## [part03-count-structures](https://github.com/rafaelhenrique/pytest-plugins-talk/tree/part03-count-structures)

Implement structures counter on pytest_runtest_call.

## [part04-colors](https://github.com/rafaelhenrique/pytest-plugins-talk/tree/part04-colors)

Use colors on output of pytest_terminal_summary.

## [part05-show-measures](https://github.com/rafaelhenrique/pytest-plugins-talk/tree/part05-show-measures)

Show formated measures on output of pytest_terminal_summary.

## [part06-pytest-addoption](https://github.com/rafaelhenrique/pytest-plugins-talk/tree/part06-pytest-addoption)

Implement hook pytest_addoption.
