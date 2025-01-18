import requests
import xml.etree.ElementTree as ET
import json


def parse_xml_to_list(xml_content):
    root = ET.fromstring(xml_content)
    result = []
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
                result.append([text_query, language, sparql_query])
    return result


def parse_json_to_list(json_content):
    data = json.loads(json_content)
    result = []

    for question in data.get("questions", []):
        sparql_query = question.get("query", "<SPARQL_QUERY_NOT_AVAILABLE>")
        for body in question.get("body", []):
            language = body.get("language", "unknown")
            if language in ["en", "de"]:  # Filter for English and German entries
                text_query = body.get("string", "").strip()
                result.append([text_query, language, sparql_query])
    return result


if __name__ == "__main__":
    # url = "https://raw.githubusercontent.com/ag-sc/QALD/master/3/data/dbpedia-train.xml"  # Use the raw URL
    # response = requests.get(url)

    # if response.status_code == 200:
    #     xml_content = response.text
    #     parsed_list = parse_xml_to_list(xml_content)
    #     for item in parsed_list[:10]:  # Display only the first 10 entries for brevity
    #         print(item)
    # else:
    #     print(f"Failed to fetch XML file. Status code: {response.status_code}")

    url_json = "https://raw.githubusercontent.com/ag-sc/QALD/refs/heads/master/5/data/qald-5_train.json"
    response_json = requests.get(url_json)
    if response_json.status_code == 200:
        parsed_list = parse_json_to_list(response_json.text)
        for item in parsed_list[-10:]:
            print(item)
    else:
        print(f"Failed to fetch XML file. Status code: {response.status_code}")
