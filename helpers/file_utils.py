import requests
import xml.etree.ElementTree as ET


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