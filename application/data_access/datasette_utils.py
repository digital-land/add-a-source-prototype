import datetime
import logging

import pandas as pd
import requests
from requests import adapters
from urllib3 import Retry


def get_datasette_http():
    """
    Function to return  http for the use of querying  datasette,
    specifically to add retries for larger queries
    """
    retry_strategy = Retry(total=3, status_forcelist=[400], backoff_factor=0)

    adapter = adapters.HTTPAdapter(max_retries=retry_strategy)

    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    return http


def get_datasette_query(db, sql, url="https://datasette.planning.data.gov.uk"):
    url = f"{url}/{db}.json"
    params = {"sql": sql, "_shape": "array", "_size": "max"}
    try:
        http = get_datasette_http()
        resp = http.get(url, params=params)
        resp.raise_for_status()
        df = pd.DataFrame.from_dict(resp.json())
        return df
    except Exception as e:
        logging.warning(e)
        return None


# def get_datasets_summary():
#     # get all the datasets listed with their active status
#     all_datasets = index_by("dataset", get_datasets())
#     missing = []

#     # add the publisher coverage numbers
#     dataset_coverage = publisher_coverage()
#     for d in dataset_coverage:
#         if all_datasets.get(d["pipeline"]):
#             all_datasets[d["pipeline"]] = {**all_datasets[d["pipeline"]], **d}
#         else:
#             missing.append(d["pipeline"])

#     # add the total resource count
#     dataset_resource_counts = resources_by_dataset()
#     for d in dataset_resource_counts:
#         if all_datasets.get(d["pipeline"]):
#             all_datasets[d["pipeline"]] = {**all_datasets[d["pipeline"]], **d}
#         else:
#             missing.append(d["pipeline"])

#     # add the first and last resource dates
#     dataset_resource_dates = first_and_last_resource()
#     for d in dataset_resource_dates:
#         if all_datasets.get(d["pipeline"]):
#             all_datasets[d["pipeline"]] = {**all_datasets[d["pipeline"]], **d}
#         else:
#             missing.append(d["pipeline"])

#     return all_datasets


def generate_weeks(number_of_weeks):
    now = datetime.datetime.now()
    monday = now - datetime.timedelta(days=now.weekday())
    dates = []
    for week in range(0, number_of_weeks):
        date = monday - datetime.timedelta(weeks=week)
        week_number = int(date.strftime("%W"))
        year_number = int(date.year)
        dates.append(
            {"date": date, "week_number": week_number, "year_number": year_number}
        )

    return list(reversed(dates))
