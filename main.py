from helpers import (
    parse_xml_to_dataframe,
    parse_json_to_dataframe,
    eliminate_invalid_sparql_queries,
)
import requests
import pandas as pd

XML_SOURCES = [
    "https://raw.githubusercontent.com/ag-sc/QALD/refs/heads/master/3/data/dbpedia-train.xml",
    "https://raw.githubusercontent.com/ag-sc/QALD/refs/heads/master/3/data/dbpedia-test.xml",
    "https://raw.githubusercontent.com/ag-sc/QALD/refs/heads/master/5/data/qald-5_test.xml",
]
JSON_SOURCES = [
    "https://raw.githubusercontent.com/ag-sc/QALD/refs/heads/master/6/data/qald-6-test-multilingual.json",
    "https://raw.githubusercontent.com/ag-sc/QALD/refs/heads/master/6/data/qald-6-train-multilingual.json",
    "https://raw.githubusercontent.com/ag-sc/QALD/refs/heads/master/5/data/qald-5_train.json",
    "https://raw.githubusercontent.com/ag-sc/QALD/refs/heads/master/7/data/qald-7-train-multilingual.json",
    "https://raw.githubusercontent.com/ag-sc/QALD/refs/heads/master/9/data/qald-9-train-multilingual.json",
    "https://raw.githubusercontent.com/ag-sc/QALD/refs/heads/master/9/data/qald-9-test-multilingual.json",
    "https://raw.githubusercontent.com/ag-sc/QALD/refs/heads/master/7/data/qald-7-test-multilingual.json",
    "https://raw.githubusercontent.com/KGQA/QALD_9_plus/refs/heads/main/data/qald_9_plus_train_dbpedia.json",
    "https://raw.githubusercontent.com/KGQA/QALD_9_plus/refs/heads/main/data/qald_9_plus_test_dbpedia.json",
]
if __name__ == "__main__":
    all_data = []
    for url in XML_SOURCES:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                all_data.append(parse_xml_to_dataframe(response.text))
            except Exception as e:
                print(f"Failed to parse XML file with url {url}. Error: {e}")
        else:
            print(f"Failed to fetch XML file. Status code: {response.status_code}")
    #print(all_data[0].sparql_query[0])
    for url in JSON_SOURCES:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                all_data.append(parse_json_to_dataframe(response.text))
            except Exception as e:
                print(f"Failed to parse JSON file with url {url}. Error: {e}")
        else:
            print(f"Failed to fetch JSON file. Status code: {response.status_code}")

    all_data_df = pd.concat(all_data)
    
    valid_data_df = eliminate_invalid_sparql_queries(all_data_df)
    print(valid_data_df)
