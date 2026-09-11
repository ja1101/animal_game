import json
import random
from urllib.request import urlopen

ANIMAL_LIST_URL = 'https://raw.githubusercontent.com/dariusk/corpora/master/data/animals/common.json'
FALLBACK_ANIMALS = ['cat', 'dog', 'elephant', 'giraffe', 'lion', 'tiger', 'zebra', 'monkey', 'rabbit', 'fox']

_cached_animals = None

def _load_animals():
    global _cached_animals
    if _cached_animals is None:
        try:
            with urlopen(ANIMAL_LIST_URL, timeout=10) as response:
                animals = json.loads(response.read().decode('utf-8'))['animals']
            if animals:
                _cached_animals = animals
        except OSError:
            pass
        if _cached_animals is None:
            _cached_animals = FALLBACK_ANIMALS
    return _cached_animals

def get_random_animal():
    ''' Returns a random animal name '''
    return random.choice(_load_animals()).lower()