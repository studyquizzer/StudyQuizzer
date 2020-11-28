import gzip
import json
import random
import re
import traceback

import requests
from Crackerbox.settings import cursor
from nltk.corpus import stopwords
from textblob import TextBlob

from brain_helpers import can_do_tf, mod_cardinals, mod_ordinals, negate_aux
from crackerbox_.models import (
    Document,
    Question,
    DocumentError,
    COMPLETE,
    PROCESSING,
    ERROR,
)
from exceptions import NotEnoughWordsError


# Need to refactor selection of distractors to account for incomplete ones.


perform_negation = [True, False]

en_stopwords = stopwords.words("english")

headers = {"Content-Type": "application/json", "content-encoding": "gzip"}
spacy_url = "http://localhost:8791/"


def assert_text_usable(text):
    length = len(text.split())
    okay = length > 40

    if not okay:
        raise NotEnoughWordsError(length)

    return True


def generate_single_tf(command, sentence, data, doc):

    actions = {
        "cardinals": mod_cardinals,
        "ordinals": mod_ordinals,
        "negate_aux": negate_aux,
        # "dates": mismatch_date,
    }

    answer = random.choice(perform_negation)  # make choice to negate sentence

    if answer:
        _negated_sentence = actions[command](sentence, data)
        negated_sentence = f"{_negated_sentence} ?"
    else:
        _negated_sentence = True
        negated_sentence = f"{sentence} ?"

    # check whether negation was done successfully

    if _negated_sentence:
        Question.objects.create(
            question_type="TF",
            doc=doc,
            text=negated_sentence,
            answer=not answer,
        )
    else:
        Question.objects.create(
            type="TF", doc=doc, text=negated_sentence, answer=True,
        )


def fetch_similar(cursor, word):
    sql = "select * from distractors where word = (?)"

    _word = word.split()

    word = word if len(_word) == 1 else _word[1]

    cursor.execute(sql, (word,))
    data = cursor.fetchall()
    return data


def get_distractors(cursor, keywords, gap, gap_type):

    distractors = []
    data = []

    if gap_type == "ner":
        data = fetch_similar(cursor, gap)

    if data:
        data = data[0][2].split()
        distractors = random.sample(data, k=2)

    if distractors:
        distractors.extend(random.sample(keywords, k=2))
    else:
        distractors = random.sample(keywords, k=4)

    # optimize distraction selection
    if not gap in distractors:  # shot circuit with most popular condition
        distractors = distractors[:-1]
    else:
        distractors.remove(gap)

    return distractors


def generate_fill_in_the_blank(sentence, data, keywords, cursor, doc):
    def make_weights(length):
        if length == 1:
            return [1.0]
        elif length == 2:
            return [0.6, 0.4]
        else:
            return [0.4, 0.3, 0.3]

    availables = [
        param
        for param, payload in data.items()
        if payload and param in ["nps", "ner", "nouns"]
    ]

    if availables:
        gap_type = random.choices(
            availables, k=1, weights=make_weights(len(availables))
        )[
            0
        ]  # make generation based on noun phrases important!

        gaps = (
            data[gap_type] if gap_type != "ner" else list(data["ner"].values())
        )
    else:
        gaps = sentence.split()
        gap_type = "random"

    gap = random.choice(gaps)

    sentence = re.sub(re.escape(f"{gap}"), "____", sentence, 1)

    distractors = get_distractors(cursor, keywords, gap, gap_type)

    # question = Question(
    #     type="TF", question=sentence, answer=gap, distractors=distractors
    # )

    Question.objects.create(
        question_type="MCQ",
        doc=doc,
        text=sentence,
        answer=gap,
        option1=distractors[0],
        option2=distractors[1],
        option3=distractors[2],
    )


def crackerbox(text, id, num_of_questions):
    doc = Document.objects.get(unique_id=id)

    doc.status = PROCESSING
    doc.save()

    body = json.dumps({"text": text, "num": num_of_questions}).encode("utf-8")
    body = gzip.compress(body)

    response = requests.post(
        url=spacy_url, headers=headers, data=body,
    ).content

    response = json.loads(response.decode())
    sentences, sentences_data, keywords_ = (
        response["sentences"],
        response["analysis"],
        response["keywords"],
    )

    for data in sentences_data:

        current_sentence = sentences[int(data["ix"])]

        tf_present, tf_commands = can_do_tf(data)

        if tf_present:
            try:
                generate_single_tf(tf_commands, current_sentence, data, doc)
            except Exception as error:
                handle_error(
                    id,
                    "true or false exception  " + traceback.format_exc(),
                    current_sentence,
                )
            continue

        try:
            generate_fill_in_the_blank(
                current_sentence, data, keywords_, cursor, doc
            )
        except Exception as error:
            handle_error(
                id,
                "fill in the blank exception  " + traceback.format_exc(),
                current_sentence,
            )

    doc.status = COMPLETE
    doc.save()


def handle_async_error(task):
    if not task.success:
        doc_id = task.args[-2]
        doc_text = task.args[0]
        doc = Document.objects.get(unique_id=doc_id)

        doc.status = ERROR
        doc.save()

        DocumentError.objects.create(
            doc_id=doc_id, source_text=doc_text, error=task.result
        )


def handle_error(id, error, text):
    DocumentError.objects.create(doc_id=id, source_text=text, error=error)
