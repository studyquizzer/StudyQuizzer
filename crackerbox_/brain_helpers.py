import random
import re

import inflect
from nltk.corpus import wordnet as wn
from word2number import w2n

ordinals = [
    "first",
    "second",
    "third",
    "fourth",
    "fifth",
    "sixth",
    "seventh",
    "eighth",
    "ninth",
    "tenth",
]


def mismatch_date(sentence, data):
    # In progress, need more ways to convert number strings to digit
    pass


def mod_ordinals(sentence, data):
    _ord = data["ner"]["ORDINAL"]
    distractor = random.choice([item for item in ordinals if item != _ord])
    sentence, done = re.subn(re.escape(_ord), distractor, sentence, 1)
    if not done:
        sentence = None
    return sentence


def mod_cardinals(sentence, data):
    original = data["ner"]["CARDINAL"]
    _card = data["ner"]["CARDINAL"]
    use_word = False
    try:
        _card = re.findall("\d+", _card)[0]
        _card = int(_card)
    except (ValueError, IndexError) as e:
        _card = _card if _card[-1] != "s" else _card[:-1]
        _card = w2n.word_to_num(_card)
        use_word = True
        p = inflect.engine()

    distractor = random.choice(
        [ix for ix in list(range(1, 15)) if ix != _card]
    )
    distractor = (
        p.number_to_words(distractor, andword=" and")
        if use_word
        else distractor
    )

    sentence, done = re.subn(re.escape(original), str(distractor), sentence, 1)
    if not done:
        sentence = None
    return sentence


def negate_aux(sentence, data):
    """
        Todo negate other named entities
    """
    negate = random.choice(list(data["aux_vb"].values()))

    possible = [
        [f"{negate}n't", negate],
        [f'{negate}n"t', negate],
        [f"{negate} not", negate],
        [negate, f"{negate} not"],
    ]

    for ix in possible:
        sentence, done = re.subn(
            re.escape(ix[0]),
            ix[1] if ix[1].lower() != "wo" else "will",
            sentence,
            1,
        )
        if done:
            break
    if not done:
        return None
    return sentence


def can_do_tf(data):
    ner = data["ner"]

    has_ordinals = "ORDINAL" in ner
    has_cardinals = "CARDINAL" in ner

    has_aux_verbs = data["aux_vb"] != {}

    _commands = [has_ordinals, has_cardinals, has_aux_verbs]
    commands = ["ordinals", "cardinals", "negate_aux"]

    if any(_commands):
        trues = list(filter(lambda x: x[0] is True, zip(_commands, commands)))
        return True, random.choice(trues)[1]

    return False, False
