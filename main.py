from helpers import (
    parse_xml_to_dataframe,
    parse_json_to_dataframe,
    eliminate_invalid_sparql_queries,
)
import requests
import pandas as pd
import json

SOURCE_FILE = "sources/qald_urls.json"

with open(SOURCE_FILE, "r") as json_file:
    sources = json.load(json_file)
    xml_sources = sources["xml"]
    json_sources = sources["json"]

if __name__ == "__main__":
    all_data = []
    for url in xml_sources:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                all_data.append(parse_xml_to_dataframe(response.text))
            except Exception as e:
                print(f"Failed to parse XML file with url {url}. Error: {e}")
        else:
            print(f"Failed to fetch XML file. Status code: {response.status_code}")

    for url in json_sources:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                all_data.append(parse_json_to_dataframe(response.text))
            except Exception as e:
                print(f"Failed to parse JSON file with url {url}. Error: {e}")
        else:
            print(f"Failed to fetch JSON file. Status code: {response.status_code}")

    all_data_df = pd.concat(all_data)
    # elimininate duplicate rows
    all_data_df.drop_duplicates(
        subset=["text_query", "language", "sparql_query"], inplace=True
    )

    all_data_df = all_data_df[
        all_data_df.sparql_query != "<SPARQL_QUERY_NOT_AVAILABLE>"
    ]
    # store all data in a file
    all_data_df.to_csv("qald_challenges.csv", index=False)

    # valid_data_df = eliminate_invalid_sparql_queries(all_data_df)
    # print(valid_data_df)
