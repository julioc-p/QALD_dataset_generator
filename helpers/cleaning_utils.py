from .sparql_validation_utils import validate_sparql_query_result
from SPARQLWrapper import SPARQLWrapper, JSON
import requests, time, pandas as pd

sparql = SPARQLWrapper("https://dbpedia.org/sparql")


def eliminate_invalid_sparql_queries(dataframe):
    valid_entries = dataframe[dataframe.sparql_query.str.contains("PREFIX")]
    valid_entries, _ = validate_queries(valid_entries)
    return valid_entries


def validate_queries(dataframe):
    # return valid entries and invalid entries separately in different dataframes
    valid_queries = []
    invalid_queries = []
    for index, row in dataframe.iterrows():
        query = row["sparql_query"]
        # get the result of the query by sending it to the SPARQL endpoint
        result = send_query_to_sparql_endpoint(query)
        if validate_sparql_query_result(result):
            valid_queries.append(row)
        else:
            invalid_queries.append(row)
            print(row)
    return pd.DataFrame(valid_queries), pd.DataFrame(invalid_queries)


def send_query_to_sparql_endpoint(query):
    sparql.setQuery(query)
    # send the query to the SPARQL endpoint and return the result
    sparql.setReturnFormat(JSON)
    try:
        response = sparql.query().convert()
    except Exception as e:
        print(f"Failed to send query to SPARQL endpoint. Error: {e}")
        return None
    # sleep for 1 second to avoid overloading the SPARQL endpoint
    time.sleep(1)
    # check if the response is valid
    return response


if __name__ == "__main__":

    print(send_query_to_sparql_endpoint("SELECT * WHERE { ?s ?p ?o } LIMIT 10"))
