import argparse
import json
import logging
from .es import *
from .fortune import FortuneClient
from .populate import populate, root_language_exceptions
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)


parser : argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument('--env-file', type=str, help='env file path', default='.env')
parser.add_argument('--ping', action='store_true', help='Ping the server')
parser.add_argument('--info', action='store_true', help='Get info about the server')
parser.add_argument('--indices', action='store_true', help='Get all indices')
parser.add_argument('--create', type=str, help='Create index')
parser.add_argument('--mapping', type=str, help='Mapping file')
parser.add_argument('--populate', type=str, help='Populate index')
parser.add_argument('--index', type=str, help='Index name')
parser.add_argument('--search', type=str, help='Search query')


args : argparse.Namespace = parser.parse_args()


def file_to_dict(filename) -> dict:
    with open(filename, 'r') as f:
        return json.load(f)


def map_exeptions(item: str) -> str:
    language: str = 'en'

    exceptions: dict[str, str] = {
        "brasil": "br",
        "chinese": "zh",
        "computer": "es",
        "luka": "it",
        "luttazi": "it",
        "italia": "it",
    }

    try:
        language = exceptions[item]
    except KeyError:
        pass

    return language


if args.env_file:
    load_dotenv(args.env_file)
else:
    load_dotenv()


create_connection()


if args.ping:
    print('PING:', ping())

if  args.info:
    print_info()

if args.indices:
    print_all_indices()

if args.create:
    mapping: dict = file_to_dict(args.mapping)
    create_index(args.create, {"mappings": mapping})

if args.populate:
    logging.info('Populating index %s', args.populate)
    populate(args.populate, language_exceptions=root_language_exceptions)

if args.search:
    result = search(args.index, args.search)
    print(json.dumps(result))


