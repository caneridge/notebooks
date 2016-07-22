# todo: setup default logging that predates logger setup

import logging
import logging.config
import yaml
import sys


class SetupLogging:
    def __init__(self):
        pass

    @classmethod
    def from_yaml(cls, fn):
        self = cls()

        # Read yaml configuration
        try:
            fh = open(fn, 'r')
        except Exception as e:
            logging.critical("Unable to read logging configuration file: {f}". format(f=fn))
            print(str(e))

            # Cannot continue
            sys.exit(1)
        else:
            try:
                config = yaml.load(fh.read())
                fh.close()
            except Exception as e:
                logging.critical("Unable to load logging yaml configuration file: {f}". format(f=fn))
                print(str(e))

                # Cannot continue
                sys.exit(1)
            else:
                logging.config.dictConfig(config)
        return self
