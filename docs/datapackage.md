# Data Package

TIDES data must include a `datapackage.json` in the format specified by the [`tides-data-package` json schema](https://raw.githubusercontent.com/TIDES-transit/TIDES/main/spec/tides-datapackage-profile.json), which is an extension of the [frictionless data package](https://specs.frictionlessdata.io/data-package/) schema.

You may create your own `datapackage.json` based on the documentaiton or start with the provided [template](#template), but don't forget to [validate](#validation) it to make sure it is in the correct format!

## Data Package Format

{{ frictionless_data_package('spec/tides-datapackage-profile.json') }}

## Tabular Data Resource

Required and recommended fields for each `tabluar-data-resource` are as follows:

{{ frictionless_data_package('spec/tides-datapackage-profile.json',sub_schema="resources") }}

## Template

The canonical `datapackage.json` template is available at [`/data/template/TIDES/datapackage.json`](https://raw.githubusercontent.com/TIDES-transit/TIDES/main/samples/template/TIDES/datapackage.json).

!!! warning
    This version of `tides-data-package` template is dependent on the version of the documentation you are viewing and only represents the canonical `tides-data-package` template if you are viewing the `main` documentation version.

{{ include_file('samples/template/TIDES/datapackage.json',code_type='json') }}

## Validation

There are lots of options for validating your `datapackage.json` file including:

- [Command Line Interface (CLI) Script](#cli)
- [Various online websites](#point-and-drool)

### CLI

You can easily validate your data package file with the script provided in [`/bin/validate-data-package-json`](https://raw.githubusercontent.com/TIDES-transit/TIDES/main/bin/validate-data-package-json)

??? tip "installation requirements"

    Make sure you have jsonschema-cli installed. You can install it specifically or with all of the other suggested tools using one of the commands below:

    ```sh
    pip install jsonschema-cli
    pip install -r requirements.txt
    ```

```sh title="usage"
validate-data-package-json -f my-datapackage.json
```

{{ include_file('bin/validate-data-package-json',code_type='sh') }}

### Point-and-Drool

Because a `tides-datapackage-profile` is just a json-schema, you can use the myriad of different json-schema validator out there on the web.  Use the [canonical `tides-datapackage-profile`](https://raw.githubusercontent.com/TIDES-transit/TIDES/main/spec/tides-datapackage-profile.json) or copy and paste the version from below.

!!! warning
    This version of `tides-datapackage-profile` is dependent on the version of the documentation you are viewing and only represents the canonical `tides-datapackage-profile` if you are viewing the `main` documentation version.

{{ include_file('spec/tides-datapackage-profile.json',code_type='json') }}
