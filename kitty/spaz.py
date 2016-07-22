"""
FILE
    spaz.py

SYNOPSIS
    Update group of files
        spaz.py
            --role NAME
            --config FILE           TODO: Well known location, self located

OPTIONS
    --role NAME
        Specifies the role to be processed. NAME is defined in the --config file.

    --config FILE
        The name of the values file that will be used to update files.

    --dry-run
        Only show what would change. No results are written.

CONFIGURATION FILE - FORMAT

    Column
    00000000011111111112
    12345678901234567890

    ROLE:
      # comment
      FQFN1:
        nickname: NAME
        type: variable or property
        values:
          key1: value1
          key2: value2

CONFIGURATION FILE - VALIDATIONS

    "is unique" means unique per scope of entire config file unless "per SCOPE" is stated.

        - ROLE is unique.
        - FQFNi is unique. FQFN may only appear under one ROLE.
        - nickname is unique
        - FQFN.values.key# is unique per file

SCRIPT CONFIGURATION

    ---
    general:
      # Which environment to run under
      current-environment: NAME
    ---
    # Settings unique to environment
    environment:
      name: NAME
      config-file: fn
    ---
    environment:
      name: NAME
      config-file: fn


FILES
    spaz.conf
        Operational configuration of script behavior.

"""

import logging
import argparse
from options import Options
from configuration import Configuration
from render import Render
from setuplogging import SetupLogging
import sys


class Spaz:
    # Script configuration file
    OPTIONS_FILE = r'spaz.conf'
    LOGGING_CONFIG_FILE = r'spaz.logging.conf'

    def __init__(self):
        self.args = None
        self.options = None
        self.configuration = None
        self.say = None

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Configure values in templates and property files")
        parser.add_argument("--role", action="store", help="File group name")
        parser.add_argument("--validate", action="store_true", help="Validate configuration files")
        parser.add_argument("--dry-run", action="store_true", help="Expand templates in memory, no files updated")
        self.args = parser.parse_args()

    def load_configuration(self):
        self.options = Options.from_file(Spaz.OPTIONS_FILE)
        if not self.options.ok:
            sys.exit(1)

        self.parse_args()
        self.configuration = Configuration.from_file(self.options.config_file)
        if not self.configuration.ok:
            sys.exit(1)
        if self.args.validate:
            # just validate configuration
            logging.getLogger(__name__).info("Validated: OK")
            sys.exit(0)

    def render_ok(self, renders):
        for render in renders:
            if not render.ok:
                return False
        return True

    def start(self):
        logging.getLogger(__name__).info("Start of script")
        self.load_configuration()
        role = self.configuration.role(self.args.role)

        if role:
            logging.getLogger(__name__).info("Processing role: {r}".format(r=role.name))

            renders = []
            for file_entry in role.file_entries:
                render = Render.from_file_entry(file_entry)
                if render:
                    renders.append(render)

            # any renders had errors, don't continue
            if not self.render_ok(renders):
                sys.exit(1)

            # Renders are OK, but don't write anything
            if self.args.dry_run:
                logging.getLogger(__name__).info("Dry run: OK")
                sys.exit(0)

            # Renders are OK and we want to write files
            for render in renders:
                render.to_file()

    def start_logging(self, fn):
        SetupLogging.from_yaml(fn)

    def stop_logging(self):
        logging.shutdown()

    def show_args(self):
        if self.args.role:
            print("--role {value}".format(value=self.args.role))
            if self.args.validate:
                print("--validate")
            if self.args.dry_run:
                print("--dry-run")


if __name__ == "__main__":
    spaz = Spaz()
    # allow testing to configure logging
    spaz.start_logging(spaz.LOGGING_CONFIG_FILE)
    spaz.start()
