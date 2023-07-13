# Data Package

TIDES data must include a `datapackage.json` in the format specified by the [`tides-data-package` json schema](https://raw.githubusercontent.com/TIDES-transit/TIDES/main/spec/tides-data-package.json), which is an extension of the [frictionless data package](https://specs.frictionlessdata.io/data-package/) schema.

You may create your own `datapackage.json` based on the documentaiton or start with the provided [template](#template), but don't forget to [validate](#validation) it to make sure it is in the correct format!

## Data Package Format

{{ frictionless_data_package('spec/tides-data-package.json') }}

## Tabular Data Resource

Required and recommended fields for each `tabluar-data-resource` are as follows:

{{ frictionless_data_package('spec/tides-data-package.json',sub_schema="resources") }}

## Template

A `datapackage.json` template is available at [`/data/template/TIDES/datapackage.json`](https://raw.githubusercontent.com/TIDES-transit/TIDES/main/data/template/TIDES/datapackage.json).

Once `datapackage.json` is created for your data, you can easily conduct [data validation](#validation) using a variet of tools.

## Validation
