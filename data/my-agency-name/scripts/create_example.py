#!/usr/bin/env python3

import glob
import json
import os
import pathlib
from random import choice, randrange
from datetime import timedelta

import numpy as np
import pandas as pd

EXAMPLE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_REPO_DIR = os.path.dirname(os.path.dirname(os.path.dirname(EXAMPLE_DIR)))
TIDES_SPEC = os.path.join(BASE_REPO_DIR, "spec")

SCHEMAS = glob.glob(os.path.join(TIDES_SPEC, "**/*.schema.json"), recursive=True)

frictionless_to_pandas_types = {
    "date": "datetime64[ns]",
    "datetime": "datetime64[ns]",
    "time": "datetime64[ns]",
    "string": "object",
    "integer": "int",
    "float": "float64",
    "number": "float64",
    "boolean": "bool",
}


def write_schema_examples(
    out_dir: str,
    schemas: list = SCHEMAS,
    generate_random: bool = False,
    example_length: int = 5,
) -> None:
    for s in schemas:
        write_csv_for_schema(
            s, out_dir, generate_random=generate_random, example_length=example_length
        )


def write_csv_for_schema(
    schema_filename: str,
    out_dir: str,
    generate_random: bool = False,
    example_length: int = 5,
) -> None:
    """Creates blank or randomly filled csvs which comply with a schema.

    Args:
        schema_filename (str): Filename with the Frictionless data schema
        out_dir (str): Where the csv will be written
        generate_random (bool): If true, will generate Defaults to False.
        example_length (int): If generate_random is True, will generate this number of records. Defaults to 5.
    """
    schema = read_schema(schema_filename)
    schema_name = pathlib.Path(schema_filename).stem.split(".")[0]
    fields_types = {
        f["name"]: frictionless_to_pandas_types[f["type"]] for f in schema["fields"]
    }
    fields_series = {f: pd.Series(dtype=t) for f, t in fields_types.items()}
    df = pd.DataFrame(fields_types)
    out_filename = os.path.join(out_dir, schema_name + ".csv")
    df.to_csv(out_filename, index=False)


def field_to_pd_series(field_def: dict, length: int):
    default_min = 0
    default_max = 100
    if field_def["type"] in ["number","integer"]:
        _min = field_def.get("constraints", {}).get("minimum", default_min)
        _max = field_def.get("constraints", {}).get("maximum", default_min)
        return pd.Series(
            np.random.randint(_min, _max, length),
            dtype=frictionless_to_pandas_types[field_def["type"]],
        )
    elif field_def["type"] == "float":
        _min = field_def.get("constraints", {}).get("minimum", default_min)
        _max = field_def.get("constraints", {}).get("maximum", default_min)
        return pd.Series(
            np.random.rand(_min, _max) * length,
            dtype=frictionless_to_pandas_types[field_def["type"]],
        )
    elif field_def["type"] == "string":
        default_str = "a value"
        _enum = field_def.get("constraints", {}).get("enum", [default_str])
        return pd.Series(
            [choice(_enum) for x in range(length)],
            dtype=frictionless_to_pandas_types[field_def["type"]],
        )
    elif field_def["type"]=="date":


    elif field_def["type"]=="time":

    elif field_def["type"]=="datetime":

    else:
        raise ValueError(f'Don't recognize {field_def["type"]')


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

default_start_datetime = datetime.strptime('1/1/2022 1:30 PM', '%m/%d/%Y %I:%M %p')
default_end_datetime = datetime.strptime('1/9/2022 6:30 PM', '%m/%d/%Y %I:%M %p'

def random_date(start: datetime.datetime = , end: datetime.datetime):
    """
    This function will return a random datetime between two datetime 
    objects.

    Source: 
    https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    """
    
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)



if __name__ == "__main__":
    write_schema_examples(out_dir=EXAMPLE_DIR, generate_random=True)
