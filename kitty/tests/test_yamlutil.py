import pytest
from ..yamlutil import YamlUtil


def test_001(env_setup, capsys, memlog):
    fn = env_setup.string_to_file(string=r"""
        ---
        ROLE1:
        - file: fqfn1
          values:
          - key: key1
            value: value1
            comment: blaw
        """)

    yaml = YamlUtil.open_sections(fn)
    assert yaml.sections[0]['ROLE1'][0]['file'] == 'fqfn1'
    assert yaml.sections[0]['ROLE1'][0]['values'][0]['key'] == 'key1'
    assert yaml.sections[0]['ROLE1'][0]['values'][0]['value'] == 'value1'
    assert yaml.sections[0]['ROLE1'][0]['values'][0]['comment'] == 'blaw'


def test_002(env_setup, memlog):
    fn = env_setup.string_to_file(string=r"""
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

    yaml = YamlUtil.open_sections(fn)
    assert yaml.sections[0]['ROLE1'][0]['file'] == 'fqfn1'
    assert yaml.sections[0]['ROLE1'][0]['values'][0]['key'] == 'key1'
    assert yaml.sections[0]['ROLE1'][0]['values'][0]['value'] == 'value1'
    assert yaml.sections[0]['ROLE1'][0]['values'][0]['comment'] == 'blaw'

    assert yaml.sections[0]['ROLE1'][1]['file'] == 'fqfn2'
    assert yaml.sections[0]['ROLE1'][1]['values'][0]['key'] == 'key2'
    assert yaml.sections[0]['ROLE1'][1]['values'][0]['value'] == 'value2'
    assert yaml.sections[0]['ROLE1'][1]['values'][0]['comment'] == 'blaw'


def test_003(env_setup, memlog):

    fn = env_setup.string_to_file(string=r"""
        ---
        ROLE1
        - file: fqfn1:
          nickname: file1
          values:
            key1: value1
        """)

    assert not YamlUtil.open_sections(fn).ok

    assert memlog.next_line_contains("ERROR: Unable to parse YAML file:")


def test_004(env_setup, memlog, capsys):

    fn = env_setup.string_to_file(string=r"""
        ---
        ROLE1: Boomb
        - file: fqfn1:
          nickname: file1
          values:
            key1: value1
        """)

    assert not YamlUtil.open_sections(fn).ok

    assert memlog.next_line_contains("ERROR: Unable to parse YAML file:")
    assert memlog.next_line_contains("ERROR: YAML error info: while parsing a block mapping")

