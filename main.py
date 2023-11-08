import glob
import json
import logging
import os
import pathlib
import re
from typing import Union, Literal

import pandas as pd

log = logging.getLogger("mkdocs")

BRANCH_NAME_KEYWORD = "{branch_name}"
GITHUB_REPO = f"http://github.com/TIDES-transit/TIDES/tree/{BRANCH_NAME_KEYWORD}"

# targets for these link keys will be updated upon doc build
UPDATE_LINKS = {
    "[architecture]":"./architecture",
    "[table schemas]":"./tables",
    "[contributors]":"./development/#contributors",
    "[contributing]": "./development",
    "[code of conduct]": "development/#code_of_conduct",
    "[license]": f"{GITHUB_REPO}/LICENSE)",
    "[tides-datapackage-profile]": "./datapackage",
    "[template-datapackage]":f"{GITHUB_REPO}/samples/template/TIDES/datapackage.json",
    "[project governance]":"governance.md"
}

def get_git_branch_name():
    import subprocess
    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()
    log.info("On branch: {branch}")
    return branch

# The pattern to match markdown links like [Architecture]:./architecture
md_link_pattern = re.compile(r'^(\[[^\]]+\]):\s*(.+)$', re.MULTILINE)

def replace_links_in_markdown(content_md:str, replacement_links:dict = UPDATE_LINKS):
   
    def replace_match(match):
        key = match.group(1)
        # If the key in the markdown matches one in our dictionary, replace it
        if key in replacement_links:
            return f"{key}: {replacement_links[key]}"
        else:
            return match.group(0)  # No replacement found, return the original text

    # Replace all occurrences in the content
    new_content = md_link_pattern.sub(replace_match, content_md)

