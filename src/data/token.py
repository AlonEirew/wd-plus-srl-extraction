class Token(object):
    def __init__(self, sent_id, token_id, token_text):
        self.sent_id = sent_id
        self.token_id = token_id
        self.token_text = token_text
        self.allen_doc_tok_id_span = None
        self.allen_span_closed = False
        self.within_coref = set()