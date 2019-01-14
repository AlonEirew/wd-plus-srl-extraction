from typing import List

from src.data.mention import Mention
from src.data.sentence import Sentence
from src.data.token import Token


class Doc(object):
    def __init__(self, doc_id: str, text: str, tokens: List[Token]):
        self.doc_id = doc_id
        self.text = text
        self.tokens = tokens

    def find_token_and_set_cluster_id(self, tok_id, cluster_num):
        found = False
        for token in self.tokens:
            if token.doc_tok_id_span and tok_id in token.doc_tok_id_span:
                token.within_coref.add(cluster_num)
                found = True

        if not found:
            print("**** Token not found for-" + self.doc_id + ', Resource token-' + str(tok_id))

    def set_within_allen_coref(self, clusters):
        for i in range(0, len(clusters)):
            cluster = clusters[i]
            for coref_span in cluster:
                for tok_id in range(coref_span[0], coref_span[1] + 1):
                    self.find_token_and_set_cluster_id(tok_id, i)

    def set_within_spacy_coref(self, clusters):
        for i in range(0, len(clusters)):
            cluster = clusters[i]
            for mention in cluster:
                coref_span = [mention.start, mention.end]
                for tok_id in range(coref_span[0], coref_span[1]):
                    self.find_token_and_set_cluster_id(tok_id, i)

    def align_with_resource_doc(self, resource_doc):
        for i in range(0, len(resource_doc)):
            if str(resource_doc[i]) == self.tokens[i].token_text:
                self.tokens[i].doc_tok_id_span = [i, i]
                self.tokens[i].span_closed = True
            else:
                print('***** OUT OF SYNC ****')

    def get_words(self):
        words = list()
        for token in self.tokens:
            words.append(token.token_text)

        return words

    def create_mentions_data(self):
        mentions_result = list()
        for i in range(0,len(self.tokens)):
            token = self.tokens[i]
            while len(token.within_coref) > 0:
                cur_with = next(iter(token.within_coref))
                token.within_coref.remove(cur_with)
                mention_str = token.token_text
                token_ids = [token.token_id]
                for j in range(i+1, len(self.tokens)):
                    if cur_with in self.tokens[j].within_coref:
                        mention_str += ' ' + self.tokens[j].token_text
                        token_ids.append(self.tokens[j].token_id)
                        self.tokens[j].within_coref.remove(cur_with)
                    else:
                        break

                mention_data = Mention(self.doc_id, int(token.sent_id), token_ids, mention_str, str(cur_with))
                mentions_result.append(mention_data)

        return mentions_result

    @staticmethod
    def to_sentences(documents):
        sentences = list()
        for doc in documents:
            sent_id = 0
            sentence = Sentence(doc.doc_id, sent_id)
            for token in doc.tokens:
                if token.sent_id != sent_id:
                    sentences.append(sentence)
                    sent_id = token.sent_id
                    sentence = Sentence(doc.doc_id, sent_id)
                    sentence.add_token(token)
                else:
                    sentence.add_token(token)

            sentences.append(sentence)

        return sentences
