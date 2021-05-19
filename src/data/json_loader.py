import json

from src.data.data_loader import IDataLoader
from src.data.doc import Doc
from src.data.token import Token


class JsonLoader(IDataLoader):
    def __init__(self):
        super(JsonLoader, self).__init__()

    def read_data_from_corpus_folder(self, corpus):
        ret_docs = list()
        with open(corpus) as json_file:
            data = json.load(json_file)
            last_doc_id = None
            tok_inx = 0
            for doc_id, doc in data.items():
                tokens = list()
                for tok in doc:
                    sent_id, _, tok_text, _ = tok
                    if last_doc_id != doc_id:
                        tok_inx = 0
                        last_doc_id = doc_id
                    tokens.append(Token(sent_id, int(tok_inx), tok_text))
                    tok_inx += 1
                ret_docs.append(Doc(doc_id, "", tokens))
        return ret_docs
