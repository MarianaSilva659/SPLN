import os
import lzma
from enum import Enum
from typing import Dict

from probability import AbsoluteProbability


class Languages(Enum):
    Pt = "pt"


def get_dictionary(lang: Languages) -> Dict[str, AbsoluteProbability]:
    cur_dir = os.path.dirname(__file__)
    path = os.path.join(cur_dir, 'corpus', f'{lang.value}.xz')

    result = {}
    total = 0

    f = lzma.open(path, 'rt', encoding='utf-8')
    for idx, line in enumerate(f):
        value_str, key = line.strip().split('\t', 1)
        value = int(value_str)
        result[key] = value
        total += value

    return {key: AbsoluteProbability(value, total) for key, value in result.items()}
