"""
File
    configuration.py

"""
from yamlutil import YamlUtil
import logging


class ValueEntry:
    def __init__(self, key, value, comment):
        self.key = key
        self.value = value
        self.comment = comment

    def __str__(self):
        return "\n".join([
            '  - key: {x}'.format(x=self.key),
            '    value: {x}'.format(x=self.value),
            '    comment: {x}'.format(x=self.comment)
        ])


class FileEntry:
    templates = 0

    def __init__(self):
        self.name = None
        self.nickname = None
        self.values = {}
        self.value_entries = []
        self.ok = True

    @classmethod
    def from_struct(cls, role, struct, nickname):
        """
        Create file entry from read in yaml
        """

        self = FileEntry()

        self.name = self.parse_key_value('file', struct, None, '{role}: "file: NAME": missing'.format(role=role))
        self.nickname = nickname

        if 'values' in struct:
            # Array of hashes [{'key': KEY, 'value': VALUE, 'comment': COMMENT}...]
            if not struct['values']:
                logging.getLogger(__name__).error('{role}: values: no values specified'.format(role=role))
                pass
            else:
                for value_entry in struct['values']:
                    key = self.parse_key_value('key', value_entry, None, '{x}: Missing entry: "key: NAME"'.format(x=self.nickname))
                    value = self.parse_key_value('value', value_entry, 'UNDEFINED', '{x}: Missing entry: "value: VALUE"'.format(x=self.nickname))
                    comment = self.parse_key_value('comment', value_entry, None, None)
                    if key:
                        self.values[key] = value
                        self.value_entries.append(ValueEntry(key, value, comment))
        else:
            logging.getLogger(__name__).error('{role}: Missing section: "values:"'.format(role=role))
        return self

    def parse_key_value(self, key, dictionary, default_value, error_message):
        if key in dictionary:
            return dictionary[key]
        elif error_message:
            logging.getLogger(__name__).error(error_message)
            self.ok = False
        return default_value

    def __str__(self):
        lines = [
            '- file: {filename}:'.format(filename=self.name),
            '  values:'
        ]
        for value_entry in self.value_entries:
            lines.append(str(value_entry))
        return "\n".join(lines)


class Role:
    def __init__(self):
        self.name = None
        self.file_entries = []
        self.ok = True

    @classmethod
    def from_struct(cls, role_name, file_entries):
        """
        Construct new role from read in yaml

        struct:
           [{'values': {'key1': 'value1'}, 'file': 'fqfn1'}, ...]
        """

        self = cls()
        self.name = role_name

        n = 0
        for file_entry in file_entries:
            n += 1
            file_object = FileEntry.from_struct(role_name, file_entry, "{role}.{n}".format(role=role_name, n=n))
            self.file_entries.append(file_object)
            if not file_object.ok:
                self.ok = False

        return self

    def file_entry(self, fn):
        """
        Return file entry given filename
        """
        for entry in self.file_entries:
            if entry.name == fn:
                return entry
        return None

    def __str__(self):
        lines = [
            '---',
            '{role}:'.format(role=self.name)
        ]

        for file_entry in self.file_entries:
            lines.append(str(file_entry))
        return "\n".join(lines)


class Configuration:
    """
    Given a configuration file, create objects that represent it.
    """
    SCHEMA_VERSION = 1
    SUPPORTED_VERSIONS = [1]

    def __init__(self):
        self.filename = None
        self.data = {}
        self.environment = None
        self.schema_version = None
        self.ok = True

        # Roles defined in configuration
        self.roles = []

    @classmethod
    def from_file(cls, filename):
        self = cls()

        self.filename = filename

        yaml = YamlUtil.open_sections(self.filename)
        self.ok = yaml.ok

        if self.ok:
            try:
                sections = yaml.sections

                header = sections.pop(0)
                self.environment = self.parse_key_value('environment', header, None, "Missing from header: 'environment: NAME'")
                self.schema_version = self.parse_key_value('schema-version', header, None, "Missing from header: 'schema-version: NUMBER'")

                if self.schema_version and not self.schema_version_supported():
                    logging.getLogger(__name__).error("Schema-version {n} is not supported".format(n=self.schema_version))
                    self.ok = False

                for section in sections:
                    for role_name in section:
                        if self.role(role_name):
                            logging.getLogger(__name__).error("Role is not unique: {name}".format(name=role_name))
                            self.ok = False
                        elif not section[role_name]:
                            logging.getLogger(__name__).error("No files defined for role: {name}".format(name=role_name))
                            self.ok = False
                        else:
                            role = Role.from_struct(role_name, section[role_name])
                            self.roles.append(role)
                            if not role.ok:
                                self.ok = False
            except Exception as e:
                self.ok = False
                logging.getLogger(__name__).error("Incorrect configuration file syntax, unable to load configuration".format(name=role_name))

        return self

    def parse_key_value(self, key, dictionary, default_value, error_message):
        if key in dictionary:
            return dictionary[key]
        elif error_message:
            logging.getLogger(__name__).error(error_message)
            self.ok = False
        return default_value

    def schema_version_supported(self):
        return self.schema_version in self.__class__.SUPPORTED_VERSIONS

    def role(self, name):
        for role in self.roles:
            if role.name == name:
                return role
        return None

    def __str__(self):
        lines = [
            '---',
            'environment: {name}'.format(name=self.environment),
            'schema_version: {name}'.format(name=self.schema_version)
        ]
        for role in self.roles:
            lines.append(str(role))
        return "\n".join(lines)
