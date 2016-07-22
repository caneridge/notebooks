import pytest
from ..spaz import Spaz
import sys


def test_001(env_setup, capsys):
    import os

    # cleanup log
    logging_conf = 'spaz.logging.conf'
    if os.path.isfile(logging_conf):
        os.remove(logging_conf)

    logfile = 'spaz.testing.log'
    if os.path.isfile(logfile):
        os.remove(logfile)

    env_setup.string_to_file(fn=logging_conf, string=r"""
        # https://docs.python.org/2/library/logging.config.html#logging-config-dictschema
        version: 1
        disable_existing_loggers: False

        loggers:
            spaz:
                level: INFO
                handlers: [to_console, to_logfile]
                propagate: no

        root:
            level: INFO
            handlers: [to_console, to_logfile]

        handlers:
            to_console:
                class: logging.StreamHandler
                level: INFO
                formatter: console
                stream: ext://sys.stdout

            to_logfile:
                class: logging.handlers.RotatingFileHandler
                level: INFO
                formatter: datetime
                filename: {logfile}
                maxBytes: 1000
                backupCount: 2
                encoding: utf8

        formatters:
            datetime:
                format: "%(asctime)s %(name)s:%(levelname)s:%(message)s"
                datefmt: "%m/%d/%Y %H:%M"
            console:
                format: "%(name)s:%(levelname)s:%(message)s"
        """.format(logfile=logfile))

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

    sys.argv = 'spaz.py --role TEST1'.split(' ')
    spaz = Spaz()
    spaz.start_logging(logging_conf)
    spaz.start()

    assert spaz.options.environment == 'STE'
    assert spaz.options.config_file == ste_config_file
    assert spaz.configuration.role('TEST1').file_entry(file1).nickname == 'TEST1.1'
    assert env_setup.file_eq_string(file1, "\nSome text value1 other text\n")
