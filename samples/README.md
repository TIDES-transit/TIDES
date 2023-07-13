# Data Directory Organization

Each TIDES Data Package example should follow the following directory structure, consistent with the structure of the [Frictionless Data Package specification](https://specs.frictionlessdata.io/data-package/), including:

```
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

TIDES data packages must include a `datapackage.json` in the format specified by the [`tides-data-package` json schema](https://raw.githubusercontent.com/TIDES-transit/TIDES/main/spec/tides-data-package.json) format (an extension of the [frictionless data package](https://specs.frictionlessdata.io/data-package/)).  Key information to include in `datapackage.json` includes:

| **Field** | **Description** | **Required** |
| --------- | --------------- | ------------ |
| `title` | A human-readable title. | Required |
| `name` | Identifier string as a URL-friendly slug. | Required |
| `description` | Short description of data package. | Recommended |
| `agency` | Transit agency name. | Recommended |
| `ntd_id` | ID for the National Transit Database. | Recommended |
| `profile` | Should be `tabular-data-package` | Required |
| `licenses` | Should be `[{"name": "Apache-2.0"}]` to be consistent with this repository | Required |
| `contributors` | Array of data contributors `[{"title": "My Name", "github": "my_handle", "email": "me@myself.com"}]` | Recommended |
| `maintainers` |  Array of data maintainers `[{"title": "My Name", "github": "my_handle", "email": "me@myself.com"}]` | Recommended |
| `resources` | Array of data files included in your package, formated as a [`tabular-data-resource`](#data-resource)| Required |

### Template

A `datapackage.json` template is available at [`/data/template/TIDES/datapackage.json`](https://raw.githubusercontent.com/TIDES-transit/TIDES/main/data/template/TIDES/datapackage.json).

Once `datapackage.json` is created for your data, you can easily conduct [data validation](#data-validation) using a variet of tools.

### Data Resource

Key fields for each [`tabular-data-resource`](https://specs.frictionlessdata.io/tabular-data-resource/) are as follows:

| **Field** | **Description** | **Required** |
| --------- | --------------- | ------------ |
| `name` | Short sluggable name used to refer to data in this file. | Required |
| `path` | Path of the data resource file relative to the `datapackage.json` | Required |
| `schema` | Data schema to use to valdiate the data resource to | Required |
| `sources` | Array of data sources formatted as a [`source`](#data-source) | Recommended |

### Data Source

| **Field** | **Description** | **Required** |
| --------- | --------------- | ------------ |
| `title` | Description of the data source. | Required |
| `component` | What technology component was used to generate this data (directly or indirectly)? Examples include `AVL`, `APC`, `AFC`, etc.  | Recommended |
| `product` | What product was used to generate this data (directly or indirectly)? | Recommended |
| `vendor` | What company makes this product? | Recommended |

## Data validation

Data with a valid [`datapackage.json`](#data-package) can be easily validated using the [frictionless framework](https://framework.frictionlessdata.io/), which can be installed and invoke as follows:

```bash
pip install frictionless
frictionless validate path/to/your/datapackage.json
```

### Specific files

Specific files can be validated by running the frictionless framework against them and their corresponding schemas as follows:

```sh
frictionless validate vehicles.csv --schema https://raw.githubusercontent.com/TIDES-transit/TIDES/main/spec/vehicles.schema.json
```

### Continuous Data Validation

Example data in the `\TIDES` subdirectories is validated upon a push action to the main repository according to the `TIDES` schema posted to the `main` branch.
