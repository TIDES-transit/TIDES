import glob
import json
import os
import pathlib
import re
from typing import Union

import pandas as pd

TABLE_TYPES = ["Event", "Summary", "Supporting"]


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


def _fill_template(
    outfile_path: Union[str, pathlib.Path],
    content_dict: dict,
    template_path: Union[str, pathlib.Path] = None,
) -> None:
    """Replace contents of a text file with template variables filled by a dictionary.

    Args:
        outfile_path (Union[str,pathlib.Path]): File to write output to.
        content_dict (dict[): Dictionary of values to fill template with.
        template_path (Union[str,pathlib.Path], optional): _description_. If not specified, will assume
            it is the outfile with a .template suffix (i.e. index.template.md)

    Raises:
        ValueError: _description_
    """

    outfile_path = pathlib.Path(outfile_path)
    if template_path is None:
        template_path = outfile_path.parent / pathlib.Path(
            outfile_path.stem + ".template" + outfile_path.suffix
        )

    with open(template_path) as _template_file:
        _txt_contents = _template_file.read().format(**content_dict)
        with open(os.path.join(outfile_path), "w") as _outfile:
            _outfile.write(_txt_contents)


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


def document_schemas(
    base_path: str = "",
    docs_path: str = "",
    outfile_name="tables.md",
) -> None:
    """Document frictionless table schema files as markdown tables.

    Args:
        base_path (str, optional): base path of repo. Defaults to two directories up from this file.
        docs_path (str, optional): path where documentation is written. Defaults to "docs" within
            the base_path.
        outfile_name (str,optional): name of the file (and corresponding template) to write to.
            Defaults to architecture.md.
        out_path (str, optional): _description_. Defaults to ''.
    """

    if not base_path:
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if not docs_path:
        docs_path = os.path.join(base_path, "docs")

    # Create markdown with a table for each schema file

    schema_files = glob.glob(
        os.path.join(base_path, "**/*.schema.json"), recursive=True
    )
    print("Documenting schemas from: {}".format(schema_files))

    file_schema_markdown = []
    for s in schema_files:
        print(f"Documenting Schema: {s}")
        spec_name = s.split("/")[-1].split(".")[0]
        spec_title = " ".join([x.capitalize() for x in spec_name.split("_")])
        schema = read_schema(s)
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
        schema_md += "\n*{}*\n".format(s.split("/")[-1])
        if "description" in schema:
            schema_md += "\n{}\n".format(schema["description"])
        schema_md += "\n" + _format_primary_key(schema)
        schema_md += "\n\n{}\n".format(_list_to_md_table(schema["fields"]))
        file_schema_markdown.append(
            {"table_type": table_type, "spec_title": spec_title, "schema_md": schema_md}
        )

    file_schema_markdown.sort(key=lambda schema: schema["spec_title"])
    md = "\n\n"
    for table_type in TABLE_TYPES:
        md += "##{} Tables\n".format(table_type)
        for table in file_schema_markdown:
            if table["table_type"] == table_type:
                md += table["schema_md"]

    _fill_template(
        outfile_path=os.path.join(docs_path, outfile_name),
        content_dict={"TABLES": md},
    )


def document_spec(
    base_path: str = "",
    docs_path: str = "",
    outfile_name="architecture.md",
) -> None:
    """Translate the frictionless .spec file to a markdown table.

    Args:
        base_path (str, optional): base path of repo. Defaults to two directories up from this file.
        docs_path (str, optional): path where documentation is written. Defaults to "docs" within
            the base_path.
        outfile_name (str,optional): name of the file (and corresponding template) to write to.
            Defaults to architecture.md.
    """
    if not base_path:
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if not docs_path:
        docs_path = os.path.join(base_path, "docs")

    spec_file = glob.glob(os.path.join(base_path, "**/*.spec.json"), recursive=True)[0]

    print("Documenting spec_file: ", spec_file)

    # Generate a table for overall file requirements
    spec_df = read_config(spec_file)
    spec_df = spec_df.drop(
        columns=["fullpath", "fullpath_schema", "path", "schema", "name"]
    ).reset_index()
    spec_df["name"] = spec_df["name"].apply(
        lambda x: "[`{}`](tables.md#{})".format(x, x)
    )

    _fill_template(
        outfile_path=os.path.join(docs_path, outfile_name),
        content_dict={"SPEC": spec_df.to_markdown(index=False)},
    )


def repo_to_docs(
    infile_name, outfile_name: str = None, base_path: str = "", docs_path: str = ""
):
    """Copy files from repo to docs (i.e. README).

    Args:
        infile_name (str): file to transfer from base repo to documentation directory
        outfile_name (str): what to call the outfile in docs dir. Defaults to infile_name.
        base_path (str, optional): _description_. Defaults to ''.
        docs_path (str, optional): _description_. Defaults to ''.
    """
    if not outfile_name:
        outfile_name = infile_name
    if not base_path:
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if not docs_path:
        docs_path = os.path.join(base_path, "docs")

    with open(os.path.join(base_path, infile_name), "rt") as fin:
        with open(os.path.join(docs_path, outfile_name), "wt") as fout:
            for line in fin:
                outline = line
                # add any fixes that need to happen here.
                fout.write(outline)


if __name__ == "__main__":
    document_spec()
    document_schemas()
