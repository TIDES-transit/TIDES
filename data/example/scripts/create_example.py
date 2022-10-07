#!/usr/bin/env python3

import glob
import json
import os
import pathlib


EXAMPLE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_REPO_DIR = os.path.dirname(os.path.dirname(EXAMPLE_DIR))
TIDES_SPEC = os.path.join(BASE_REPO_DIR, "spec")
SCHEMAS = glob.glob(os.path.join(TIDES_SPEC, "**/*.schema.json"), recursive=True)
SCHEMAS_LOC = "https://raw.githubusercontent.com/TIDES-transit/TIDES/main/spec/"

# DATAPACKAGE.JSON INFORMATION
# Per https://specs.frictionlessdata.io/data-package/
TITLE = "example"
NAME = "Example TIDES Data Package"
PROFILE = "tabular-data-package"
LICENSES = [{"name": "Apache-2.0"}]
SOURCES = [{"title": "Generated from /scripts/create_example.py"}]
CONTRIBUTORS = [{"title": "My Name", "email": "me@myself.com"}]
MAINTAINERS = [{"title": "Another Name", "email": "another@myself.com"}]
DATAPACKAGE_TEMPLATE = {
    "name": NAME,
    "title": TITLE,
    "profile": PROFILE,
    "licenses": LICENSES,
    "contributors": CONTRIBUTORS,
    "maintainers": MAINTAINERS,
    "resources": [],
}


def write_schema_examples(
    out_dir: str,
    schemas: list = SCHEMAS,
) -> None:
    """Write blank csvs to out_dir with headings for for each schema in list.

    Args:
        out_dir (str): Where blank csvs are written.
        schemas (list, optional): List of schemas to generate blank csvs for. Defaults to SCHEMAS.
    """
    for s in schemas:
        write_csv_for_schema(s, out_dir)


def write_datapackage(
    out_dir: str,
    schemas: list = SCHEMAS,
    template: dict = DATAPACKAGE_TEMPLATE,
) -> None:
    """Write a datapackage.json file in Frictionless data-package format based on list of schemas.

    Args:
        out_dir (str): directory where datapackage.json is written.
        schemas (list, optional): List of schemas to add to resources list . Defaults to SCHEMAS.
    """
    datapackage = template
    datapackage["resources"] = [schema_to_resources(s) for s in schemas]

    out_filename = os.path.join(out_dir, "datapackage.json")
    with open(out_filename, "w") as outfile:
        outfile.write(json.dumps(datapackage, indent=4))
        print(f"Wrote {out_filename}")
    json.dumps


def schema_to_resources(schema_filename: str) -> dict:
    """Transform a schema filename into a frictionless resource for listing in datapackage.json

    Args:
        schema_filename (str): Schema file in frictionless format.

    Returns:
        dict: object consistent with frictionless data resource specification
    """
    schema_filename = pathlib.Path(schema_filename)
    name = schema_filename.stem.split(".")[0]
    path = name + ".csv"
    schema_loc = SCHEMAS_LOC + name + ".schema.json"

    return {"name": name, "path": path, "schema": schema_loc}


def write_csv_for_schema(
    schema_filename: str,
    out_dir: str,
) -> None:
    """Creates blank csvs which comply with a schema.

    Args:
        schema_filename (str): Filename with the Frictionless data schema
        out_dir (str): Where the csv will be written
    """
    schema = read_schema(schema_filename)
    fields = [s["name"] for s in schema["fields"]]
    schema_name = pathlib.Path(schema_filename).stem.split(".")[0]
    out_filename = os.path.join(out_dir, schema_name + ".csv")
    with open(out_filename, "w") as outfile:
        outfile.write(",".join(fields))
        print(f"Wrote {out_filename}")


def read_schema(schema_file: str) -> dict:
    """
    Reads in schema from schema json file and returns as dictionary.

    Args:
        schema_file: File location of the schema json file.
    Returns: The schema as a dictionary
    """
    with open(schema_file, encoding="utf-8") as f:
        schema = json.load(f)
    return schema


if __name__ == "__main__":
    write_schema_examples(out_dir=os.path.join(EXAMPLE_DIR, "data"))
    write_datapackage(out_dir=os.path.join(EXAMPLE_DIR, "data"))
