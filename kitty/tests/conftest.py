import re
import os
import shutil
import pytest
from textwrap import dedent


@pytest.fixture
def env_setup(request):
    """
    Creates temp files in a temp directory.

    fn = string_to_file(string)
    ---------------------------

    writes string to temp filename

    string: String to write. Removes leading whitespace on string for idnedted tripple quoted strings.
    fn: filename created
    """
    setup = TempFileFixture()
    setup.create_fixture()
    request.addfinalizer(setup.destroy_fixture)
    return setup


class TempFileFixture:
    TEST_TEMP_DIR = 'test_temp'
    TEST_TEMP_FN = 'test.yaml'
    NUM=1

    def __init__(self):
        # print('\n--- Setting up ---')
        pass

    @classmethod
    def create_fixture(cls):
        # print('\n--- up ---')
        if not os.path.exists(cls.TEST_TEMP_DIR):
            os.makedirs(cls.TEST_TEMP_DIR)

    @classmethod
    def destroy_fixture(cls):
        # print('\n--- down ---')
        if os.path.exists(cls.TEST_TEMP_DIR):
            shutil.rmtree(cls.TEST_TEMP_DIR)

    @classmethod
    def fn(cls):
        filename = "{dir}/temp{n}.file".format(dir=cls.TEST_TEMP_DIR, n=cls.NUM)
        cls.NUM += 1
        return filename

    @classmethod
    def string_to_file(cls, fn=None, string=None):
        if fn:
            filename = fn
        else:
            filename = cls.fn()

        if string:
            # print('\n--- Filename {f}'.format(f=filename))
            with open(filename, mode='w') as to_file:
                to_file.write(dedent(string))
        return filename

    @classmethod
    def file_eq_string(cls, fn, string):
        with open(fn, mode='r') as fh:
            fn_string = fh.read()

        if fn_string != string:
            print ""
            print "---- file:"
            print fn_string
            print "---- string:"
            print string
            print "----"
            return False

        return True


@pytest.fixture
def hello_setup(request):
    fixture = PlayFixture()
    fixture.create_fixture()
    request.addfinalizer(fixture.destroy_fixture)
    return fixture


class PlayFixture:
    def __init__(self):
        pass

    @classmethod
    def create_fixture(cls):
        pass

    @classmethod
    def destroy_fixture(cls):
        pass

    @classmethod
    def output(cls):
        print "hello"


@pytest.fixture
def world_setup(request):
    fixture = WorldFixture(hello_setup(request))
    fixture.create_fixture()
    request.addfinalizer(fixture.destroy_fixture)
    return fixture


class WorldFixture:
    def __init__(self, hello):
        self.hello = hello
        pass

    @classmethod
    def create_fixture(cls):
        pass

    @classmethod
    def destroy_fixture(cls):
        pass

    def output(self):
        self.hello.output
        print "world"


import io
import logging


@pytest.fixture(scope='module')
def memlog(request):
    fixture = MemLog()
    fixture.create_fixture()
    request.addfinalizer(fixture.destroy_fixture)
    return fixture


class MemLog:
    """
    Capture logging messages in memory.

    Ability to return the last log line read so we can assert against the most recint log message.
    """
    def __init__(self):
        self.memlog = None
        self.log_lines = []

    def create_fixture(self):
        # create logger
        logger = logging.getLogger('spaz')
        logger.setLevel(logging.INFO)

        # create console handler with a higher log level
        self.memlog = io.BytesIO()
        stream = logging.StreamHandler(self.memlog)
        #stream.setLevel(logging.INFO)

        # create formatter and add it to the handlers
        stream.setFormatter(
            logging.Formatter('%(levelname)s: %(message)s')
        )

        # add the handlers to the logger
        logger.addHandler(stream)

    def destroy_fixture(self):
        logging.shutdown()

    def get_log_messages(self):
        lines = self.memlog.getvalue().split("\n")
        for line in lines:
            # Don't post blank lines
            # memlog always has a blank line as the last entry
            if line and not line == '':
                self.log_lines.append(line)

    def last_log_line_is(self, string):
        self.get_log_messages()
        if len(self.log_lines) > 0:
            line = self.log_lines[-1].rstrip("\n")
            if line == string:
                return True
            else:
                print
                print("last_log_line: {a}".format(a=line))
                print("  compared to: {b}".format(b=string))
                return False
        return None == string

    def print_lines(self):
        self.get_log_messages()
        for line in self.log_lines:
            print(line)

    def contains(self, substring):
        r = re.compile(".*{s}.*".format(s=substring))

        self.get_log_messages()
        for line in self.log_lines:
            if r.match(line):
                return True
        return False

    def next_line(self):
        if len(self.log_lines) > 0:
            return self.log_lines.pop(0)
        return None

    def next_line_contains(self, substring):
        self.get_log_messages()
        line = self.next_line()
        if line:
            if re.compile("^.*{s}.*".format(s=substring)).match(line):
                return True
            else:
                print
                print("next_log_line: {a}".format(a=line))
                print("  compared to: {b}".format(b=substring))
        else:
            print
            print("next_log_line: None")
            print("  compared to: {b}".format(b=substring))

        return False
