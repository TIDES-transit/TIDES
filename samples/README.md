# Samples Directory Organization

Each TIDES Data Package example should follow the following directory structure, consistent with the structure of the [Frictionless Data Package specification](https://specs.frictionlessdata.io/data-package/), including:

```sh
unique-example-name
  \TIDES     # Required. Data to be validated against the TIDES specification
  \datapackage.json # Required. [`tides-data-package`](#tides-data-package) metadata
  \raw      # Optional. Data which the agency uses to create TIDES data
  \scripts  # Optional. Scripts used to transform raw --> TIDES
```

## Adding Examples

We encourage the addition of examples, but please follow the following guidelines:

1. *No large files* This isn't the place to store your data, rather to document some minimal examples.  The recommended size is 100-1000 records per file, more if absolutely required to reproduce an issue with the spec.  All individual files should be well under 50 MB.  
2. *Include Metadata* as specified in [tides-data-package](#data-package).
3. *Include a README.md* in the base folder of your example with an overview so that it can be included in the documentation.

## Data Package

TIDES sample data must include a `datapackage.json` in the format specified by the [`tides-data-package` json schema](https://raw.githubusercontent.com/TIDES-transit/TIDES/main/spec/tides-datapackage-profile.json) (an extension of the [frictionless data package](https://specs.frictionlessdata.io/data-package/)).  

See:

- [Full documentation on the `tides-data-package`]({{ site_url }}/datapackage)
- [Example `tides-data-package` file](https://raw.githubusercontent.com/TIDES-transit/TIDES/main/samples/template)

## Data validation

Data with a valid [`datapackage.json`](#data-package) can be easily validated using the [frictionless framework](https://framework.frictionlessdata.io/), which can be installed and invoked as follows:

```bash
pip install frictionless
frictionless validate --schema-sync path/to/your/datapackage.json
```

### Specific files

Specific files can be validated by running the frictionless framework against them and their corresponding schemas as follows:

```sh
frictionless validate vehicles.csv --schema https://raw.githubusercontent.com/TIDES-transit/TIDES/main/spec/vehicles.schema.json
```

### Continuous Data Validation

Sample data in the `\TIDES` subdirectories of each sample is validated upon a push action to the main repository.
