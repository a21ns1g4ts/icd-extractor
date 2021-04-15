"""
This is a extractor file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = icd_extractor.extractor:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This extractor file can be safely removed if not needed!

References:
    - https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from icd_extractor import __version__

__author__ = "Atiladanvi"
__copyright__ = "Atiladanvi"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from icd_extractor.extractor import fib`,
# when using this Python module as a library.


def extract(file):
    """Extract icd from file

    Args:
      file (str): string

    Returns:
      str: file path output
    """
    path_import = file

    with open(path_import, 'r') as _f:
        raw = _f.read()
        _f.close()

    # convert raw txt to json
    data = []
    for rcd in raw.split('\n'):
        if rcd:
            data.append({
                'code': rcd[:8].strip(),
                'desc': rcd[9:],
            })

    # export converted json
    file_name = file.split('/')[-1].split('.')[0] + '.json'
    path_export = Path().absolute().__str__() + '/storage/' + file_name

    with open(path_export, 'w') as _f:
        json.dump(data, _f)
        _f.close()

    return path_export


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="ICD Extractor")
    parser.add_argument(
        "--version",
        action="version",
        version="icd-extractor {ver}".format(ver=__version__),
    )
    parser.add_argument(dest="n", help="path of ICD .txt file", type=str, metavar="STR")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`extract` to be called with string arguments in a CLI fashion

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    _logger.debug("Starting ICD extract...")

    try:
        extract(args.n)
    except Exception as e:
        logging.exception(e)
    finally:
        print("FILE_PATH: {}".format(args.n))
        _logger.info("Success!")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m icd_extractor.extractor /home/danvizera/Projects/danvi/icd-extractor/tests/icd10cm_codes_test.txt
    #
    run()
