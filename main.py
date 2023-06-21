import glob
import json
import os
import pathlib
import re
from typing import Union

import pandas as pd

FIND_REPLACE = {  # original relative to /docs : redirect target
    "<CONTRIBUTING.md>": "[Contributing Section](development/#CONTRIBUTING)",
    "(CODE_OF_CONDUCT.md)": "(development/#CODE_OF_CONDUCT)",
    "CONTRIBUTING.md)": "development/#CONTRIBUTING)",
    "<LICENSE>": "[LICENSE](https://github.com/TIDES-transit/TIDES/blob/main/LICENSE)",
    "contributors.md)": "development/#contributors)",
    "architecture.md)": "architecture)",
    "tables.md": "tables",
}


def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """

    @env.macro
    def include_file(
        filename: str, downshift_h1=True, start_line: int = 0, end_line: int = None
    ):
        """
        Include a file, optionally indicating start_line and end_line.

        Will create redirects if specified in FIND_REPLACE in main.py.

        args:
            filename: file to include, relative to the top directory of the documentation project.
            downshift_h1: If true, will downshift headings by 1 if h1 heading found.
                Defaults to True.
            start_line (Optional): if included, will start including the file from this line
                (indexed to 0)
            end_line (Optional): if included, will stop including at this line (indexed to 0)
        """
        full_filename = os.path.join(env.project_dir, filename)
        with open(full_filename, "r") as f:
            lines = f.readlines()
        line_range = lines[start_line:end_line]
        content = "".join(line_range)

        # Downshift headings if h1 found
        md_heading_re = {
            1: re.compile(r"(#{1}\s)(.*)"),
            2: re.compile(r"(#{2}\s)(.*)"),
            3: re.compile(r"(#{3}\s)(.*)"),
            4: re.compile(r"(#{4}\s)(.*)"),
            5: re.compile(r"(#{5}\s)(.*)"),
        }
        print(f"???before downshifting! {full_filename}")
        if md_heading_re[1].search(content) and downshift_h1:
            print("!!!downshifting!")
            content = re.sub(md_heading_re[5], r"#\1\2", content)
            content = re.sub(md_heading_re[4], r"#\1\2", content)
            content = re.sub(md_heading_re[3], r"#\1\2", content)
            content = re.sub(md_heading_re[2], r"#\1\2", content)
            content = re.sub(md_heading_re[1], r"#\1\2", content)

        _filenamebase = env.page.file.url
        for _find, _replace in FIND_REPLACE.items():
            if _filenamebase in _replace:
                _replace = _replace.replace(_filenamebase, "")

            content = content.replace(_find, _replace)
        return content

    @env.macro
    def frictionless_spec(
        spec_path: str = "**/*.spec.json",
    ) -> str:
        """Translate the frictionless .spec file to a markdown table.

        Note: Right now if it finds more than one, it will take the first one.

        Args:
            spec_path (str, optional): base path of repo. Defaults to two directories
                up from this file.

        Returns: a markdown table string
        """

        spec_file = glob.glob(spec_path, recursive=True)[0]

        print("Documenting spec_file: ", spec_file)

        # Generate a table for overall file requirements
        spec_df = read_config(spec_file)
        spec_df = spec_df.drop(
            columns=["fullpath", "fullpath_schema", "path", "schema", "name"]
        ).reset_index()
        spec_df["name"] = spec_df["name"].apply(
            lambda x: f"[`{x}`](tables.md#{x})".replace("_", "-")
        )

        return spec_df.to_markdown(index=False)

    @env.macro
    def frictionless_schemas(
        schema_path: str = "**/*.schema.json",
    ) -> None:
        """Document frictionless table schema files as markdown tables.

        Args:
            schema_path (str, optional): Schema path in glob format.
                Defaults to "**/*.schema.json".
        """

        # Create markdown with a table for each schema file
        schema_files = glob.glob(schema_path, recursive=True)

        print("Documenting schemas from: {}".format(schema_files))

        file_schema_markdown = [
            _document_frictionless_schema(_s) for _s in schema_files
        ]
        file_schema_markdown.sort(key=lambda schema: schema["spec_title"])
        md = "\n\n"
        for table_type in TABLE_TYPES:
            md += "##{} Tables\n".format(table_type)
            for table in file_schema_markdown:
                if table["table_type"] == table_type:
                    md += table["schema_md"]

        return md


TABLE_TYPES = ["Event", "Summary", "Supporting"]


def _document_frictionless_schema(schema_filename: str) -> dict:
    """Documents a single frictionless schema.

    Args:
        schema_filename (str): location of the schema.

    Returns:
        dict: dictionary with the following keys:
            "table_type": one of TABLE_TYPES to help in sorting/organizing tables
            "spec_title": to use for heading
            "schema_md": markdown table documenting fields

    """
    print(f"Documenting schema from file: {schema_filename}")
    spec_name = schema_filename.split("/")[-1].split(".")[0]
    spec_title = " ".join([x.capitalize() for x in spec_name.split("_")])
    schema = read_schema(schema_filename)
    if "_table_type" in schema:
        table_type = schema["_table_type"]
        if table_type not in TABLE_TYPES:
            raise Exception(
                "{} table_type property of {} does not match known table types".format(
                    table_type, spec_name
                )
            )
    else:
        raise Exception("_table_type property missing from {}".format(spec_name))
    schema_md = "\n### {}\n".format(spec_title)
    schema_md += "\n*{}*\n".format(schema_filename.split("/")[-1])
    if "description" in schema:
        schema_md += "\n{}\n".format(schema["description"])
    schema_md += "\n" + _format_primary_key(schema)
    schema_md += "\n\n{}\n".format(_list_to_md_table(schema["fields"]))
    return {"table_type": table_type, "spec_title": spec_title, "schema_md": schema_md}


def _format_cell_by_type(x, header):
    if "enum" in header and len(x) > 1:
        return "Allowed Values: `" + "`,`".join(map(str, x)) + "`"
    if header == "foreign_key" and len(x) > 1:
        table, var = x.split(".")
        if table == "":
            return "Variable: `{}`".format(var)
        return "Table: `{}`, Variable: `{}`".format(table, var)
    if header == "title" and "referencing GTFS" in x:
        return re.sub(
            r"(.+ referencing )(GTFS )([a-z_]+)\.([a-z_]+)",
            r"\1 [\2\3](https://gtfs.org/schedule/reference/#\3txt).\4",
            x,
        )
    if header == "title" and "ID referencing" in x:
        tname = re.sub(r"ID referencing ([a-z_]+)\.([a-z_]+)", r"\1", x)
        tfield = re.sub(r"ID referencing [a-z_]+\.([a-z_]+)", r"\1", x)
        return "ID referencing [{}](#{tname}).{tfield}".format(
            tname, tname=tname.replace("_", "-"), tfield=tfield
        )
    if header in {"title", "rdfType"} and x.startswith("http"):
        return "<{}>".format(x)
    return str(x).replace("\n", "<br />")


def _recursive_items(d: dict, key_prefix: str = ""):
    """
    Recursively flattens a nested dictionary and returns a dictionary with key_prefixe
    to represent original nesting structures.
    Modified from https://stackoverflow.com/questions/39233973/get-all-keys-of-a-nested-dictionary
    """
    for k, v in d.items():
        if k == "constraints":
            _str = ""
            if v.pop("required", None):
                _str += "**Required**\n"
            if v.pop("unique", None):
                _str += "*Unique*\n"
            enum = [str(x) for x in v.pop("enum", [])]
            if enum:
                _str += "Allowed Values\n - `" + "`\n- `".join(enum) + "`"
            _remove = ["{", "}", "[", "]", '"', ","]
            _json = json.dumps(v, indent=2)
            _str += "".join(s for s in _json if s not in _remove)
            yield (k, _str)

        elif type(v) is dict:
            yield from _recursive_items(v, key_prefix=k + " ")
        else:
            yield (key_prefix + k, v)


def _format_primary_key(schema: dict) -> str:
    """
    Reads the primaryKey property of a schema and creates markdown for the table
    description.
    args:
        schema: a schema dict, see `read_schema`
    returns: A markdown string describing the primary key.
    """
    if "primaryKey" in schema:
        primary_key = schema["primaryKey"]
    else:
        primary_key = "none"
    if isinstance(primary_key, list):
        primary_key = set(primary_key)
    else:
        primary_key = set([primary_key])
    return "Primary key: {`" + "`, `".join(primary_key) + "`}\n"


def _list_to_md_table(list_of_dicts: list) -> str:
    """
    Reads a list of dictionaries defining a schema and creates a markdown table.
    args:
        list_of_dicts: a list of dictionaries containing definition of fields.
    returns: A markdown string representing the table.
    """

    # flatten dictionary
    flat_list = []
    for i in list_of_dicts:
        flat_list.append({k: v for k, v in _recursive_items(i)})

    # get all items listed
    standard_header_fields = [
        "name",
        "constraints",
        "type",
        # "foreign_key",
        "description",
    ]

    _all_header_fields = [k for i in flat_list for k, v in i.items()]
    _additional_header_fields = list(
        set(_all_header_fields) - set(standard_header_fields)
    )
    _header_fields = standard_header_fields + sorted(_additional_header_fields)

    header_md = "|" + "|".join(_header_fields) + "|\n"
    header_md += "|---" * len(_header_fields) + "|\n"

    body_md = ""
    for d in flat_list:
        body_md += (
            "|"
            + "|".join([_format_cell_by_type(d.get(i, " "), i) for i in _header_fields])
            + "|\n"
        )

    return header_md + body_md


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


def read_config(
    config_path: Union[pathlib.Path, str],
    data_dir: Union[pathlib.Path, str] = None,
    schema_dir: Union[pathlib.Path, str] = None,
) -> pd.DataFrame:
    """
    Reads a frictionliess spec config file, adds some full paths and returns as a dataframe.

    Args:
        config_path: Configuration file. A json file with a list of "resources"
            specifying the "name", "path", and "schema" for each spec table as
            well as a boolean value for "required".
            Example:
            ::
                {
                  "resources": [
                   {
                     "name":"link",
                     "path": "link.csv",
                     "schema": "link.schema.json",
                     "required": true
                   },
                   {
                     "name":"node",
                     "path": "node.csv",
                     "schema": "node.schema.json",
                     "required": true
                   }
                 }
        data_dir: Directory where example files go.
        schema_dir: Directory where schema files are. If not specified, assumes
            the same directory as the config_file.
    Returns: frictionless configuration file as a DataFrame.
    """
    config_path = pathlib.Path(config_path)
    if data_dir is None:
        data_dir = config_path.parent
    if schema_dir is None:
        schema_dir = config_path.parent

    with open(config_path, encoding="utf-8") as config_file:
        config = json.load(config_file)

    resource_df = pd.DataFrame(config["resources"])

    resource_df["required"].fillna(False, inplace=True)

    # Add full paths
    resource_df["fullpath"] = resource_df["path"].apply(
        lambda x: os.path.join(data_dir, x)
    )
    resource_df["fullpath_schema"] = resource_df["schema"].apply(
        lambda x: os.path.join(schema_dir, x)
    )

    resource_df.set_index("name", drop=False, inplace=True)
    return resource_df
