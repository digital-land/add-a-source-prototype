from sqlalchemy.dialects.postgresql import JSON

from application.extensions import db


class Organisation(db.Model):

    organisation = db.Column(db.TEXT, primary_key=True, nullable=False)
    name = db.Column(db.TEXT)
    official_name = db.Column(db.TEXT)
    addressbase_custodian = db.Column(db.TEXT)
    billing_authority = db.Column(db.TEXT)
    census_area = db.Column(db.TEXT)
    combined_authority = db.Column(db.TEXT)
    company = db.Column(db.TEXT)
    entity = db.Column(db.BIGINT)
    esd_inventory = db.Column(db.TEXT)
    local_authority_type = db.Column(db.TEXT)
    local_resilience_forum = db.Column(db.TEXT)
    opendatacommunities_area = db.Column(db.TEXT)
    opendatacommunities_organisation = db.Column(db.TEXT)
    region = db.Column(db.TEXT)
    shielding_hub = db.Column(db.TEXT)
    statistical_geography = db.Column(db.TEXT)
    twitter = db.Column(db.TEXT)
    website = db.Column(db.TEXT)
    wikidata = db.Column(db.TEXT)
    wikipedia = db.Column(db.TEXT)
    entry_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    start_date = db.Column(db.Date)

    def __repr__(self):
        return f"<{self.__class__.__name__}> organisation: {self.organisation} entry_date: {self.entry_date}"


class Source(db.Model):

    source = db.Column(db.TEXT, primary_key=True, nullable=False)
    documentation_url = db.Column(db.TEXT)
    attribution = db.Column(db.TEXT)
    licence = db.Column(db.TEXT)

    entry_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    endpoint = db.Column(db.TEXT, db.ForeignKey("endpoint.endpoint"))
    organisation = db.Column(db.TEXT, db.ForeignKey("organisation.organisation"))
    collection = db.Column(db.TEXT)


class Endpoint(db.Model):

    endpoint = db.Column(db.TEXT, primary_key=True, nullable=False)
    endpoint_url = db.Column(db.TEXT)
    parameters = db.Column(db.TEXT)
    plugin = db.Column(db.TEXT)
    entry_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)


class Collection(db.Model):

    collection = db.Column(db.TEXT, primary_key=True, nullable=False)
    name = db.Column(db.TEXT)
    entry_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)


class Dataset(db.Model):

    dataset = db.Column(db.TEXT, primary_key=True, nullable=False)
    description = db.Column(db.TEXT)
    key_field = db.Column(db.TEXT)
    entity_minimum = db.Column(db.BIGINT)
    entity_maximum = db.Column(db.BIGINT)
    name = db.Column(db.TEXT)
    paint_options = db.Column(JSON)
    plural = db.Column(db.TEXT)
    prefix = db.Column(db.TEXT)
    text = db.Column(db.TEXT)
    typology = db.Column(db.TEXT)
    wikidata = db.Column(db.TEXT)
    wikipedia = db.Column(db.TEXT)
    collection = db.Column(db.TEXT, db.ForeignKey("collection.collection"))
    typology = db.Column(db.TEXT, db.ForeignKey("typology.typology"))
    entry_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)


class Typology(db.Model):
    typology = db.Column(db.TEXT, primary_key=True, nullable=False)
    name = db.Column(db.TEXT)
    description = db.Column(db.TEXT)
    text = db.Column(db.TEXT)
    plural = db.Column(db.TEXT)
    wikidata = db.Column(db.TEXT)
    wikipedia = db.Column(db.TEXT)
    entry_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
