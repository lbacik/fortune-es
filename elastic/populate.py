import os
import logging
from .fortune import FortuneClient
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
        path: str|None = None,
        language: str = 'en',
        language_exceptions: dict|None = None
    ) -> None:

    logging.info(f"Processing: {path}, {language}")

    fortune_client = FortuneClient(os.getenv('FORTUNE_API'))
    data: list = fortune_client.request(path)

    for item in data:
        if item[-1] == '/':
            lang: str = item[:-1]
            new_path = path + item if path is not None else item
            populate(index_name, new_path, lang)
            continue

        if language_exceptions is not None:
            language = map_exeptions(item, language, language_exceptions)

        fortune_file_path = path + item if path is not None else item
        fortunes: list = fortune_client.request(fortune_file_path)

        i: int = 0
        data: list = []
        for fortune in fortunes:
            data.append(
                {
                    "fortune": fortune,
                    "file": item,
                    "index": i,
                    "length": len(fortune),
                    "language": language,
                    "text-hash": str(hash(fortune)),
                }
            )
            i += 1
            # print(".", sep="", end="")

        logging.info('language: %s, file: %s, fortunes: %d', language, item, len(data))
        populate_index(index_name, data)

