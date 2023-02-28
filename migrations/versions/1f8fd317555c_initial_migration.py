"""initial migration

Revision ID: 1f8fd317555c
Revises:
Create Date: 2023-02-27 14:52:43.389006

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "1f8fd317555c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "attribution",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("attribution", sa.Text(), nullable=False),
        sa.Column("text", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("attribution"),
    )
    op.create_table(
        "datatype",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("datatype", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("text", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("datatype"),
    )
    op.create_table(
        "endpoint",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("endpoint", sa.Text(), nullable=False),
        sa.Column("endpoint_url", sa.Text(), nullable=True),
        sa.Column("parameters", sa.Text(), nullable=True),
        sa.Column("plugin", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("endpoint"),
    )
    op.create_table(
        "licence",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("licence", sa.Text(), nullable=False),
        sa.Column("text", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("licence"),
    )
    op.create_table(
        "organisation",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("organisation", sa.Text(), nullable=False),
        sa.Column("addressbase_custodian", sa.Text(), nullable=True),
        sa.Column("billing_authority", sa.Text(), nullable=True),
        sa.Column("census_area", sa.Text(), nullable=True),
        sa.Column("combined_authority", sa.Text(), nullable=True),
        sa.Column("company", sa.Text(), nullable=True),
        sa.Column("entity", sa.BigInteger(), nullable=True),
        sa.Column("esd_inventory", sa.Text(), nullable=True),
        sa.Column("local_authority_type", sa.Text(), nullable=True),
        sa.Column("local_resilience_forum", sa.Text(), nullable=True),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("official_name", sa.Text(), nullable=True),
        sa.Column("opendatacommunities_uri", sa.Text(), nullable=True),
        sa.Column("parliament_thesaurus", sa.Text(), nullable=True),
        sa.Column("prefix", sa.Text(), nullable=True),
        sa.Column("reference", sa.Text(), nullable=True),
        sa.Column("region", sa.Text(), nullable=True),
        sa.Column("shielding_hub", sa.Text(), nullable=True),
        sa.Column("statistical_geography", sa.Text(), nullable=True),
        sa.Column("twitter", sa.Text(), nullable=True),
        sa.Column("website", sa.Text(), nullable=True),
        sa.Column("wikidata", sa.Text(), nullable=True),
        sa.Column("wikipedia", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("organisation"),
    )
    op.create_table(
        "pipeline",
        sa.Column("pipeline", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("pipeline"),
    )
    op.create_table(
        "typology",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("typology", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("plural", sa.Text(), nullable=True),
        sa.Column("wikidata", sa.Text(), nullable=True),
        sa.Column("wikipedia", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("typology"),
    )
    op.create_table(
        "dataset",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("dataset", sa.Text(), nullable=False),
        sa.Column("attribution_id", sa.Text(), nullable=True),
        sa.Column("collection", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("key_field", sa.Text(), nullable=True),
        sa.Column("entity_minimum", sa.BigInteger(), nullable=True),
        sa.Column("entity_maximum", sa.BigInteger(), nullable=True),
        sa.Column("licence_id", sa.Text(), nullable=True),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column(
            "paint_options", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("plural", sa.Text(), nullable=True),
        sa.Column("prefix", sa.Text(), nullable=True),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("typology_id", sa.Text(), nullable=True),
        sa.Column("wikidata", sa.Text(), nullable=True),
        sa.Column("wikipedia", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["attribution_id"],
            ["attribution.attribution"],
        ),
        sa.ForeignKeyConstraint(
            ["licence_id"],
            ["licence.licence"],
        ),
        sa.ForeignKeyConstraint(
            ["typology_id"],
            ["typology.typology"],
        ),
        sa.PrimaryKeyConstraint("dataset"),
    )
    op.create_table(
        "field",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("field", sa.Text(), nullable=False),
        sa.Column("cardinality", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("guidance", sa.Text(), nullable=True),
        sa.Column("hint", sa.Text(), nullable=True),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("parent_field", sa.Text(), nullable=True),
        sa.Column("replacement_field", sa.Text(), nullable=True),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("uri_template", sa.Text(), nullable=True),
        sa.Column("wikidata_property", sa.Text(), nullable=True),
        sa.Column("datatype_id", sa.Text(), nullable=True),
        sa.Column("typology_id", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["datatype_id"],
            ["datatype.datatype"],
        ),
        sa.ForeignKeyConstraint(
            ["typology_id"],
            ["typology.typology"],
        ),
        sa.PrimaryKeyConstraint("field"),
    )
    op.create_table(
        "source",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("attribution_id", sa.Text(), nullable=True),
        sa.Column("documentation_url", sa.Text(), nullable=True),
        sa.Column("endpoint_id", sa.Text(), nullable=True),
        sa.Column("licence_id", sa.Text(), nullable=True),
        sa.Column("organisation_id", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["attribution_id"],
            ["attribution.attribution"],
        ),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.endpoint"],
        ),
        sa.ForeignKeyConstraint(
            ["licence_id"],
            ["licence.licence"],
        ),
        sa.ForeignKeyConstraint(
            ["organisation_id"],
            ["organisation.organisation"],
        ),
        sa.PrimaryKeyConstraint("source"),
    )
    op.create_table(
        "_default",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Text(), nullable=True),
        sa.Column("dataset_id", sa.Text(), nullable=True),
        sa.Column("endpoint_id", sa.Text(), nullable=True),
        sa.Column("resource", sa.Text(), nullable=True),
        sa.Column("field", sa.Text(), nullable=True),
        sa.Column("default_field", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.dataset"],
        ),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.endpoint"],
        ),
        sa.ForeignKeyConstraint(
            ["field"],
            ["field.field"],
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.pipeline"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "column",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Text(), nullable=True),
        sa.Column("dataset_id", sa.Text(), nullable=True),
        sa.Column("endpoint_id", sa.Text(), nullable=True),
        sa.Column("resource", sa.Text(), nullable=True),
        sa.Column("column", sa.Text(), nullable=True),
        sa.Column("field_id", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.dataset"],
        ),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.endpoint"],
        ),
        sa.ForeignKeyConstraint(
            ["field_id"],
            ["field.field"],
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.pipeline"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "combine",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline", sa.Text(), nullable=True),
        sa.Column("dataset_id", sa.Text(), nullable=True),
        sa.Column("endpoint_id", sa.Text(), nullable=True),
        sa.Column("resource", sa.Text(), nullable=True),
        sa.Column("field_id", sa.Text(), nullable=True),
        sa.Column("separator", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.dataset"],
        ),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.endpoint"],
        ),
        sa.ForeignKeyConstraint(
            ["field_id"],
            ["field.field"],
        ),
        sa.ForeignKeyConstraint(
            ["pipeline"],
            ["pipeline.pipeline"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "concat",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Text(), nullable=True),
        sa.Column("dataset_id", sa.Text(), nullable=True),
        sa.Column("endpoint_id", sa.Text(), nullable=True),
        sa.Column("resource", sa.Text(), nullable=True),
        sa.Column("field_id", sa.Text(), nullable=True),
        sa.Column("fields", sa.Text(), nullable=True),
        sa.Column("separator", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.dataset"],
        ),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.endpoint"],
        ),
        sa.ForeignKeyConstraint(
            ["field_id"],
            ["field.field"],
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.pipeline"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "convert",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Text(), nullable=True),
        sa.Column("dataset_id", sa.Text(), nullable=True),
        sa.Column("endpoint_id", sa.Text(), nullable=True),
        sa.Column("resource", sa.Text(), nullable=True),
        sa.Column("plugin", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.dataset"],
        ),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.endpoint"],
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.pipeline"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "dataset_field",
        sa.Column("dataset_id", sa.Text(), nullable=False),
        sa.Column("field_id", sa.Text(), nullable=False),
        sa.Column("hint", sa.Text(), nullable=True),
        sa.Column("guidance", sa.Text(), nullable=True),
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.dataset"],
        ),
        sa.ForeignKeyConstraint(
            ["field_id"],
            ["field.field"],
        ),
        sa.PrimaryKeyConstraint("dataset_id", "field_id"),
    )
    op.create_table(
        "default_value",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Text(), nullable=True),
        sa.Column("dataset_id", sa.Text(), nullable=True),
        sa.Column("endpoint_id", sa.Text(), nullable=True),
        sa.Column("resource", sa.Text(), nullable=True),
        sa.Column("field_id", sa.Text(), nullable=True),
        sa.Column("entry_number", sa.BigInteger(), nullable=True),
        sa.Column("value", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.dataset"],
        ),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.endpoint"],
        ),
        sa.ForeignKeyConstraint(
            ["field_id"],
            ["field.field"],
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.pipeline"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "filter",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Text(), nullable=True),
        sa.Column("dataset_id", sa.Text(), nullable=True),
        sa.Column("endpoint_id", sa.Text(), nullable=True),
        sa.Column("resource", sa.Text(), nullable=True),
        sa.Column("field", sa.Text(), nullable=True),
        sa.Column("pattern", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.dataset"],
        ),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.endpoint"],
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.pipeline"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "lookup",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Text(), nullable=True),
        sa.Column("dataset_id", sa.Text(), nullable=True),
        sa.Column("endpoint_id", sa.Text(), nullable=True),
        sa.Column("resource", sa.Text(), nullable=True),
        sa.Column("pattern", sa.Text(), nullable=True),
        sa.Column("entry_number", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.dataset"],
        ),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.endpoint"],
        ),
        sa.ForeignKeyConstraint(
            ["pattern"],
            ["field.field"],
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.pipeline"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "patch",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Text(), nullable=True),
        sa.Column("dataset_id", sa.Text(), nullable=True),
        sa.Column("endpoint_id", sa.Text(), nullable=True),
        sa.Column("resource", sa.Text(), nullable=True),
        sa.Column("field", sa.Text(), nullable=True),
        sa.Column("entry_number", sa.BigInteger(), nullable=True),
        sa.Column("pattern", sa.Text(), nullable=True),
        sa.Column("value", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.dataset"],
        ),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.endpoint"],
        ),
        sa.ForeignKeyConstraint(
            ["field"],
            ["field.field"],
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.pipeline"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "skip",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Text(), nullable=True),
        sa.Column("dataset_id", sa.Text(), nullable=True),
        sa.Column("endpoint_id", sa.Text(), nullable=True),
        sa.Column("pattern", sa.Text(), nullable=True),
        sa.Column("resource", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.dataset"],
        ),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.endpoint"],
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.pipeline"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "source_pipeline",
        sa.Column("pipeline_id", sa.Text(), nullable=True),
        sa.Column("source_id", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.pipeline"],
        ),
        sa.ForeignKeyConstraint(
            ["source_id"],
            ["source.source"],
        ),
    )
    op.create_table(
        "transform",
        sa.Column("entry_date", sa.TIMESTAMP(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pipeline_id", sa.Text(), nullable=True),
        sa.Column("dataset_id", sa.Text(), nullable=True),
        sa.Column("endpoint_id", sa.Text(), nullable=True),
        sa.Column("resource", sa.Text(), nullable=True),
        sa.Column("field", sa.Text(), nullable=True),
        sa.Column("replacement_field", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.dataset"],
        ),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.endpoint"],
        ),
        sa.ForeignKeyConstraint(
            ["field"],
            ["field.field"],
        ),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipeline.pipeline"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transform")
    op.drop_table("source_pipeline")
    op.drop_table("skip")
    op.drop_table("patch")
    op.drop_table("lookup")
    op.drop_table("filter")
    op.drop_table("default_value")
    op.drop_table("dataset_field")
    op.drop_table("convert")
    op.drop_table("concat")
    op.drop_table("combine")
    op.drop_table("column")
    op.drop_table("_default")
    op.drop_table("source")
    op.drop_table("field")
    op.drop_table("dataset")
    op.drop_table("typology")
    op.drop_table("pipeline")
    op.drop_table("organisation")
    op.drop_table("licence")
    op.drop_table("endpoint")
    op.drop_table("datatype")
    op.drop_table("attribution")
    # ### end Alembic commands ###
