import pytest
from ..render import Render
from textwrap import dedent
import re


def test_001(capsys):
    render = Render.from_string(dedent(r"""
        blaw blaw:${VAR1}:blaw blaw
        """), {'VAR1': 'value-one'})

    string = render.rendered_text

    assert string == "\nblaw blaw:value-one:blaw blaw\n"
    out, err = capsys.readouterr()
    assert out == ""


def test_002(capsys):
    values = {'VAR1': 'value-one', 'VAR2': 'value-two'}
    render = Render.from_string(dedent(r"""
        blaw blaw:${VAR1}:blaw blaw
        ---- ----:${VAR2}:---- ----
        """), values)

    string = render.rendered_text

    assert string == "\nblaw blaw:value-one:blaw blaw\n---- ----:value-two:---- ----\n"
    out, err = capsys.readouterr()
    assert out == ""


def test_003(capsys, memlog):
    values = {'VAR1': 'value-one', 'VAR2': 'value-two'}

    render = Render.from_string(dedent(r"""
        blaw blaw:${VAR1:blaw blaw
        """), values)

    assert not render.ok
    memlog.print_lines()
    assert memlog.next_line_contains("ERROR: Syntax error in template")
    assert memlog.next_line_contains("ERROR: Syntax error info: Expected:")


def test_004(capsys, memlog):
    values = {'VAR1': 'value-one', 'VAR2': 'value-two'}
    render = Render.from_file('file_does_not_exist.txt', values)

    assert not render.ok
    assert memlog.next_line_contains("ERROR: Unable to open file: file_does_not_exist.txt")


def test_005(memlog):
    """
    Unexpanded variable in template
    """
    values = {'VAR3': 'value-one'}
    render = Render.from_string(dedent(r"""
        blaw blaw:${VAR3}:blaw blaw
        ---- ----:${VAR4}:---- ----
        """), values)

    assert not render.ok
    assert memlog.next_line_contains("ERROR: No value for key: VAR4")
