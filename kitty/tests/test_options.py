"""
test_options.py
"""
from ..options import Options


def test_001(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        # Settings unique to environment
        config-file: ste.yaml
        """)

    options = Options.from_file(fn)

    memlog.print_lines()
    out, err = capsys.readouterr()
    assert out == ""

    assert options.ok == True
    assert options.environment == 'STE'
    assert options.config_file == 'ste.yaml'


def test_002(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        schema-version: 1
        ---
        # Settings unique to environment
        config-file: ste.yaml
        """)

    options = Options.from_file(fn)

    memlog.last_log_line_is("ERROR: Missing from options header: environment: NAME")
    out, err = capsys.readouterr()
    assert out == ""
    assert not options.ok


def test_003(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        ---
        # Settings unique to environment
        config-file: ste.yaml
        """)

    options = Options.from_file(fn)

    assert not options.ok
    out, err = capsys.readouterr()
    assert out == ""


def test_004(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 999
        ---
        # Settings unique to environment
        config-file: ste.yaml
        """)

    options = Options.from_file(fn)

    memlog.last_log_line_is("ERROR: Schema-version 999 is not supported. Update options file")
    out, err = capsys.readouterr()
    assert out == ""
    assert not options.ok


def test_005(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        """)

    options = Options.from_file(fn)

    memlog.last_log_line_is("ERROR: Expected one section following header")
    out, err = capsys.readouterr()
    assert out == ""
    assert not options.ok


def test_006(env_setup, memlog, capsys):
    fn = env_setup.string_to_file(string=r"""
        ---
        environment: STE
        schema-version: 1
        ---
        # Settings unique to environment
        """)

    options = Options.from_file(fn)

    memlog.last_log_line_is('ERROR: Missing entry: "config-file:"')
    out, err = capsys.readouterr()
    assert out == ""
    assert not options.ok
