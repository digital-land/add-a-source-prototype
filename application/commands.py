import csv
import glob
import logging
import os
import pathlib
import tempfile
from datetime import datetime
from zipfile import ZipFile

import click
import requests
from flask.cli import AppGroup

from application.db.models import Endpoint, Pipeline, Source

logger = logging.getLogger(__name__)

# Create handlers
info_handler = logging.StreamHandler()
error_handler = logging.FileHandler("error.log")
info_handler.setLevel(logging.INFO)
error_handler.setLevel(logging.ERROR)

logger.addHandler(info_handler)
logger.addHandler(error_handler)

management_cli = AppGroup("manage")

DIGITAL_LAND_DATASETTE = "https://datasette.planning.data.gov.uk/digital-land"
DIGITAL_LAND_RAW_GITHUB_URL = "https://raw.githubusercontent.com/digital-land"

reference_tables = [
    "attribution",
    "licence",
    "typology",
    "datatype",
    "field",
    "organisation",
    "dataset",
    "dataset_field",
]


foreign_key_columns = set(
    [
        "dataset",
        "endpoint",
        "datatype",
        "typology",
        "dataset",
        "field",
        "licence",
        "attribution",
        "organisation",
        "pipeline",
    ]
)


@management_cli.command("load-data")
@click.option("--reference", default=False, help="Load just specification tables")
@click.option("--config", default=False, help="Load config tables")
def load_data(reference, config):
    from application.extensions import db

    if reference:
        for table in reference_tables:
            _load_reference_data(db, table)

    if config:
        _load_config(db)


@management_cli.command("drop-data")
def drop_data():
    from application.extensions import db

    for table in reversed(db.metadata.sorted_tables):
        delete = table.delete()
        try:
            db.engine.execute(delete)
        except Exception as e:
            logger.exception(e)


def _load_reference_data(db, table):
    url = f"{DIGITAL_LAND_DATASETTE}/{table}.json?_shape=array"
    logger.info(f"loading from {url}")

    records = []
    while url:
        resp = requests.get(url)
        try:
            url = resp.links.get("next").get("url")
        except AttributeError:
            url = None
        records.extend(resp.json())

    for record in records:
        if table in ["attribution", "licence"]:
            if "entity" in record.keys():
                del record["entity"]

        for key, val in record.items():
            if not val:
                record[key] = None
                continue
            if "date" in key:
                if not val:
                    record[key] = None
                else:
                    try:
                        record[key] = datetime.strptime(val, "%Y-%m-%d").date()
                    except Exception as e:
                        logger.exception(e)
                        record[key] = None

        insert_record = {}
        for key, val in record.items():
            if key == "rowid":
                continue
            if key != table and key in foreign_key_columns:
                f_key = f"{key}_id"
                insert_record[f_key] = val
            else:
                insert_record[key] = val
        try:
            t = db.metadata.tables.get(table)
            insert = t.insert().values(**insert_record)
            db.engine.execute(insert)
        except Exception as e:
            logger.exception(e)
            logger.exception(f"error loading {table} with data {record}")

    logger.info(f"inserted {len(records)} records into {table}")


