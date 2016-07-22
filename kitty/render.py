import re
import sys

from mako.template import Template
from mako.exceptions import SyntaxException, CompileException
import logging


class Render:
    # When True, don't write files, just be sure we can read them
    verify = False

    def __init__(self):
        # Source template text
        self.template = None

        # Hash to supply values
        self.values = {}

        # String with mako syntax
        self.mako_template = None

        # Results of rendering template
        self.rendered_text = None

        # Resulting undefined mako_template variable names
        self.undefined_names = {}

        # File to write to
        self.fn = None

        # Need the ability to show errors but not exit
        self.ok = True

    @classmethod
    def from_string(cls, template_string, values):
        """
        New instance from template string.
        """
        self = cls()

        self.template = template_string
        self.values = values

        if self.open_template():
            self.to_string()

        return self

    @classmethod
    def from_file(cls, fn, values):
        """
        New instance from template filename.
        """
        self = cls()
        self.fn = fn
        self.values = values

        try:
            fh = open(fn)
            self.template = fh.read()
            fh.close()
        except Exception as e:
            self.ok = False
            logging.getLogger(__name__).error("Unable to open file: {fn}".format(fn=fn))
        else:
            if self.open_template():
                self.to_string()

        return self

    @classmethod
    def from_file_entry(cls, file_entry):
        self = cls.from_file(file_entry.name, file_entry.values)

        return self

    def open_template(self):
        self.mako_template = None

        if not self.ok:
            return

        try:
            self.mako_template = Template(self.template, strict_undefined=True)
        except SyntaxException as e:
            self.ok = False
            logging.getLogger(__name__).error("Syntax error in template")
            logging.getLogger(__name__).error('Syntax error info: {msg}'.format(msg=str(e)))
        except CompileException as e:
            self.ok = False
            logging.getLogger(__name__).error("Unable to compile template")
            logging.getLogger(__name__).error('Error info: {msg}'.format(msg=str(e)))
        except Exception as e:
            self.ok = False
            logging.getLogger(__name__).error("Unexpected error: {msg}".format(msg=sys.exc_info()[0]))
            logging.getLogger(__name__).error('Error info: {msg}'.format(msg=str(e)))

        return self.mako_template

    def to_string(self):
        self.rendered_text = None
        self.undefined_names = {}

        if not self.ok:
            return

        # Show up to N errors, and ensure we don't loop forever
        for i in range(20):
            try:
                replace_values = self.values.copy()
                replace_values.update(self.undefined_names)
                self.rendered_text = self.mako_template.render(**replace_values)
            except NameError as e:
                self.ok = False
                m = re.compile(r"'(?P<name>\S+)' is not defined")
                if m.match(str(e)):
                    # Define the value with a dummy value so we can find the next undefined name
                    undefined_name = m.match(str(e)).group('name')
                    self.undefined_names[undefined_name] = '[UNDEFINED:{name}]'.format(name=undefined_name)
                    logging.getLogger(__name__).error("No value for key: {key}".format(key=undefined_name))
            except Exception as e:
                self.ok = False
                logging.getLogger(__name__).error("Exception: {_class}".format(_class=e.__class__.__name__))
                logging.getLogger(__name__).error(str(e))
                break
            else:
                break

    def to_file(self):
        # Don't write files when verifying
        if self.__class__.verify or not self.ok:
            return

        try:
            fh = open(self.fn, mode='w')
        except Exception as e:
            self.ok = False
            logging.getLogger(__name__).error("{_class}: {_message}: {_file}"
                .format(_class=e.__class__.__name__, _message="Unable to write to file", _file=self.fn))
            print(str(e))
        else:
            fh.write(self.rendered_text)
            fh.close()

    def show_undefined_names(self):        
        print("Undefined:")
        for key in self.undefined_names:
            print(key)
