import requests
import xml.etree.ElementTree as ET
import json
import pandas as pd


def parse_xml_to_dataframe(xml_content):
    root = ET.fromstring(xml_content)
    data = []
    for question in root.findall("question"):
        sparql_query = (
            question.find("query").text
            if question.find("query") is not None
            else "<SPARQL_QUERY_NOT_AVAILABLE>"
        )
        for string_element in question.findall("string"):
            language = string_element.attrib.get("lang", "unknown")
            if language in ["en", "de"]:  # Filter for English and German entries
                text_query = string_element.text.strip()
                data.append(
                    {
                        "text_query": text_query,
                        "language": language,
                        "sparql_query": sparql_query,
                    }
                )
    return pd.DataFrame(data)


def parse_json_to_dataframe(json_content):
    data = json.loads(json_content)
    rows = []

    for question in data.get("questions", []):
        sparql_query = question.get("query", "<SPARQL_QUERY_NOT_AVAILABLE>")
        for body in question.get("body", []):
            language = body.get("language", "unknown")
            if language in ["en", "de"]:  # Filter for English and German entries
                text_query = body.get("string", "").strip()
                rows.append(
                    {
                        "text_query": text_query,
                        "language": language,
                        "sparql_query": sparql_query,
                    }
                )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    url_json = "https://raw.githubusercontent.com/ag-sc/QALD/refs/heads/master/5/data/qald-5_train.json"
    response_json = requests.get(url_json)

    if response_json.status_code == 200:
        parsed_df = parse_json_to_dataframe(response_json.text)
        print(parsed_df.head(10))  # Display the last 10 rows of the DataFrame
    else:
        print(f"Failed to fetch JSON file. Status code: {response_json.status_code}")
