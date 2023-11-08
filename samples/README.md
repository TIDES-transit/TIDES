# Samples Directory Organization

Each TIDES Data Package example should follow the following directory structure, consistent with the structure of the [Frictionless Data Package specification](https://specs.frictionlessdata.io/data-package/), including:

```sh
unique-example-name
  \TIDES     # Required. Data to be validated against the TIDES specification
  \datapackage.json # Required. [`tides-data-package`](#tides-data-package) metadata
  \raw      # Optional. Data which the agency uses to create TIDES data
  \scripts  # Optional. Scripts used to transform raw --> TIDES
```

[tides-datapackage-profile]:.docs/datapackage
[tides-datapackage-profile-json]:.spec/tides-datapackage-profile.json
[template-datapackage]:./samples/template/TIDES/datapackage.json"

## Adding Examples

We encourage the addition of examples, but please follow the following guidelines:

1. *No large files* This isn't the place to store your data, rather to document some minimal examples.  The recommended size is 100-1000 records per file, more if absolutely required to reproduce an issue with the spec.  All individual files should be well under 50 MB.  
2. *Include Metadata* as specified in [tides-data-package](#data-package).
3. *Include a README.md* in the base folder of your example with an overview so that it can be included in the documentation.

## Data Package

TIDES sample data must include a [`datapackage.json`][tides-datapackage-profile] in the format specified by the [`tides-data-package` json schema][tides-datapackage-profile-json] (an extension of the [frictionless data package](https://specs.frictionlessdata.io/data-package/)).  

See:

- [Full documentation on the `tides-data-package`][tides-datapackage-profile]
- [Example `tides-data-package` file][template-datapackage]

## Data validation

Data with a valid [`datapackage.json`](#data-package) can be easily validated using the [frictionless framework](https://framework.frictionlessdata.io/), which can be installed and invoked as follows:

```bash
pip install frictionless
frictionless validate --schema-sync path/to/your/datapackage.json
```

Alternatively, we also provide a wrapper script to provide some additional flexibility and options.

Usage: `bin/validate-datapackage [-v remote_spec_ref | -l local_spec_path] [-d dataset_path]`

- `-r remote_spec_ref`: Optional. Specify the ref name of the GitHub repository for validating agianst
    a remote profile. Should not be used with -l option. Example: `-r main`
- `-l local_spec_path`: Optional. Specify the path of the local schema directory.
    Default is 'spec'. Is only used if remote_spec_ref = local.
- `-d dataset_path`: Optional. Specify the path of the TIDES datapackage.json.
    Default is the current directory.

Key usage examples:

- `bin/validate-datapackage -l spec -d samples/<my_samples>/TIDES`: Validate my sample data to a version of the spec located in the `/spec` directory.
- `bin/validate-datapackage -r main -d samples/<my_samples>/TIDES`: Validate my sample data to the canonical version of the TIDES spec.
- `bin/validate-datapackage -r v1.0 -d samples/<my_samples>/TIDES`: Validate my sample data to v1.0 of the spec.
- `bin/validate-datapackage -r develop -d samples/<my_samples>/TIDES`: Validate my sample data to the current `develop` branch of the TIDES spc.

If you **only** want to validate your `datapackage.json` file and not the datapackage as a whole, you can run the script `bin/validate-datapackage-to-profile` instead with the same options. Note that this is also run as a part of `validate-datapackage`.

### Specific files

Specific files can be validated by running the frictionless framework against them and their corresponding schemas as follows:

```sh
frictionless validate vehicles.csv --schema https://raw.githubusercontent.com/TIDES-transit/TIDES/main/spec/vehicles.schema.json
```

### Continuous Data Validation

Sample data in the `\TIDES` subdirectories of each sample is validated upon a push action to the main repository.
