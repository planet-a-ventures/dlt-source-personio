import dlt
from dlt_source_personio import source

DEV_MODE = True


def load_personio_data() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="personio_pipeline", destination="duckdb", dev_mode=DEV_MODE
    )
    data = source(
        limit=-1 if not DEV_MODE else 1,
    )
    info = pipeline.run(
        data,
        refresh="drop_sources" if DEV_MODE else None,
        # we need this in case new resources, etc. are added
        schema_contract={"columns": "evolve"},
    )
    print(info)


if __name__ == "__main__":
    load_personio_data()
