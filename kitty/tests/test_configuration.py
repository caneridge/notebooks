"""
Example imports in unit tests

https://github.com/cod3monk3y/PyImports
"""
import pytest
from ..configuration import Configuration


def test_001(env_setup, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        ROLE1:
        - file: fqfn1
          values:
          - key: key1
            value: value1
            comment: blaw
        """)

    assert Configuration.from_file(fn)
    out, err = capsys.readouterr()
    assert out == ""


def test_002(env_setup, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        ROLE1:
        - file: fqfn1
          values:
          - key: key1
            value: value1
            comment: blaw
        - file: fqfn2
          values:
          - key: key2
            value: value2
            comment: blaw
        """)

    assert Configuration.from_file(fn)
    out, err = capsys.readouterr()
    assert out == ""


def test_003(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        ROLE1:
        - file: fqfn1
          nickname: file1
          values:
          - key: key1
            value: value1
            comment: blaw
        ---
        ROLE1:
        - file: fqfn1
          nickname: file1
          values:
          - key: key1
            value: value1
            comment: blaw
        """)

    config = Configuration.from_file(fn)

    assert not config.ok
    assert memlog.last_log_line_is('ERROR: Role is not unique: ROLE1')

    out, err = capsys.readouterr()
    assert out == ""


def test_004(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        ROLE1:
        - file: fqfn1
          nickname: file1
          values:
          - key: key1
            value: value1
            comment: blaw
        ROLE2:
        - file: fqfn1
          nickname: file1
          values:
          - key: key1
            value: value1
            comment: blaw
        ---
        ROLE2:
        - file: fqfn1
          nickname: file1
          values:
          - key: key1
            value: value1
            comment: blaw
        """)

    config = Configuration.from_file(fn)

    assert not config.ok
    assert memlog.last_log_line_is('ERROR: Role is not unique: ROLE2')

    out, err = capsys.readouterr()
    assert out == ""


def test_005(env_setup, memlog, capsys):
    """
    Missing environment section
    """
    fn = env_setup.string_to_file(string=r"""
        ---
        schema-version: 1
        ---
        ROLE1:
        - file: fqfn1
          nickname: file1
          values:
          - key: key1
            value: value1
            comment: blaw
        """)

    config = Configuration.from_file(fn)

    assert not config.ok
    assert memlog.last_log_line_is("ERROR: Missing from header: 'environment: NAME'")

    out, err = capsys.readouterr()
    assert out == ""


def test_006(env_setup, memlog, capsys):
    """
    Missing schema-version section
    """
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        ---
        ROLE1:
        - file: fqfn1
          nickname: file1
          values:
          - key: key1
            value: value1
            comment: blaw
        """)

    config = Configuration.from_file(fn)

    assert not config.ok
    assert memlog.last_log_line_is("ERROR: Missing from header: 'schema-version: NUMBER'")

    out, err = capsys.readouterr()
    assert out == ""


def test_007(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 999
        ---
        ROLE1:
        - file: fqfn1
          values:
          - key: key1
            value: value1
            comment: blaw
        """)

    config = Configuration.from_file(fn)
    out, err = capsys.readouterr()
    assert out == ""

    assert memlog.last_log_line_is("ERROR: Schema-version 999 is not supported")
    assert not config.ok


def test_008(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        ROLE1:
        """)

    config = Configuration.from_file(fn)
    out, err = capsys.readouterr()
    assert out == ""

    assert memlog.last_log_line_is("ERROR: No files defined for role: ROLE1")
    assert not config.ok


def test_009(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        ROLE1:
        - xxxx: fqfn1
          values:
          - key: key1
            value: value1
            comment: blaw
        """)

    config = Configuration.from_file(fn)
    out, err = capsys.readouterr()
    assert out == ""

    assert memlog.last_log_line_is('ERROR: ROLE1: "file: NAME": missing')
    assert not config.ok


def test_010(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        ROLE1:
        - file: fqfn1
          values:
          - value: value1
            comment: blaw
        """)

    config = Configuration.from_file(fn)
    out, err = capsys.readouterr()
    assert out == ""

    assert memlog.last_log_line_is('ERROR: ROLE1.1: Missing entry: "key: NAME"')
    assert not config.ok


def test_011(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        ROLE1:
        - file: fqfn1
          values:
          - key: key1
            comment: blaw
        """)

    config = Configuration.from_file(fn)
    out, err = capsys.readouterr()
    assert out == ""

    assert memlog.last_log_line_is('ERROR: ROLE1.1: Missing entry: "value: VALUE"')
    assert not config.ok


def test_012(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        ROLE1:
        - file: fqfn1
          values:
          - key: key1
            value: value1
        """)

    config = Configuration.from_file(fn)
    out, err = capsys.readouterr()
    assert out == ""

    assert config.ok


def test_013(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        ROLE1:
        - file: fqfn1
        """)

    config = Configuration.from_file(fn)
    out, err = capsys.readouterr()
    assert out == ""

    assert config.ok

    assert memlog.last_log_line_is('ERROR: ROLE1: Missing section: "values:"')


def test_014(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        ROLE1:
        - file: fqfn1
          values:
        """)

    config = Configuration.from_file(fn)
    out, err = capsys.readouterr()
    assert out == ""

    assert config.ok

    assert memlog.last_log_line_is('ERROR: ROLE1: values: no values specified')


def test_015(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        ROLE1: value
        - file: fqfn1
          values:
        """)

    config = Configuration.from_file(fn)
    assert not config.ok

    assert memlog.contains('ERROR: Unable to parse YAML file')

    out, err = capsys.readouterr()
    assert out == ""




