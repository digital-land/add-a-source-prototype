import datetime

import pandas as pd

from application.data_access.datasette_utils import generate_weeks, get_datasette_query


def get_logs():
    sql = """
        select year, month, week, day, status, entry_date, count
        from (
            select
                case when (status = '200') then '200' else 'Not 200' end as status,
                strftime('%Y',entry_date) as year,
                strftime('%m',entry_date) as month,
                strftime('%W',entry_date) as week,
                strftime('%d',entry_date) as day,
                substr(entry_date,1,10) as entry_date,
                count(*) as count
            from log
            group by year, week, status
        ) as t1
        where cast(year as int) > 2018
        group by year, week, status
    """
    logs_df = get_datasette_query("digital-land", sql)
    if logs_df is not None:
        return logs_df
    else:
        return None


def get_issue_counts():
    sql = """
        select
            it.severity, count(*) as count
        from issue i
        inner join issue_type it
        where i.issue_type = it.issue_type
        group by it.severity
    """
    issues_df = get_datasette_query("digital-land", sql)
    if issues_df is not None:
        errors = issues_df[issues_df["severity"] == "error"].iloc[0]["count"]
        warning = issues_df[issues_df["severity"] == "warning"].iloc[0]["count"]
        return errors, warning
    else:
        return None


def get_contributions_and_erroring_endpoints():
    current_date = datetime.datetime.now().date()
    date_query = (
        f" where year = '{current_date.year - 1}' or year = '{current_date.year}'"
    )
    sql = f"""
        select
            count(*) as count,
            status,
            substr(entry_date,1,10) as entry_date,
            strftime('%Y',entry_date) as year
            from log l
            {date_query}
            group by substr(entry_date,1,10), case when status = '200' then status else 'not_200' end
    """
    contributions_and_errors_df = get_datasette_query("digital-land", sql)
    if contributions_and_errors_df is not None:
        contributions_df = contributions_and_errors_df[
            contributions_and_errors_df["status"] == "200"
        ].reindex()
        errors_df = contributions_and_errors_df[
            contributions_and_errors_df["status"] != "200"
        ].reindex()
        contributions = contributions_df["count"].tolist()
        contributions_dates = contributions_df["entry_date"].tolist()
        errors = errors_df["count"].tolist()
        errors_dates = errors_df["entry_date"].tolist()
        return {"dates": contributions_dates, "contributions": contributions}, {
            "dates": errors_dates,
            "errors": errors,
        }
    else:
        return None


def get_endpoints_added_by_week():
    sql = """
        select
            strftime('%Y',entry_date) as year,
            strftime('%m',entry_date) as month,
            strftime('%W',entry_date) as week,
            strftime('%d',entry_date) as day,
            count(endpoint),
            substr(entry_date,1,10) as entry_date
        from endpoint
        where year >= '2018'
        group by year, week
    """
    endpoints_added_df = get_datasette_query("digital-land", sql)
    if endpoints_added_df is not None:
        endpoints_added_df["week"] = pd.to_numeric(endpoints_added_df["week"])
        endpoints_added_df["year"] = pd.to_numeric(endpoints_added_df["year"])
        min_entry_date = endpoints_added_df["entry_date"].min()
        dates = generate_weeks(date_from=min_entry_date)
        endpoints_added = []
        for date in dates:
            current_date_data_df = endpoints_added_df[
                (endpoints_added_df["week"] == date["week_number"])
                & (endpoints_added_df["year"] == date["year_number"])
            ]
            if len(current_date_data_df) != 0:
                count = current_date_data_df["count(endpoint)"].values[0]
            else:
                count = 0
            endpoints_added.append(
                {"date": date["date"].strftime("%d/%m/%Y"), "count": count}
            )
        return endpoints_added
    else:
        return None


def get_endpoint_errors_and_successes_by_week(logs_df):
    logs_df["year"] = pd.to_numeric(logs_df["year"])
    logs_df["week"] = pd.to_numeric(logs_df["week"])
    min_entry_date = logs_df["entry_date"].min()
    dates = generate_weeks(date_from=min_entry_date)
    successes_by_week = []
    errors_by_week = []
    for date in dates:
        current_date_data_df = logs_df[
            (logs_df["week"] == date["week_number"])
            & (logs_df["year"] == date["year_number"])
        ]
        if len(current_date_data_df) > 0:
            successes_df = current_date_data_df[current_date_data_df["status"] == "200"]
            if len(successes_df) > 0:
                successes = successes_df["count"].values[0]
            else:
                successes = 0
            errors_df = current_date_data_df[
                current_date_data_df["status"] == "Not 200"
            ]
            if len(errors_df) > 0:
                errors = errors_df["count"].values[0]
            else:
                errors = 0
        else:
            successes = 0
            errors = 0

        successes_by_week.append(
            {"date": date["date"].strftime("%d/%m/%Y"), "count": successes}
        )
        errors_by_week.append(
            {"date": date["date"].strftime("%d/%m/%Y"), "count": errors}
        )
    return successes_by_week, errors_by_week
