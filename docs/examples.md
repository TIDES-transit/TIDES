# Examples

[![Example Data](https://github.com/TIDES-transit/TIDES/actions/workflows/validate-data.yaml/badge.svg)](https://repository.frictionlessdata.io/pages/dashboard.html?user=TIDES-transit&repo=TIDES&flow=validate-data)

Example data can be found in the `/data` directory, with one directory for each example.  

## Example validation

Example data in the `\TIDES` subdirectories is validated upon a push action to the main repository according to the `TIDES` schema contained in the respective repository commit.

## Example Directory Organization

Each example should follow the following directory structure:

```
unique-example-name
  \TIDES    # data to be validated against the TIDES specification
  \raw      # data which the agency uses to create TIDES data
  \scripts  # scripts used to transform raw --> TIDES
```

## Example List

{{ testingme }}
