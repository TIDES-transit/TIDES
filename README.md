# TIDES

Transit ITS Data Exchange Specification (TIDES) for historical transit operation data.

This repository provides data schemas and tools to support the access, management, and improvement of historical transit operations data, including vehicle operations, passenger activity, fare collection, and other similar data.

## TIDES specification

The TIDES specification is is a series of interrelated table schemas which are defined by a series of `<table_name>.schema.json` files in the `/spec` sub-directory in the [frictionless data table schema format](https://specs.frictionlessdata.io/table-schema/) and accompanied by [`tides-datapackage-profile.json`](https://tides-transit.github.io/TIDES/main/datapackage) which describes the schema of the required [datapackage.json](#data_package) file which must accompany TIDES data.

Human-friendlier documentation is auto-generated and available at:

- [Architecture](https://tides-transit.github.io/TIDES/main/architecture)
- [Table Schemas](https://tides-transit.github.io/TIDES/main/tables)

### Data Package

Directories with TIDES data must contain metadata in a [`datapackage.json`](https://tides-transit.github.io/TIDES/main/datapackage) file in a format compliant with the [`tides-datapackage-profile`](https://tides-transit.github.io/TIDES/main/datapackage) of a [`frictionless data package`](https://specs.frictionlessdata.io/data-package/).  

[`/samples/template/datapackage.json`](https://raw.githubusercontent.com/TIDES-transit/TIDES/main/samples/template/datapackage.json) has a template datapackage which can be used.

## Validating TIDES data

TIDES data with a valid [`datapackage.json`](#data-package) can be easily validated using the [frictionless framework](https://framework.frictionlessdata.io/), which can be installed and invoked as follows:

```bash
pip install frictionless
frictionless validate --schema-sync path/to/your/datapackage.json
```

Several other validation scripts and tools with more flexibility such as validating to the canonical, named version or a local spec can be found in the `/bin` directory, with usage available with the `--help` flag.

```bash
bin/validate-datapackage [-v remote_spec_ref | -l local_spec_path] [-d dataset_path]
```

### Specific files

Specific files can be validated by running the frictionless framework against them and their corresponding schemas as follows:

```sh
frictionless validate vehicles.csv --schema https://raw.githubusercontent.com/TIDES-transit/TIDES/main/spec/schema.vehicles.json --schema-sync
```

## Sample Data

[Sample data](https://tides-transit.github.io/TIDES/main/samples) can be found in the `/samples` directory, with one directory for each sample.

### Template

Templates of `datapackage.json` and each TIDES file type are located in the `/samples/template` directory. They can be used to build out TIDES data, particuarly samples.  Most TIDES data in practice will be directly produced as an output from software or scripts.

## Contributing to TIDES

Those who want to help with the development of the TIDES specification should review the guidance in [CONTRIBUTING.md](CONTRIBUTING.md).

## Issues

Please add issues, bugs, and feature requests to [GitHub](https://github.com/TIDES-transit/TIDES/issues).

## Acknowledgment

These data schemas and tool definitions developed here are based on the results of research conducted by the Transportation Research Board (TRB) of the National Academies of Science, Engineering, and Medicine (NASEM) under the Transit Cooperative Research Program (TCRP). This research is available at [the National Academies website](https://nap.nationalacademies.org/catalog/26674/improving-access-and-management-of-public-transit-its-data).

Note that neither the TIDES Project nor the TIDES-transit repository are associated with TCRP, TRB, or the Academies. The use of the TCRP research results in this repository do not reflect any explicit or implicit endorsement of or participation in this work by the Academies. In addition, the opinions and conclusions expressed or implied in the research are those of the contractor. They are not necessarily those of the Transportation Research Board, the Academies, or the program sponsors.
