from faker import Faker
import random


class Config:
    """
    Configuration class for YouTube video view simulation.

    Each property could be adjusted as needed.
    """
    PAUSE_VID_PROBABILITY = 0.2  # TODO: Set to 0.1
    PAUSE_MIN_DURATION = 4
    PAUSE_MAX_DURATION = 10
    SCROLL_PROBABILITY = 0.9
    DEFAULT_SLEEP_TIME = 3
    WAIT_FOR_ELEM_TIME = 10
    FAKE_WORD_MIN_LENGTH = 1
    FAKE_WORD_MAX_LENGTH = 4


def generate_random_search_query():
    """
    Generates a random search query using the faker library.
    """
    fake = Faker()
    query_length = random.randint(Config.FAKE_WORD_MIN_LENGTH, Config.FAKE_WORD_MAX_LENGTH)
    query = ' '.join(fake.words(nb=query_length))
    return query
