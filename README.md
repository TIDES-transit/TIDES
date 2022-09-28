# TIDES

Transit ITS Data Exchange Specification (TIDES) for historical transit operation data.

This repository provides data schemas and tools to support the access, management, and improvement of historical transit operations data, including vehicle operations, passenger activity, fare collection, and other similar data.

## TIDES specification

The TIDES specification is maintained in the `/spec` sub-directory as a series of JSON tables compatible with the [frictionless data](https://specs.frictionlessdata.io/table-schema/) table schema standards.
Human-friendlier documentation is auto-generated and available at:

- [Architecture](architecture.md)
- [Table Schemas](tables.md)

## Example Data

[![Example Data](https://github.com/TIDES-transit/TIDES/actions/workflows/validate-data.yaml/badge.svg)](https://repository.frictionlessdata.io/pages/dashboard.html?user=TIDES-transit&repo=TIDES&flow=validate-data)

Example data can be found in the `/data` directory, with one directory for each example.  

Example data in the `/TIDES` subdirectories is validated upon a push action to the main repository according to the `TIDES` schema contained in the respective repository commit.

## Contributing to TIDES

Those who want to help with the development of the TIDES specification should review the guidance in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Issues

Please add issues, bugs, and feature requests to [GitHub](https://github.com/TIDES-transit/TIDES/issues).

## Acknowledgment

These data schemas and tool definitions developed here are based on the results of research conducted by the Transportation Research Board (TRB) of the National Academies of Science, Engineering, and Medicine (NASEM) under the Transit Cooperative Research Program (TCRP). This research is available at [the National Academies website](https://nap.nationalacademies.org/catalog/26674/improving-access-and-management-of-public-transit-its-data).

Note that neither the TIDES Project nor the TIDES-transit repository are associated with TCRP, TRB, or the Academies. The use of the TCRP research results in this repository do not reflect any explicit or implicit endorsement of or participation in this work by the Academies. In addition, the opinions and conclusions expressed or implied in the research are those of the contractor. They are not necessarily those of the Transportation Research Board, the Academies, or the program sponsors.
