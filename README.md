---
description: dlt source for personio.com
keywords: [personio API, personio.com]
---

# dlt-source-personio

[![PyPI version](https://img.shields.io/pypi/v/dlt-source-personio)](https://pypi.org/project/dlt-source-personio/)

[DLT](https://dlthub.com/) source for [personio](https://www.personio.com/).

Currently loads the following data:

| Table | Contains | Spec version |
| -- | -- | -- |
| `persons` | Items of the `Person` model with all properties | `V2` |
| `persons_custom_attributes` | All defined custom attributes. The table is pivoted, so each custom attribute becomes a column in the table. | `V2` |
| `persons_profile_pictures` | The profile picture for each employee (that has defined one) | `V1` |
| `employments` | Items of the `Employment` model with all properties | `V2` |

## Why are you not using the `dlt-hub/verified-sources` personio source / Differences

The [official verified source](https://github.com/dlt-hub/verified-sources/tree/master/sources/personio)
has a few drawbacks:

- it is based on the Personio API V1, not the current V2
- on usage of the verified source, a copy of the current state of
  the `dlt-hub/verified-sources` repository is copied into your project;
  Once you make changes to it, it effectively becomes a fork,
  making it hard to update after the fact.
- The verified source does not use any data validation other than
  ensuring dates are correct; This means that data shape is not guaranteed,
  resulting in potential schema changes.
  This data source uses an (unofficial) OpenAPI spec, which is transformed
  into Pydantic 2 models.

Currently this data source does not support delta updates
(the verified source does) and it also does not contain some of the data
sources (absences, etc.). Contributions are welcome!

## Usage

Create a `.dlt/secrets.toml` with your API key and email:

```toml
personio_client_id = "papi-..."
personio_client_secret = "papi-..."
```

and then run the default source with optional list references:

```py
from dlt_source_personio import source as personio_source

pipeline = dlt.pipeline(
   pipeline_name="personio_pipeline",
   destination="duckdb",
   dev_mode=True,
)
personio_data = personio_source()
pipeline.run(personio_data)
```

## Development

This project is using [devenv](https://devenv.sh/).

Commands:

| Command | What does it do? |
| -- | -- |
| `generate-model` | generates the personio Pydantic model from the current spec file, applies patches, etc. |
| `update-spec` | Pulls in the latest `master#HEAD` of [personio/api-docs](https://github.com/personio/api-docs) |
| `validate-spec` | Validates the local (unofficial) Personio V2 spec |
| `refresh-model` | Both commands above plus adds it to git and commits the changes. |
| `format` | Formats & lints all code |
| `sample-pipeline-run` | Runs the sample pipeline. By default `dev_mode=True` which fetches resources with a limit of 1 (page) |
| `sample-pipeline-show` | Starts the streamlit-based dlt hub |

### Run the sample

```sh
PERSONIO_CLIENT_ID=[...] \
   PERSONIO_CLIENT_SECRET=[...] \
      sample-pipeline-run
```

alternatively you can also create a `.dlt/secrets.toml`
(excluded from git) with the following content:

```toml
personio_client_id = "papi-..."
personio_client_secret = "papi-..."
```
