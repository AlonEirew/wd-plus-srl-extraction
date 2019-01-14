class Token(object):
    def __init__(self, sent_id: int, token_id: int, token_text: str):
        self.sent_id = sent_id
        self.token_id = token_id
        self.token_text = token_text
        self.doc_tok_id_span = None # List[int]
        self.span_closed = False
        self.within_coref = set()
