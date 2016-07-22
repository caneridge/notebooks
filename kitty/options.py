"""
options.py

Manages options which configure running of the script. These are intended to be
set by administrators as a site wide policy.
"""
from yamlutil import YamlUtil
import logging


class Options:
    SCHEMA_VERSION = 1
    SUPPORTED_VERSIONS = [1]

    def __init__(self):
        self.filename = None

        self.environment = None
        self.schema_version = None
        self.config_file = None
        self.ok = True

    def parse_key_value(self, key, dictionary, default_value, error_message):
        if not dictionary:
            self.ok = False
            logging.getLogger(__name__).error(error_message)
        elif key in dictionary:
            return dictionary[key]
        elif error_message:
            self.ok = False
            logging.getLogger(__name__).error(error_message)
        return default_value

    @classmethod
    def from_file(cls, filename):
        self = cls()

        self.filename = filename

        yaml = YamlUtil.open_sections(self.filename)
        self.ok = yaml.ok

        if self.ok:
            sections = yaml.sections
            header = sections.pop(0)
            self.environment = self.parse_key_value('environment', header, None, "Missing from options header: environment: NAME")
            self.schema_version = self.parse_key_value('schema-version', header, None, "Missing from options header: schema-version: NUMBER")

            if self.schema_version and not self.schema_version_supported():
                self.ok = False
                logging.getLogger(__name__).error("Schema-version {n} is not supported. Update options file".format(n=self.schema_version))
            else:
                if not 1 == len(sections):
                    self.ok = False
                    logging.getLogger(__name__).error("Expected one section following header")
                else:
                    section = sections[0]

                    self.config_file = self.parse_key_value('config-file', section, None, 'Missing entry: "config-file:"')

        return self

    def schema_version_supported(self):
        return self.schema_version in self.__class__.SUPPORTED_VERSIONS
