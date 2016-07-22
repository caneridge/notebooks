import yaml
import logging


class YamlUtil:

    def __init__(self):
        self.fn = None
        self.sections = None
        self.ok = True

    @classmethod
    def open_sections(cls, filename):
        self = cls()
        self.fn = filename
        self.sections = []

        try:
            fh = open(self.fn)
        except Exception as e:
            self.ok = False
            logging.getLogger(__name__).error("Unable to open file: {_file}".format(_file=self.fn))
        else:
            try:
                for section in yaml.load_all(fh):
                    self.sections.append(section)
            except Exception as e:
                self.ok = False
                logging.getLogger(__name__).error('Unable to parse YAML file: {f}'.format(f=self.fn))
                logging.getLogger(__name__).error('YAML error info: {msg}'.format(msg=str(e)))

            fh.close()
        return self
