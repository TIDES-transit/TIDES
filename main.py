from datetime import datetime, date
import glob
import json
import logging
import os
import pathlib
import re
import yaml
from typing import Union, Literal

import pandas as pd

log = logging.getLogger("mkdocs")

BRANCH_NAME_KEYWORD = "{branch_name}"
GITHUB_REPO = f"http://github.com/TIDES-transit/TIDES/tree/{BRANCH_NAME_KEYWORD}"

# targets for these link keys will be updated upon doc build
UPDATE_LINKS = {
    "[architecture]":"architecture.md",
    "[table schemas]":"tables.md",
    "[contributors]":"development.md#contributors",
    "[contributors.md]":"development.md#contributors",
    "[contributing]": "development.md",
    "[code of conduct]": "./governance/policies/code_of_conduct.md",
    "[license]": f"{GITHUB_REPO}/LICENSE)",
    "[tides-datapackage-profile]": "datapackage.md",
    "[tides-datapackage-profile-json]":f"{GITHUB_REPO}/spec/tides-datapackage-profile.json",
    "[template-datapackage]":f"{GITHUB_REPO}/samples/template/TIDES/datapackage.json",
    "[TIDES-governance]":"governance.md",
    "[TIDES-board]":"governance.md#tides-board-of-directors",
    "[TIDES-contributor]":"governance.md#tides-contributor",
    "[TIDES-manager]":"governance.md#tides-manager",
    "[TIDES-stakeholder]":"governance.md#tides-stakeholder",
    "[`tides.spec.json`]": f"{GITHUB_REPO}/spec/tides.spec.json"
}

# The pattern to match markdown links like [Architecture]:./architecture
MD_LINK_DEF_REGEX = re.compile(r'^(\[[^\]]+\]):\s*(.+)$', re.MULTILINE)
MD_LINK_USE_REGEX = re.compile(r'\[(.*?)\]\s*\[([^\]]*?)\](?:(?!\n\n).)*\[\2\]:\s*(\S+)')
MD_HEADING_REGEX = re.compile(r'^(#{1,6})\s+(.*)', re.MULTILINE)

def split_yaml_header(text:str,delimeter:str = '---'):
    """Splits text (i.e. a markdown file) into structured yaml frontmatter and text.
    """
    _,y,t = text.split(delimeter)
    y = yaml.safe_load(y)
    return y,t

def get_git_branch_name():
    import subprocess
    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()
    log.info(f"On branch: {branch}")
    return branch

def downshift_md_heading(content_md:str):
    """Downshift heading level in markdown content by 1.

    Args:
        content_md (str): Markdown content
    """
    def _downshift_headings_in_match(match):
        heading = match.group(0)
        # Add a '#' to the heading, but only if it's not already an h6.
        if heading.count('#') < 6:
            return '#' + heading
        return heading

    content_md = re.sub(MD_HEADING_REGEX, _downshift_headings_in_match, content_md)
    return content_md

def replace_links_in_markdown(content_md:str, replacement_links:dict = UPDATE_LINKS):
    """Replace links in a markdown document. 

    Args:
        content_md (str): Markdown content to replace links for.
        replacement_links (dict, optional): Dictionary with links to update in a markdown document. 
            key: link handle (e.g. '[code of conduct]')
            value: updated link target (e.g. `code_of_conduct.md`)
            Defaults to UPDATE_LINKS.
    """
    MD_LINK_DEF_REGEX = re.compile(r'^(\[[^\]]+\]):\s*(.+)$', re.MULTILINE)
    def _replace_defs_in_match(match):
        #log.info(f"REPLACE DEFS MATCH: {match}")
        key = match.group(1)
        # If the key in the markdown matches one in our dictionary, replace it
        if key in replacement_links:
            return f"{key}: {replacement_links[key]}"
        else:
            return match.group(0)  # No replacement found, return the original text

    # Replace all occurrences in the content
    content_md = re.sub(MD_LINK_DEF_REGEX,_replace_defs_in_match, content_md)
    return content_md

