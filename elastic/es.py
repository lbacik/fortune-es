import os
import json
from elasticsearch import Elasticsearch


es: Elasticsearch = None


def create_connection() -> None:
    global es

    ES_HOST: str = os.getenv('ES_HOST')

    # print(f'Connecting to Elasticsearch: {ES_HOST}')

    es = Elasticsearch(
        os.getenv('ES_HOST'),
        http_auth=(os.getenv('ES_USER'), os.getenv('ES_PASS')), 
        scheme=os.getenv('ES_SCHEME'),
        port=os.getenv('ES_PORT'),
    )


def ping() -> bool:
    return es.ping()


def print_info() -> None:
    print('PING:', ping())

    info = es.info()
    print(json.dumps(info, indent=2))


def print_all_indices() -> None:
    indices = es.indices.get_alias().keys()
    for index_name in list(indices):
        print(index_name)


def create_index(index_name: str, mapping: dict) -> None:

    result = es.indices.create(
        index=index_name,
        ignore=400,
        body=mapping,
    )
    print(result)


def populate_index(index_name: str, data: list) -> None:

    for item in data:
        try:
            es.index(
                index=index_name,
                body=item,
            )
        except Exception as e:
            print(e)
            os.sleep(5)


def search(index_name: str, query: dict) -> dict:

    result = es.search(
        index=index_name,
        q=query,
    )
    return result