def _load_config(db):
    config_zip_url = (
        "https://github.com/digital-land/config/archive/refs/heads/main.zip"
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        logger.info(f"Created temp directory {tmp_dir}")

        resp = requests.get(config_zip_url)
        zip_file_path = os.path.join(tmp_dir, "main.zip")

        with open(zip_file_path, "wb") as f:
            f.write(resp.content)

        with ZipFile(zip_file_path) as config_zip:
            config_zip.extractall(path=tmp_dir)

        pipeline_dir = os.path.join(tmp_dir, "config-main", "pipeline")
        pipelines = os.listdir(pipeline_dir)

        for p in pipelines:
            pipeline_path = os.path.join(pipeline_dir, p)
            logger.info(f"pipleline path {pipeline_path}")

            pipeline = Pipeline.query.get(p)
            if pipeline is None:
                name = p.replace("-", " ").capitalize()
                pipeline = Pipeline(pipeline=p, name=name, dataset_id=p)
                db.session.add(pipeline)
                db.session.commit()

            endpoint_file = f"{pipeline_path}/endpoint.csv"

            if os.path.exists(endpoint_file):
                with open(endpoint_file, "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        endpoint_id = row["endpoint"]
                        if Endpoint.query.get(endpoint_id) is None:
                            insert_copy = _get_insert_copy(row, "endpoint")
                            try:
                                endpoint = Endpoint(**insert_copy)
                                db.session.add(endpoint)
                                db.session.commit()
                            except Exception as e:
                                logger.exception(e)
                                logger.error(f"could not insert endpoint {row}")
                                logger.error(e)

            source_file = f"{pipeline_path}/source.csv"
            if os.path.exists(source_file):
                with open(source_file, "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        source_id = row["source"]
                        endpoint_id = row["endpoint"]
                        if endpoint_id.strip() != "":
                            if Endpoint.query.get(endpoint_id) is None:
                                message = f"Can't add source that doesn't link to endpoint {row}"
                                logger.error(message)
                                continue
                        source = Source.query.get(source_id)
                        if source is None:
                            # TODO - fix licence and attribution missing from reference data
                            insert_copy = _get_insert_copy(
                                row,
                                "source",
                                skip_fields=[
                                    "collection",
                                    "pipeline",
                                    "attribution",
                                    "licence",
                                ],
                            )
                            try:
                                source = Source(**insert_copy)
                                db.session.add(source)
                                pipeline.sources.append(source)
                                db.session.commit()

                            except Exception as e:
                                message = f"could not save source {insert_copy} for pipeline {p}"
                                logger.exception(e)
                                logger.error(message)
                                db.session.rollback()
                                continue

            # load the rest of the config files
            files = [
                file
                for file in glob.glob(f"{pipeline_path}/*.csv")
                if pathlib.Path(file).name
                not in ["source.csv", "endpoint.csv", "lookup.csv"]
            ]

            for file in files:
                path = pathlib.Path(file)
                logger.info(f" processing {path.name} for {p}")
                table_name = path.stem.replace("-", "_")
                table = db.metadata.tables.get(table_name)
                if table is not None:
                    with open(file) as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            try:
                                insert_record = _get_insert_copy(row, path.stem)
                                insert_record["pipeline_id"] = p
                                insert = table.insert().values(**insert_record)
                                db.engine.execute(insert)
                                logger.info(f"inserted: {insert}")
                            except Exception as e:
                                logger.error(e)
                                logger.error(
                                    f"could not insert into table {table_name}: {insert_record}"
                                )

            lookup_files = glob.glob(f"{pipeline_path}/lookup.csv")

            for file in lookup_files:
                path = pathlib.Path(file)
                logger.info(f" processing {path.name} for {p}")
                with open(file) as f:
                    reader = csv.reader(f)
                    fields = next(reader)
                    fields = [field.replace("-", "_") for field in fields]
                    fieldnames = []
                    for field in fields:
                        if field in ["organisation", "endpoint"]:
                            field = f"{field}_id"
                        fieldnames.append(field)
                    fieldnames.extend(["dataset_id", "pipeline_id"])
                    rows = list(reader)
                    update_header_path = f"{file}.tmp"
                    with open(update_header_path, "w") as out:
                        writer = csv.writer(out)
                        writer.writerow(fieldnames)
                        for row in rows:
                            row.extend([p, p])
                            writer.writerow(row)

                # run pg copy for lookup files due to number of records
                import psycopg2

                connection = psycopg2.connect(os.getenv("DATABASE_URL"))
                cursor = connection.cursor()
                with open(update_header_path) as f:
                    # cursor.copy_from(f, "lookup", columns=fieldnames, sep=",")
                    copy_command = f"COPY lookup({','.join(fieldnames)}) FROM STDIN WITH HEADER CSV"
                    cursor.copy_expert(copy_command, f)
                    connection.commit()
                    connection.close()

        logger.info("done")


def _get_insert_copy(row, current_file_key, skip_fields=[]):
    insert_copy = {}
    for key, val in row.items():
        if key in skip_fields:
            continue
        if key != current_file_key and key in foreign_key_columns:
            k = f"{key}_id"
        else:
            k = key
        k = k.replace("-", "_")
        if val is None or val.strip() == "":
            insert_copy[k] = None
        else:
            insert_copy[k] = val
        if "date" in k:
            insert_copy[k] = _parse_date(val, row)
    return insert_copy


def _parse_date(value, row):
    if value.strip() == "":
        return None
    try:
        date = datetime.strptime(value, "%Y-%m-%d").date()
        return date
    except Exception as e:
        logger.exception(e)
        logger.exception(row)

    try:
        date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").date()
        return date
    except Exception as e:
        logger.exception(e)
        logger.exception(row)

    try:
        date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S:%fZ").date()
        return date
    except Exception as e:
        logger.exception(e)
        logger.exception(row)

    logger.error(f"no date parsed for {row} using value {value}")

    return None
