#!/usr/bin/env python3

import glob
import json
import os
import pathlib
import string
from random import choice, randrange
from datetime import timedelta, datetime

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

    fields_series = {f['name']: field_to_pd_series(f,example_length) for f in schema["fields"]}
    df = pd.DataFrame(fields_series)
    out_filename = os.path.join(out_dir, schema_name + ".csv")
    df.to_csv(out_filename, index=False)


def field_to_pd_series(field_def: dict, length: int):
    default_min = 0
    default_max = 100
    default_str = list(string.ascii_lowercase)
    default_dt_min = 'Jan 1 2022  12:01AM'
    default_dt_max = 'Apr 1 2022  3:00AM'
    
    if field_def["type"] in ["number","integer"]:
        _min = field_def.get("constraints", {}).get("minimum", default_min)
        _max = field_def.get("constraints", {}).get("maximum", default_max)
        return pd.Series(
            np.random.randint(_min, _max, length),
            dtype=frictionless_to_pandas_types[field_def["type"]],
        )
    elif field_def["type"] == "float":
        _min = field_def.get("constraints", {}).get("minimum", default_min)
        _max = field_def.get("constraints", {}).get("maximum", default_max)
        return pd.Series(
            np.random.rand(_min, _max) * length,
            dtype=frictionless_to_pandas_types[field_def["type"]],
        )
    elif field_def["type"] == "string":
        _enum = field_def.get("constraints", {}).get("enum", default_str)
        return pd.Series(
            [choice(_enum) for x in range(length)],
            dtype=frictionless_to_pandas_types[field_def["type"]],
        )
    elif field_def["type"]=="date":
        _min = datetime.strptime(field_def.get("constraints", {}).get("minimum", default_dt_min), '%b %d %Y %I:%M%p').date()
        _max = datetime.strptime(field_def.get("constraints", {}).get("maximum", default_dt_max), '%b %d %Y %I:%M%p').date()
        _rand_int = np.random.randint(0, int((_max - _min).days), length).tolist()
        return pd.Series(
            [_min+timedelta(days=i) for i in _rand_int ],
            dtype=frictionless_to_pandas_types[field_def["type"]],
        )

    elif field_def["type"]=="time":
        _min = datetime.strptime(field_def.get("constraints", {}).get("minimum", default_dt_min), '%b %d %Y %I:%M%p')
        _max = datetime.strptime(field_def.get("constraints", {}).get("maximum", default_dt_max), '%b %d %Y %I:%M%p')
        _rand_int = np.random.randint(0, int((_max - _min).seconds/60), length).tolist()
        _dt_df = pd.Series(
            [_min+timedelta(seconds=i*60) for i in _rand_int ],
            dtype=frictionless_to_pandas_types[field_def["type"]],
        )
        #format as string
        return pd.to_datetime(_dt_df).dt.strftime('%H:%M:%SZ')

    elif field_def["type"]=="datetime":
        _min = datetime.strptime(field_def.get("constraints", {}).get("minimum", default_dt_min), '%b %d %Y %I:%M%p')
        _max = datetime.strptime(field_def.get("constraints", {}).get("maximum", default_dt_max), '%b %d %Y %I:%M%p')
        _rand_int = np.random.randint(0, int((_max - _min).seconds/60), length).tolist()
        _dt_df = pd.Series(
            [_min+timedelta(seconds=i*60) for i in _rand_int],
            dtype=frictionless_to_pandas_types[field_def["type"]],
        )
        #format as ISO-8601 string
        return pd.to_datetime(_dt_df).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    elif field_def["type"]=="boolean":

        return pd.Series(
            [choice([True,False]) for x in range(length)],
            dtype=frictionless_to_pandas_types[field_def["type"]],
        )
    else:
        raise ValueError(f'Dont recognize {field_def["type"]}')


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
    write_schema_examples(out_dir=EXAMPLE_DIR, generate_random=True)
