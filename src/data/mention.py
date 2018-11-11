from typing import List


class Mention(object):
    def __init__(self, doc_id: str, sent_id: int, tokens: List[int],
                 mention_str: str, cur_with: str):
        '''

        :param doc_id: the document ID
        :param sent_id: the mention sentence ID
        :param tokens: the tokens number (list in case of a span)
        :param mention_str: the mention text
        :param cur_with: the within doc co-reference
        '''
        self.doc_id = doc_id
        self.sent_id = sent_id
        self.tokens = tokens
        self.mention_str = mention_str
        self.cur_with = cur_with