def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """
    @env.macro
    def list_artifacts(directory: str):
        """
        List all artifacts in the specified directory, including PDF files.
        Use the first H1 heading in Markdown files as the link text.
        """
        artifacts_dir = os.path.join(env.project_dir, directory)
        if not os.path.exists(artifacts_dir):
            return "Directory does not exist."
        
        files = os.listdir(artifacts_dir)
        links = []
        for file in files:
            full_path = os.path.join(artifacts_dir, file)
            if file.endswith('.md'):
                with open(full_path, 'r', encoding='utf-8') as md_file:
                    content = md_file.read()
                match = re.search(r'^#\s(.+)$', content, re.MULTILINE)
                link_text = match.group(1).strip() if match else os.path.splitext(file)[0]
                url = url_for(os.path.join(directory, file))
            elif file.endswith('.pdf'):
                link_text = os.path.splitext(file)[0]
                url = url_for(os.path.join(directory, file))
            else:
                continue
            links.append(f'- [{link_text}]({url})')
        return '\n'.join(links)

    @env.macro
    def url_for(file_path):
        """
        Create a relative URL for a file given its path within the MkDocs source directory.

        :param file_path: The file path relative to the MkDocs documentation source directory.
        :return: A relative URL that can be used in the MkDocs site.
        """
        # Remove the leading 'docs/' if present, because URLs do not include it
        if file_path.startswith('docs/'):
            file_path = file_path.replace("docs/", "TIDES/")

        # MkDocs will convert the .md files to a folder structure
        if file_path.endswith('.md'):
            file_path = file_path[:-3] + '/'

        # Ensure leading slash
        if not file_path.startswith('/'):
            file_path = '/' + file_path

        # Append 'index.html' if the file path points to a directory (this should be adjusted if MkDocs is configured differently)
        if not file_path.endswith('/'):
            file_path += '/index.html'

        return file_path


    @env.macro
    def list_samples(sample_dir: str) -> str:
        """Outputs a simple list of the directories in a folder in markdown.
        Args:
            sample_dir (str):directory to search in
        Returns:
            str: markdown-formatted list
        """
        EXCLUDE = ["template"]
        fields = ["Sample", "Agency", "Resources", "Vendors"]

        sample_dir = os.path.join(env.project_dir, sample_dir)
        samples = [
            d
            for d in os.listdir(sample_dir)
            if os.path.isdir(os.path.join(sample_dir, d)) and d not in EXCLUDE
        ]

        md_table = (
            "| *" + "** | **".join(fields) + "* |\n| " + " ----- |" * len(fields) + "\n"
        )

        for s in samples:
            md_table += datapackage_to_row(os.path.join(sample_dir, s, "TIDES"), fields)
        return md_table

    @env.macro
    def include_file(
        filename: str,
        downshift_h1=True,
        start_line: int = 0,
        end_line: int = None,
        code_type: str = None,
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
            code_type: if not None, will encapsulate the resulting file in
                ```<code_type>..file contents...```
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

        if md_heading_re[1].search(content) and downshift_h1:
            content = re.sub(md_heading_re[5], r"#\1\2", content)
            content = re.sub(md_heading_re[4], r"#\1\2", content)
            content = re.sub(md_heading_re[3], r"#\1\2", content)
            content = re.sub(md_heading_re[2], r"#\1\2", content)
            content = re.sub(md_heading_re[1], r"#\1\2", content)

        content = replace_links_in_markdown(content)

        if BRANCH_NAME_KEYWORD in content:
            content = content.replace(BRANCH_NAME_KEYWORD,  get_git_branch_name())

        # Add code fences if applicable
        if code_type is not None:
            content = f"\n```{code_type} title='{filename}'\n{content}\n```"
        return content

    @env.macro
    def frictionless_data_package(
        data_package_path: str = "**/data-package.json",
        sub_schema: str = None,
        include: Literal["required", "recommended", "all"] = "recommended",
    ) -> str:
        """Describes top-level fields of a data package as a markdown table.

        Note: Right now if it finds more than one, it will take the first one.

        Args:
            data_package_path (str, optional): location or glob pattern of data package. If glob,
                will use the first found match.
            sub_schema: if provided, will look for that portion of the schema and use that as
                the "top level"
            include: specifies the fields to include. Must be one of:
                 - "required": will only document required fields
                 - "recommended": will document required and recommended fields
                 - "all": will document all fields
                Defaults to "recommended".

        Returns: a markdown table string
        """
        INCLUDE = ["name", "description", "type", "requirement"]

        dp_filename = glob.glob(data_package_path, recursive=True)[0]

        log.info(
            f"Documenting spec_file: {dp_filename}.{sub_schema} including {include}"
        )

        with open(dp_filename, "r") as dp_file:
            dp = json.loads(dp_file.read())

        if sub_schema is not None:
            if sub_schema in dp["properties"]:
                dp = dp["properties"][sub_schema]
            elif sub_schema in dp["$defs"]:
                dp = dp["$defs"][sub_schema]
            else:
                return "Cannot find sub-schema {sub_schema} in data package file {dp_filename}"
            if dp["type"] == "array":
                dp = dp["items"]

        _field_names = []

        if include in ["required", "recommended"]:
            _field_names += dp.get("required", [])
        if include == "recommended":
            _field_names += dp.get("recommended", [])
        if include == "all":
            _field_names = list(dp["properties"].keys())

        if not _field_names:
            return "No fields found to document with parameters."

        _fields = []
        for _f in _field_names:
            log.debug(f"Documenting: {_f}")
            _row_entry = {k: v for k, v in dp["properties"][_f].items() if k in INCLUDE}
            if _f in dp.get("required", []):
                _row_entry["requirement"] = "required"
            elif _f in dp.get("recommended", []):
                _row_entry["requirement"] = "recommended"
            else:
                _row_entry["requirement"] = " - "

            _row_entry["name"] = f"`{_f}`"
            if dp["properties"][_f].get("enum"):
                _row_entry["description"] += "<br>**Must** be one of:<ul><li>`"
                _row_entry["description"] += "`</li><li>`".join(
                    dp["properties"][_f]["enum"]
                )
                _row_entry["description"] += "`</li></ul>"
            elif dp["properties"][_f].get("const"):
                _row_entry[
                    "description"
                ] += f"<br>**Must** be: `{dp['properties'][_f]['const']}`"
            elif dp["properties"][_f].get("examples"):
                _ex = dp["properties"][_f]["examples"][0].replace("\n", "<br>")
                _row_entry["description"] += f"<br>**Example**:<br>`{_ex}`"

            _fields.append(_row_entry)

        dp_df = pd.DataFrame(_fields, columns=INCLUDE)
        dp_md = dp_df.to_markdown(index=False)

        return dp_md

    @env.macro
    def frictionless_spec(
        spec_path: str = "**/*.spec.json",
    ) -> str:
        """Translate the frictionless .spec file to a markdown table.

        Note: Right now if it finds more than one, it will take the first one. If glob,
                will use the first found match.

        Args:
            spec_path (str, optional): location or glob pattern of spec

        Returns: a markdown table string
        """

        spec_file = glob.glob(spec_path, recursive=True)[0]

        log.info(f"Documenting spec_file: {spec_file}")

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

        log.info("Documenting schemas from: {schema_files}")

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


def datapackage_to_row(dir: str, fields: list) -> str:
    """Reads datapackage and translates key metadata to a row in a markdown table.

    Right now, only works for fields: "Sample", "Agency", "Resources", "Vendors"

    Args:
        dir (str): fully qualified directory for sample data
        fields (list): list of fields to return

    Returns:
        str: row in a markdown table with name, agency, resources, vendors
    """
    dp_filename = os.path.join(dir, "datapackage.json")
    if not os.path.isfile(dp_filename):
        raise ValueError(f"Can't find datapackage file:\n   {dp_filename}.")
    with open(dp_filename, "r") as dp_file:
        dp = json.loads(dp_file.read())

        _vendors = [
            s.get("vendor", None) for r in dp["resources"] for s in r.get("sources", [])
        ]
        _vendors = list(set(_vendors) - set([None]))

        _md_cells = {
            "Sample": _to_sample_readme_link(dp["name"], dir),
            "Agency": dp["agency"],
            "Resources": (
                "<ul><li>`"
                + "`</li><li>`".join([r["name"] for r in dp["resources"]])
                + "`</li></ul>"
            ),
            "Vendors": "<ul><li>`" + "`</li><li>`".join(_vendors) + "`</li></ul>",
        }

        md_row = "| " + " | ".join([_md_cells[f] for f in fields]) + " |\n"

        return md_row


def _to_sample_readme_link(sample_name, folder_dir):
    return f"[{sample_name.capitalize()}]({folder_dir}/README.md)"


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
    log.info(f"Documenting schema from file: {schema_filename}")
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
