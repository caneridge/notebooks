import pytest
from ..spaz import Spaz
import sys


def test_001(capsys):
    sys.argv = 'spaz.py --role TEST1 --validate --dry-run'.split(' ')
    spaz = Spaz()
    spaz.parse_args()
    spaz.show_args()

    out, err = capsys.readouterr()
    assert out == "--role TEST1\n--validate\n--dry-run\n"


def test_002(env_setup, memlog, capsys):
    """
    --validate does not change any files
    """
    file1 = env_setup.string_to_file(string=r"""
        Some text ${key1} other text
        """)

    ste_config_file = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        TEST1:
        - file: {file1}
          values:
          - key: key1
            value: value1
            comment: blaw
          - key: key2
            value: value2
            comment: blaw blaw
        """.format(file1=file1))

    env_setup.string_to_file(fn='spaz.conf', string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        # Settings unique to environment
        config-file: {ste_config_file}
        """.format(ste_config_file=ste_config_file))

    sys.argv = 'spaz.py --role TEST1 --validate'.split(' ')
    spaz = Spaz()

    with pytest.raises(SystemExit):
        spaz.start()

    assert memlog.contains('INFO: Validated: OK')

    assert spaz.options.environment == 'STE'
    assert spaz.options.config_file == ste_config_file
    assert spaz.configuration.role('TEST1').file_entry(file1).nickname == 'TEST1.1'
    assert env_setup.file_eq_string(file1, "\nSome text ${key1} other text\n")


def test_003(env_setup, memlog, capsys):
    """
    --dry-run
    no errors
    """
    file1 = env_setup.string_to_file(string=r"""
        Some text ${key1} other text
        """)

    ste_config_file = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        TEST1:
        - file: {file1}
          values:
          - key: key1
            value: value1
            comment: blaw
          - key: key2
            value: value2
            comment: blaw blaw
        """.format(file1=file1))

    out, err = capsys.readouterr()
    assert out == ""

    env_setup.string_to_file(fn='spaz.conf', string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        # Settings unique to environment
        config-file: {ste_config_file}
        """.format(ste_config_file=ste_config_file))

    sys.argv = 'spaz.py --role TEST1 --dry-run'.split(' ')
    spaz = Spaz()

    with pytest.raises(SystemExit):
        spaz.start()

    memlog.print_lines()

    assert memlog.contains('INFO: Dry run: OK')
    assert spaz.options.environment == 'STE'
    assert spaz.options.config_file == ste_config_file
    assert spaz.configuration.role('TEST1').file_entry(file1).nickname == 'TEST1.1'
    assert env_setup.file_eq_string(file1, "\nSome text ${key1} other text\n")


def test_004(env_setup, memlog, capsys):
    """
    --dry-run
    no errors
    """
    file1 = env_setup.string_to_file(string=r"""
        Some text ${key1} ${missing_key} other text
        """)

    ste_config_file = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        TEST1:
        - file: {file1}
          values:
          - key: key1
            value: value1
            comment: blaw
        """.format(file1=file1))

    out, err = capsys.readouterr()
    assert out == ""

    env_setup.string_to_file(fn='spaz.conf', string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        # Settings unique to environment
        config-file: {ste_config_file}
        """.format(ste_config_file=ste_config_file))

    sys.argv = 'spaz.py --role TEST1 --dry-run'.split(' ')
    spaz = Spaz()

    with pytest.raises(SystemExit):
        spaz.start()

    memlog.print_lines()

    assert memlog.contains('ERROR: No value for key: missing_key')
    assert spaz.options.environment == 'STE'
    assert spaz.options.config_file == ste_config_file
    assert spaz.configuration.role('TEST1').file_entry(file1).nickname == 'TEST1.1'
    assert env_setup.file_eq_string(file1, "\nSome text ${key1} ${missing_key} other text\n")
