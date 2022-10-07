# Example TIDES Data Package

## Structure

The structure of a TIDES Data Package follows the [Frictionless Data Package specification](https://specs.frictionlessdata.io/data-package/), including:

- `\data`: formatted TIDES data
- `\scripts`: scripts to create, manipulate, or use TIDES data
- `datapackage.json`: data package metadata

## Validate Data

```bash
pip install frictionless
frictionless validate path/to/your/datapackage.json
```