def list_to_file_list(input_list: Union[str,list[str]], glob_pattern = '*') -> list[str]:
    all_files = []
    if type(input_list) is str:
        input_list = [input_list]

    for item in input_list:
        # If item is a file, add it to the list
        if os.path.isfile(item):
            all_files.append(item)
        # If item is a directory, add all files from that directory
        elif os.path.isdir(item):
            all_files+=glob.glob(os.path.join(item, glob_pattern))
        else:
            log.warning(f"{item} is neither a file nor a directory")
    return all_files

def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """
    @env.macro
    def list_actions(files: Union[str,list[str]]):
        filepaths = list_to_file_list(files, glob_pattern='*.md')

        def _fmt_action_to_admon(action:dict,adm_type = "abstract"):
            _indent = " "*4
            _nl = "\n"
            title = f'"{action["date"]} {action["title"]}"' 
            a = f"??? {adm_type} {title}\n\n"
            if "via" in action:
                a += f"\n{_indent}:material-file-check: {action['via']}"
            if "loc" in action:
                a += f"\n{_indent}:material-folder-open: [full document]({action['loc']})"
    
            _indented_md = f"{_indent}{action['md_txt'].replace(_nl, f'{_nl}{_indent}')}"
            a += _indented_md
            
            return a

        actions = []
        for fp in filepaths:
            with open(fp,'r') as f:
                action,md_txt = split_yaml_header(f.read())
                action['md_txt'] = md_txt
            actions.append(action)
        
        actions.sort(
            key=lambda x: x['date'] if 
                    isinstance(x['date'], date) 
                else 
                    datetime.strptime(x['date'], '%Y-%m-%d'), 
            reverse=True
        )
        adm = [_fmt_action_to_admon(x) for x in actions]
        
        return '\n'.join(adm)


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
    def include_file_sections(
        filename: str,
        include_sections: list[str] = [],
        exclude_sections: list[str] = [],
        downshift_h1=True,
        start_line: int = 0,
        end_line: int = None,
        code_type: str = None,
    ):
        """Wrapper around include_file to only include some sections.

        Args:
            filename (str): _description_
            sections: list of sections to include in order If not found will skip.
            downshift_h1 (bool, optional): _description_. Defaults to True.
            start_line (int, optional): _description_. Defaults to 0.
            end_line (int, optional): _description_. Defaults to None.
            code_type (str, optional): _description_. Defaults to None.
        """

        full_file_md = include_file(filename,downshift_h1,start_line,end_line,code_type)
        link_definitions = MD_LINK_DEF_REGEX.findall(full_file_md)
        #log.info(f"LINK DEFS:\n{link_definitions}")
        # Normalize titles for comparison
        include_titles = set(title.lower().strip() for title in include_sections)
        exclude_titles = set(title.lower().strip() for title in exclude_sections)

        # Check for conflicts between include and exclude lists
        if not include_titles.isdisjoint(exclude_titles):
            conflicting_titles = include_titles.intersection(exclude_titles)
            raise ValueError(f"Conflicting section titles to include and exclude: {conflicting_titles}")

        # Split the markdown content by headings to process sections
        parts = re.split(MD_HEADING_REGEX, full_file_md)
        parts=parts[1:]

        # Process in triples: (level, title, content)
        sections = []
        for i in range(0, len(parts), 3):
            level, title, content = parts[i:i+3]
            sections.append((level, title.strip(), content.strip()))
        
        # Extract the desired sections
        extracted_content = []
        for level, title, content in sections:
            title_lower = title.lower()
            if (title_lower in include_titles or not include_titles) and title_lower not in exclude_titles:
                extracted_content.append(f"{level} {title}")
                extracted_content.append(content)

        # Append all link definitions
        link_content = ""
        for link_label, link_href in link_definitions:
            link_content += f"\n{link_label}: {link_href}\n"
        extracted_content.append(link_content)
       
        return "\n\n".join(extracted_content)

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

        if downshift_h1 and re.search(r'^#\s', content, re.MULTILINE):
            content = downshift_md_heading(content)

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
