#!/usr/bin/env python3

"""
Generates a set of template files using structure and defaults of **schema.json

--output-path Saves it in the specified output directory (/path/to/output).
If the argument is not provided, it will default to the same directory as the script.

--schema can specify using a specific schema instead of the default of all
"""

import argparse
import glob
import logging
import os
import pathlib

from frictionless import Schema

USAGE = """
python samples/template/scripts/create_template_files.py --output-dir /path/to/output
"""


SAMPLE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_REPO_DIR = os.path.dirname(os.path.dirname(SAMPLE_DIR))
SCHEMAS = glob.glob(
    os.path.join(os.path.join(BASE_REPO_DIR, "spec"), "**/*.schema.json"),
    recursive=True,
)
DEFAULT_OUT_PATH = "../TIDES"


def write_template_for_schema(
    schema_filename: str,
    out_dir: str,
) -> None:
    """Creates blank csvs which comply with a schema.

    Args:
        schema_filename (str): Filename with the Frictionless data schema
        out_dir (str): Where the csv will be written
    """
    _schema = Schema(schema_filename)
    fields = [s.name for s in _schema.fields]
    _schema_name = pathlib.Path(schema_filename).stem.split(".")[0]
    out_filename = os.path.join(out_dir, _schema_name + ".csv")
    with open(out_filename, "w") as outfile:
        logging.info(f"Writing: {out_filename}")
        outfile.write(",".join(fields))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description="Generate a template csvs.")
    parser.add_argument(
        "--schema",
        default=SCHEMAS,
        help="List of paths to frictionless schemas to generate. Default: all in /spec dir.",
    )
    parser.add_argument(
        "--output-path",
        default=DEFAULT_OUT_PATH,
        help="Directory to save the generated files. Default: same directory as script.",
    )
    args = parser.parse_args()

    for s in args.schema:
        write_template_for_schema(s, args.output_path)
