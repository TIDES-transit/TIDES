# TIDES

Transit ITS Data Exchange Specification (TIDES) for historical transit operation data.

This repository provides data schemas and tools to support the access, management, and improvement of historical transit operations data, including vehicle operations, passenger activity, fare collection, and other similar data.

## TIDES specification

The TIDES specification is maintained in the `/spec` sub-directory as a series of JSON tables compatible with the [frictionless data](https://specs.frictionlessdata.io/table-schema/) table schema and [data package](https://specs.frictionlessdata.io/data-package) standards.
Human-friendlier documentation is auto-generated and available at:

- [Architecture](architecture.md)
- [Table Schemas](tables.md)

## Example Data

Sample data can be found in the `/samples` directory, with one directory for each example.  

## Validating TIDES data

TIDES data with a valid [`datapackage.json`](#data-package) can be easily validated using the [frictionless framework](https://framework.frictionlessdata.io/), which can be installed and invoke as follows:

```bash
pip install frictionless
frictionless validate path/to/your/datapackage.json
```

### Data Package

To validate a package of TIDES data, you must add a frictionless-compliant [`datapackage.json`](https://specs.frictionlessdata.io/data-package/) alongside your data which describes which files should be validated to which schemas.  Most of this can be copied from [`/data/template/datapackage.json`](https://raw.githubusercontent.com/TIDES-transit/TIDES/main/data/template/datapackage.json).

Once this is created, mapping the data files to the schema, simply run:

```sh
frictionless validate datapackage.json
```

### Specific files

Specific files can be validated by running the frictionless framework against them and their corresponding schemas as follows:

```sh
frictionless validate vehicles.csv --schema https://raw.githubusercontent.com/TIDES-transit/TIDES/main/spec/schema.vehicles.json
```

## Contributing to TIDES

Those who want to help with the development of the TIDES specification should review the guidance in <CONTRIBUTING.md>.

## Issues

Please add issues, bugs, and feature requests to [GitHub](https://github.com/TIDES-transit/TIDES/issues).

## Acknowledgment

These data schemas and tool definitions developed here are based on the results of research conducted by the Transportation Research Board (TRB) of the National Academies of Science, Engineering, and Medicine (NASEM) under the Transit Cooperative Research Program (TCRP). This research is available at [the National Academies website](https://nap.nationalacademies.org/catalog/26674/improving-access-and-management-of-public-transit-its-data).

Note that neither the TIDES Project nor the TIDES-transit repository are associated with TCRP, TRB, or the Academies. The use of the TCRP research results in this repository do not reflect any explicit or implicit endorsement of or participation in this work by the Academies. In addition, the opinions and conclusions expressed or implied in the research are those of the contractor. They are not necessarily those of the Transportation Research Board, the Academies, or the program sponsors.
