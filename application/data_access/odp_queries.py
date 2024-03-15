from application.data_access.datasette_utils import get_datasette_query

SPATIAL_DATASETS = [
    "article-4-direction-area",
    "conservation-area",
    "listed-building-outline",
    "tree-preservation-zone",
    "tree",
]
DOCUMENT_DATASETS = [
    "article-4-direction",
    "conservation-area-document",
    "tree-preservation-order",
]

COHORTS = [
    "ODP-Track1",
    "ODP-Track2",
    "ODP-Track3",
    "ODP-Track4",
    "RIPA-BOPS",
]


def get_odp_status_summary(dataset_type, cohort):
    cohort_filter = f"where odp_orgs.cohort = '{cohort}'" if cohort in COHORTS else ""
    sql = f"""
        select
            odp_orgs.organisation,
            odp_orgs.cohort,
            odp_orgs.name,
            rle.collection,
            rle.pipeline,
            rle.endpoint,
            rle.endpoint_url,
            rle.status,
            rle.exception,
            rle.resource,
            rle.latest_log_entry_date,
            rle.endpoint_entry_date,
            rle.endpoint_end_date,
            rle.resource_start_date,
            rle.resource_end_date
        from (
            select p.organisation, p.cohort, o.name from provision p
                inner join organisation o on o.organisation = p.organisation
                where "cohort" not like "RIPA-Beta" and "project" like "open-digital-planning"
            group by p.organisation
        )
        as odp_orgs
        left join reporting_latest_endpoints rle on replace(rle.organisation, '-eng', '') = odp_orgs.organisation
        {cohort_filter}
        order by odp_orgs.cohort
    """
    status_df = get_datasette_query("digital-land", sql)
    rows = []
    if status_df is not None:
        organisation_cohort_dict_list = (
            status_df[["organisation", "cohort", "name"]]
            .drop_duplicates()
            .to_dict(orient="records")
        )
        if dataset_type == "spatial":
            datasets = SPATIAL_DATASETS
        elif dataset_type == "document":
            datasets = DOCUMENT_DATASETS
        else:
            datasets = [*SPATIAL_DATASETS, *DOCUMENT_DATASETS]
        for organisation_cohort_dict in organisation_cohort_dict_list:
            rows.append(
                create_row(
                    organisation_cohort_dict["organisation"],
                    organisation_cohort_dict["cohort"],
                    status_df,
                    datasets,
                )
            )

        # Calculate overview stats
        percentages = 0.0
        datasets_added = 0
        for row in rows:
            percentages += float(row[-1]["text"].strip("%")) / 100
            for cell in row:
                print(cell)
                if cell.get("data", None) and cell["text"] != "No endpoint":
                    datasets_added += 1
        average_percentage = str(100 * (percentages / len(rows)))[:2] + "%"
        datasets_added = str(datasets_added)
        max_datasets = len(rows) * len(datasets)

        headers = [
            {"text": "Cohort"},
            {"text": "Organisation"},
            *map(lambda dataset: {"text": dataset}, datasets),
            {"text": "% provided"},
        ]
        return {
            "rows": rows,
            "headers": headers,
            "percentage_datasets_added": average_percentage,
            "datasets_added": datasets_added,
            "max_datasets": max_datasets,
        }

    else:
        return None


def create_row(organisation, cohort, status_df, datasets):
    row = []
    row.append({"text": cohort, "classes": "reporting-table-sticky-cell"})
    row.append({"text": organisation, "classes": "reporting-table-sticky-cell"})
    provided_score = 0
    for dataset in datasets:
        df_row = status_df[
            (status_df["organisation"] == organisation)
            & (status_df["pipeline"] == dataset)
        ]
        if len(df_row) != 0:
            provided_score += 1
            if df_row["status"].values:
                status = df_row["status"].values[0]
            else:
                # Look at exception for status
                if df_row["status"].values:
                    status = df_row["status"].values[0]
        else:
            status = "None"

        if status == "200":
            text = "Yes"
            classes = "reporting-good-background reporting-table-cell"
        elif (
            status != "None" and status != "200" and df_row["endpoint"].values[0] != ""
        ):
            text = "Yes - erroring"
            classes = "reporting-bad-background reporting-table-cell"
        else:
            text = "No endpoint"
            classes = "reporting-null-background reporting-table-cell"

        row.append(
            {
                "text": text,
                "classes": classes,
                "data": df_row.fillna("").to_dict(orient="records")
                if (len(df_row) != 0)
                else {},
            }
        )
    # Calculate % of endpoints provided
    provided_percentage = str(int(provided_score / len(datasets) * 100)) + "%"
    row.append({"text": provided_percentage, "classes": "reporting-table-cell"})
    return row