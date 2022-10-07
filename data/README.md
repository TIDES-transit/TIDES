# Data Directory Organization

Each TIDES Data Package example should follow the following directory structure, consistent with the structure of the [Frictionless Data Package specification](https://specs.frictionlessdata.io/data-package/), including:

```
unique-example-name
  \data     # data to be validated against the TIDES specification
  \data\datapackages.json # data package metadata per https://specs.frictionlessdata.io/data-package/
  \raw      # data which the agency uses to create TIDES data
  \scripts  # scripts used to transform raw --> TIDES
```

## Data validation

Data with a valid `datapackage.json` can be easily validated using the [frictionless framework](https://framework.frictionlessdata.io/), which can be installed and invoke as follows:

```bash
pip install frictionless
frictionless validate path/to/your/datapackage.json
```

### Continuous Data Validation

Example data in the `\data` subdirectories is validated upon a push action to the main repository according to the `TIDES` schema posted to the `main` branch.
