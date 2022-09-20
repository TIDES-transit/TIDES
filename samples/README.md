# Sample data

This directory contains sample data provided by agencies.

Data are organized into agency directories containing:

- metadata.yml: **required**, information about the agency, and the person responsible for maintaining the sample data. See format description below.
- TIDES: **required**, directory of data files in TIDES spec format. These files will be validated against proposed spec changes.
- data-raw: *optional*, directory of "raw" data from CAD/AVL vendor. What constitutes "raw" is up to the maintainer, for example, data extracted from a datamart with a star-schema could be provided as one fact table and the required dimensions tables (e.g., `fact_avl.csv`, `dim_stop.csv`, `dim_trip.csv`, etc.), mirroring the structure of the datamart, or just one table with dimension tables already joined to the fact table (e.g., `avl.csv`).
- scripts: *optional*, directory of scripts used to process data in `data-raw`. Scripts will not be run on GitHub, but are provided as starting points for others wishing to implement their own data processing routines. Scripts should read raw data from `data-raw` and write tables to `TIDES`. We recommend documenting your scripts so that someone unfamiliar with your process can understand them.
