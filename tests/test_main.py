import os
import sys
import pytest
from contextlib import contextmanager
from io import StringIO
from wordpath import main

@contextmanager
def capture_sys_output():
    capture_out, capture_err = StringIO(), StringIO()
    current_out, current_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = capture_out, capture_err
        yield capture_out, capture_err
    finally:
        sys.stdout, sys.stderr = current_out, current_err


help_text = """[-h] [-d DICTIONARY] [-w1 WORDONE] [-w2 WORDTWO]

This is a word ladder calculator program

optional arguments:
  -h, --help            show this help message and exit
  -d DICTIONARY, --dictionary DICTIONARY
                        Dictionary file for the script
  -w1 WORDONE, --word-one WORDONE
                        Starting word
  -w2 WORDTWO, --word-two WORDTWO
                        Destination word
"""

@pytest.mark.parametrize("args",
                         (['-h'], ['--help']))
def test_help(args):
    with capture_sys_output() as (stdout, stderr):
        with pytest.raises(SystemExit):
            main.parse_args(args)
    assert stderr.getvalue() == ''
    assert str(stdout.getvalue()).endswith(help_text)


@pytest.mark.parametrize("args, expected", [
    (['-d', "/some/random/file"], "/some/random/file"),
    (['--dictionary', "/some/random/file"], "/some/random/file"),
])
def tests_argument_passing_dict(args, expected):
    assert main.parse_args(args).dictionary == expected

@pytest.mark.parametrize("args, expected", [
    (['-w1', "start"], "start"),
    (['--word-one', "start"], "start"),
])
def tests_argument_passing_start(args, expected):
    assert main.parse_args(args).wordone == expected

@pytest.mark.parametrize("args, expected", [
    (['-w2', "destination"], "destination"),
    (['--word-two', "destination"], "destination"),
])
def tests_argument_passing_destination(args, expected):
    assert main.parse_args(args).wordtwo == expected
