
import glob
import json
import os
import pathlib

import pandas as pd

def _format_cell_by_type(x,header):
    if "enum" in header  and len(x)>1:
        return "Allowed Values: `"+",".join(map(str,x))+"`"
    if header is "foreign_key" and len(x)>1:
        table, var = x.split(".")
        if table == "":
            return "Variable: `{}`".format(var)
        return "Table: `{}`, Variable: `{}`".format(table, var)
    else:
        return str(x)

def _recursive_items(d: dict, key_prefix: str=''):
    """
    Recursively flattens a nested dictionary and returns a dictionary with key_prefixe
    to represent original nesting structures.
    Modified from https://stackoverflow.com/questions/39233973/get-all-keys-of-a-nested-dictionary
    """
    for k,v in d.items():
        if type(v) is dict:
            yield from _recursive_items(v,key_prefix=k+" ")
        elif k=="required":
            yield (k,v)
        else:
            yield (key_prefix+k,v)


def _replace_in_txt(txt_file: str,replacement_string: str , orig_string: str = '{{ REPLACE }}'):
    """Replaces contents of a txt file.

    Args:
        txt_file (str): file that you are writing to, based on a file with "template" as a pre-suffix.
        replacement_string (str): what you want to add in place of orig_string
        orig_string (str, optional):What you want to replace. Defaults to '{{ REPLACE }}'.
    """    
    txt_file_path = pathlib.Path(txt_file)
    _template_filename = pathlib.Path(txt_file_path.stem + ".template" + txt_file_path.suffix)
    txt_file_template_path = txt_file_path.parent / _template_filename

    with open(txt_file_template_path) as _template_file:
        _txt_contents = _template_file.read()

    if orig_string not in _txt_contents:
        raise ValueError(f"Couldn't find replacemen_string {orig_string} in txt_file: {txt_file_template_path}.")

    _updated_txt_contents = _txt_contents.replace(orig_string,replacement_string)

    with open(os.path.join(txt_file_path),"w") as _outfile:
        _outfile.write(_updated_txt_contents)



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
        flat_list.append({k:v for k,v in _recursive_items(i)})

    # get all items listed
    standard_header_items =  ["name","required","type","foreign_key","description",]
    additional_header_items = list(set([k for i in flat_list for k,v in i.items()])-set(standard_header_items))
    header_items = standard_header_items + sorted(additional_header_items)

    header_md = "|"+"|".join(header_items)+"|\n"
    header_md += "|---"*len(header_items)+"|\n"

    body_md = ''
    for d in flat_list:
        body_md += "|" + "|".join([_format_cell_by_type(d.get(i,"-"),i) for i in header_items]) +  "|\n"

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

def read_config(config_file: str, data_dir: str = "", schema_dir: str = "") -> pd.DataFrame:
    """
    Reads a frictionliess config file, adds some full paths and returns as a dataframe.
    Args:
        config_file: Configuration file. A json file with a list of "resources"
            specifying the "name", "path", and "schema" for each GMNS table as
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
    with open(config_file, encoding="utf-8") as f:
        config = json.load(f)
    ## todo validate config
    resource_dict = {i["name"]: i for i in config["resources"]}
    # print(config["resources"])

    resource_df = pd.DataFrame(config["resources"])
    resource_df["required"].fillna(False, inplace=True)

    print(resource_df)

    # Add full paths to data files
    if not data_dir:
        data_dir = os.path.dirname(config_file)
    resource_df["fullpath"] = resource_df["path"].apply(
        lambda x: os.path.join(data_dir, x)
    )

    # Add full paths to data files
    if not schema_dir:
        schema_dir = os.path.dirname(config_file)
    resource_df["fullpath_schema"] = resource_df["schema"].apply(
        lambda x: os.path.join(schema_dir, x)
    )
    print(resource_df)

    resource_df.set_index("name", drop=False, inplace=True)
    return resource_df

def document_schemas(base_path:str = '', spec_dir: str = 'spec', docs_path: str = ''):
    """_summary_

    Args:
        spec_path (str, optional): _description_. Defaults to ''.
        out_path (str, optional): _description_. Defaults to ''.
    """
    print("DOCUMENTING SCHEMA")
    
    if not base_path: base_path =  os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if not docs_path: docs_path = os.path.join(base_path,"docs")
    spec_path = os.path.join(base_path, spec_dir)

    print("Looking for specs in: {}".format(spec_path))

    # Create markdown with a table for each schema file
    
    schema_files = glob.glob(os.path.join(base_path,"**/*.schema.json"), recursive=True)
    print("files: {}".format(schema_files))

    file_schema_markdown =  ""
    for s in schema_files:
        print("Documenting Schema: {}".format(s))
        spec_name = s.split("/")[-1].split(".")[0]
        schema = read_schema(s)
        file_schema_markdown+="\n\n## {}\n".format(spec_name)
        file_schema_markdown+="\n\n{}".format(_list_to_md_table(schema["fields"]))

    _schema_documentation_file = os.path.join(docs_path,"tables.md")
    _replace_in_txt(_schema_documentation_file, file_schema_markdown)

def document_spec(base_path:str = '', spec_dir: str = 'spec', docs_path: str = ''):
    """_summary_

    Args:
        spec_path (str, optional): _description_. Defaults to ''.
        docs_path (str, optional): _description_. Defaults to ''.
    """
    print("DOCUMENTING SPEC")
    
    if not base_path: base_path =  os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if not docs_path: docs_path = os.path.join(base_path,"docs")
    spec_path = os.path.join(base_path, spec_dir)
    print("base_path: ",base_path)
    # Generate a table for overall file requirements
    spec_file = glob.glob(os.path.join(base_path,"**/*.spec.json"), recursive=True)[0]
    print("spec_file: ",spec_file)
    spec_df   = read_config(spec_file)
    spec_df   = spec_df.drop(columns=["fullpath","fullpath_schema","path","schema","name"]).reset_index()
    spec_df["name"]=spec_df["name"].apply(lambda x: "[`{}`](tables.md#{})".format(x,x))

    spec_markdown = spec_df.to_markdown(index=False)

    # Write it out to file
    _spec_documentation_file = os.path.join(docs_path,"architecture.md")
    print("spec_documentation_file: ",_spec_documentation_file)
    _replace_in_txt(_spec_documentation_file, spec_markdown)

if __name__ == "__main__":
    document_spec()
    document_schemas()