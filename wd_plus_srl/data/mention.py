from typing import List


class Mention(object):
    def __init__(self, doc_id: str, sent_id: int, tokens_number: List[int],
                 tokens_str: str, coref_chain: str, context: str = None):
        '''

        :param doc_id: the document ID
        :param sent_id: the mention sentence ID
        :param tokens_number: the tokens number (list in case of a span)
        :param tokens_str: the mention text
        :param coref_chain: the within doc co-reference
        '''
        self.doc_id = doc_id
        self.sent_id = sent_id
        self.tokens_number = tokens_number
        self.tokens_str = tokens_str
        self.coref_chain = coref_chain
        self.context = context
