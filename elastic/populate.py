import os
import logging
from fortune_client import get_data, Parameters
from .es import populate_index
from dotenv import load_dotenv


root_language_exceptions: dict[str, str] = {
    "brasil": "br",
    "chinese": "zh",
    "computer": "es",
    "luka": "it",
    "luttazi": "it",
    "italia": "it",
}


def map_exeptions(item: str, default_language: str, language_exceptions: dict) -> str:
    try:
        language: str = language_exceptions[item]
    except KeyError:
        language: str = default_language

    return language


def populate(
        index_name: str,
        path: str | None = None,
        language: str = 'en',
        language_exceptions: dict | None = None
    ) -> None:

    logging.info(f"Processing: {path}, {language}")

    if path is None:
        path = ''

    data = get_data(Parameters(
        url=os.getenv('FORTUNE_API'),
        explore=True,
        recursive=False,
        path=(path,),
        index=None,
    ))

    for item in data:
        if item.isDirectory:
            for fortune_path in item.content:
                populate(index_name, item.path + fortune_path, language)
            continue

        if language_exceptions is not None:
            language = map_exeptions(item.path, language, language_exceptions)

        i: int = 0
        data: list = []
        for fortune in item.content:
            data.append(
                {
                    "fortune": fortune,
                    "file": item.path,
                    "index": i,
                    "length": len(fortune),
                    "language": language,
                    "text-hash": str(hash(fortune)),
                }
            )
            i += 1

        logging.info('language: %s, file: %s, fortunes: %d', language, item.path, len(data))
        populate_index(index_name, data)

