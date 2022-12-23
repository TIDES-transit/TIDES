# Example TIDES Data Package

Template directory for example scaffolding and helper scripts.

## Scripts for Generating Template Data

`scripts\create_template.py` has some template code which can help with the following

- `write_schema_examples()`: will generate blank csvs according to the TIDES schema
- `write_datapackage()` will generate a datapackage.json based on the TIDES schemas and a set of defaults specified in th script.

To run both (note this replaces the existing files in the directory)

```bash
python samples/template/scripts/create_template.py
```
