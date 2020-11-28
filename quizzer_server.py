import gzip
import json
import random
import re
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from multiprocessing import cpu_count
from socketserver import ThreadingMixIn
from threading import currentThread
from time import sleep
from urllib import parse
from urllib.parse import parse_qs, urlparse


import spacy
from loguru import logger

from ProcessPoolMixin import PooledProcessMixIn

from helpers import TextRank4Keyword

logger.add(
    sys.stderr,
    format="{time} {level} {message}",
    filter="my_module",
    level="INFO",
)

spacy_labels = [
    "FAC",
    "ORG",
    "LAW",
    "LOC",
    "PRODUCT",
    "EVENT",
    "WORK_OF_ART",
    "LAW",
    "LANGUAGE",
    "PERCENT",
    "NORP",
    "QUANTITY",
]


class Handler(BaseHTTPRequestHandler):
    def __init__(self, nlp, keywords, *args, **kwargs):
        self._keywords = keywords
        self.nlp = nlp
        super(Handler, self).__init__(*args, **kwargs)

    def do_ner(self, doc):
        ner = {ent.label_: ent.text for ent in doc.ents}
        return ner

    def do_np_pos_tag(self, doc):
        nouns = [token.text for token in doc if token.tag_ in ["NP", "NNP"]]
        return nouns

    def do_np(self, doc):
        np = [np.text for np in doc.noun_chunks if len(np.text.split()) > 1]
        return np

    def do_vb(self, doc):
        verbs = [
            token.text
            for token in doc
            if token.tag_ == "VB"
            and token.text
            not in ["being", "been", "will be", "will have", "will do"]
        ]
        return verbs

    def do_aux_verb(self, doc):
        aux_verb = {
            token.tag_: token.text for token in doc if token.tag_ == "MD"
        }
        return aux_verb

    def do_keywords(self, text):
        node_weight = self._keywords.analyze(
            text,
            candidate_pos=["NOUN", "PROPN", "VERB"],
            window_size=4,
            lower=False,
        )
        keywords = self._keywords.get_keywords(node_weight, 10)
        return keywords

    def sentence_scoring_filter(self, text: str) -> bool:
        """
        Returns True if the sentence is valid .

        Args:
            text (str): [description]

        Returns:
            bool: [description]
        """
        return text[-1] != "?" and text[-2] != "?" and len(text) > 60

    def sample_sentences(self, sentences: list, num_of_questions: int) -> list:
        """
        Return a random sample of sentences .

        Args:
            sentences (list): [description]
            num_of_questions (int): [description]

        Returns:
            list: [description]
        """
        sentences = list(filter(self.sentence_scoring_filter, sentences))
        selected = random.sample(
            sentences, k=min(num_of_questions, len(sentences))
        )
        return selected

    def make_sentences(self, doc, num):
        sentences = list(doc.sents)
        sentences = list(map(lambda x: x.text, sentences))
        sentences = self.sample_sentences(sentences, num)
        return sentences

    def make_output(self, **kwargs) -> dict:
        """
        Build a dictionary of output dictionaries .

        Returns:
            [dict]: [description]
        """
        out = {}
        out["ner"] = kwargs.get("ner", [])
        out["nps"] = kwargs.get("nps", [])
        out["nouns"] = kwargs.get("nouns", [])
        out["vb"] = kwargs.get("vb", [])
        out["aux_vb"] = kwargs.get("aux_vb", [])
        out["ix"] = kwargs.get("ix")
        return out

    def do_POST(self):
        """
        Do a POST request .
        """
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        body = json.loads(gzip.decompress(body))

        text, num = body["text"], body["num"]
        doc = nlp(text)

        out = {}
        sentences = self.make_sentences(doc, num)

        out["keywords"] = self.do_keywords(text)
        out["sentences"] = sentences

        analysis = []
        for ix, paragraph in enumerate(sentences):
            doc = nlp(paragraph)

            ner = self.do_ner(doc)
            np = self.do_np(doc)
            nouns = self.do_np_pos_tag(doc)
            vb = self.do_vb(doc)
            aux_vb = self.do_aux_verb(doc)

            analysis.append(
                self.make_output(
                    ner=ner, nps=np, nouns=nouns, vb=vb, aux_vb=aux_vb, ix=ix
                )
            )

        out["analysis"] = analysis

        self.send_response(200)
        self.end_headers()

        response = BytesIO()
        response.write(json.dumps(out).encode())
        self.wfile.write(response.getvalue())


class ThreadedHTTPServer(PooledProcessMixIn, HTTPServer):
    """
    Simple http-server
    """

    def __init__(
        self,
        nlp,
        keywords,
        processes=max(2, cpu_count()),
        threads=64,
        daemon=False,
        kill=True,
        debug=False,
        logger=None,
    ):
        """
        Constructor
        :param processes: processes pool length
        :type processes: int
        :param threads: threads pool length for process
        :type threads: int
        :param daemon: True if daemon threads
        :type daemon: bool
        :param kill: True if kill main process when shutdown
        :type kill: bool
        :param debug: True if debug mode
        :type debug: bool
        :param logger: logger
        :type logger: logging.Logger
        """

        HTTPServer.__init__(
            self,
            ("localhost", 8791),
            lambda *args, **kwargs: Handler(nlp, keywords, *args, **kwargs),
        )
        self._process_n = processes
        self._thread_n = threads
        self._daemon = daemon
        self._kill = kill
        self._debug = debug
        self._logger = logger
        self._init_pool()


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    infix_re = re.compile(r"""[-]~""")
    nlp.tokenizer.infix_finditer = infix_re.finditer

    keywords = TextRank4Keyword(nlp)

    # neuralcoref.add_to_pipe(nlp)

    server = ThreadedHTTPServer(
        processes=2, threads=4, logger=logger, nlp=nlp, keywords=keywords
    )
    try:
        server.serve_forever()
    finally:
        server.shutdown()

    print("Sage ready to name entities.")
